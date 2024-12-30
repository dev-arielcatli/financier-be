from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from features.income.model import IncomeDB, IncomeRequest, get_income_category

income_router = APIRouter(prefix="/income", tags=["income"])


@income_router.get("/")
async def list_incomes(
    user_id: str, start_date: datetime | None = None, end_date: datetime | None = None
):
    # TODO: Add date filtering
    incomes = IncomeDB.query(
        user_id, IncomeDB.category.startswith(get_income_category())
    )
    return [income.attribute_values for income in incomes]


@income_router.get("/{income_id}")
async def get_income(income_id: str, user_id: str):
    try:
        income = IncomeDB.income_id_index.query(
            user_id, IncomeDB.id == income_id
        ).next()
    except StopIteration as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="INCOME_NOT_FOUND")
    return income.attribute_values


@income_router.post("/")
async def create_income(income: IncomeRequest, user_id: str):
    new_income = IncomeDB(user_id=user_id, **income.model_dump())
    new_income.save()
    return new_income.attribute_values


@income_router.put("/{income_id}")
async def update_income(income_id: str, income: IncomeRequest, user_id: str):
    try:
        income_db = IncomeDB.income_id_index.query(
            user_id, IncomeDB.id == income_id
        ).next()
    except StopIteration as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="INCOME_NOT_FOUND")
    income_db.update(**income.model_dump())
    return income_db.attribute_values


@income_router.delete("/", status_code=HTTPStatus.NO_CONTENT)
async def delete_income(ids: Annotated[list[str], Body()], user_id: str):
    deleted = []
    not_found = []
    for id in ids:
        try:
            income_db = IncomeDB.income_id_index.query(
                user_id, IncomeDB.id == id
            ).next()
            income_db.delete()
            deleted.append(id)
        except StopIteration as e:
            not_found.append(id)
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"deleted": deleted, "not_found": not_found},
    )
