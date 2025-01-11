from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from features.expense.expense import expense_router
from features.income.income import income_router
from mangum import Mangum

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expense_router)
app.include_router(income_router)


@app.get("/v1")
async def main():
    return {"hello": "world"}


handler = Mangum(app)
