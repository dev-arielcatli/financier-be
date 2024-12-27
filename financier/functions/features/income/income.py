from datetime import datetime

from fastapi import APIRouter
from features.income.model import IncomeDB, get_income_category

income_router = APIRouter(prefix="/api/income", tags=["income"])


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
    income = IncomeDB.income_id_index.query(
        user_id, IncomeDB.id == income_id
    ).next()
    return income.attribute_values
