from fastapi import APIRouter

expense_router = APIRouter(
    prefix="/api/expense",
    tags=["expense"]
)

@expense_router.get("/")
async def list_expense():
    return {"message": []}