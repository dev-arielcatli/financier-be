from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from features.expense.model import ExpenseDB, ExpenseRequest, get_expense_category

expense_router = APIRouter(prefix="/api/expense", tags=["expense"])


@expense_router.get("/")
async def list_expenses(
    user_id: str, start_date: datetime | None = None, end_date: datetime | None = None
):
    # TODO: Add date filtering
    expenses = ExpenseDB.query(
        user_id, ExpenseDB.category.startswith(get_expense_category())
    )
    return [expense.attribute_values for expense in expenses]


@expense_router.get("/{expense_id}")
async def get_expense(expense_id: str, user_id: str):
    try:
        expense = ExpenseDB.expense_id_index.query(
            user_id, ExpenseDB.id == expense_id
        ).next()
    except StopIteration as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="EXPENSE_NOT_FOUND"
        )
    return expense.attribute_values


@expense_router.post("/")
async def create_expense(expense: ExpenseRequest, user_id: str):
    new_expense = ExpenseDB(user_id=user_id, **expense.model_dump())
    new_expense.save()
    return new_expense.attribute_values


@expense_router.put("/{expense_id}")
async def update_expense(expense_id: str, expense: ExpenseRequest, user_id: str):
    try:
        fetched_expense = ExpenseDB.expense_id_index.query(
            user_id, ExpenseDB.id == expense_id
        ).next()
    except StopIteration as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="EXPENSE_NOT_FOUND"
        )
    fetched_expense.update(**expense.model_dump())
    return fetched_expense.attribute_values
