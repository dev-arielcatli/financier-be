from fastapi import FastAPI
from mangum import Mangum

from financier.functions.features.expense.expense import expense_router

app = FastAPI()

app.include_router(expense_router)

@app.get("/api")
async def main():
    return {"hello": "world"}


handler = Mangum(app)
