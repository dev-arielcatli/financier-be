from fastapi import FastAPI
from features.expense.expense import expense_router
from mangum import Mangum

app = FastAPI()

app.include_router(expense_router)


@app.get("/api")
async def main():
    return {"hello": "world"}


handler = Mangum(app)
