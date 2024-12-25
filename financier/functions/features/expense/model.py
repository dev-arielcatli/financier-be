from datetime import datetime

from financier.config.config import APP_NAME, STAGE
from pydantic import BaseModel
from pynamodb.attributes import (
    ListAttribute,
    NumberAttribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
)
from pynamodb.models import Model

from uuid import uuid4

def get_expense_category():
    return "expense"

class ExpenseDB(Model):
    class Meta:
        table_name = f"{APP_NAME}-{STAGE}-table-main"

    def __init__(self, hash_key = None, range_key = None, _user_instantiated = True, **attributes):
        super().__init__(hash_key, range_key, _user_instantiated, **attributes)
        self.id = self.get_unique_id()
        self.category = self.get_category()
        self.created_at = datetime.now()
        self.date = datetime.now()

    user_id = UnicodeAttribute(hash_key=True)
    category = UnicodeAttribute(range_key=True, default=get_expense_category)
    created_at = UTCDateTimeAttribute(null=False)
    updated_at = UTCDateTimeAttribute(null=True)

    # Expense attributes
    id = UnicodeAttribute(null=False)
    name = UnicodeAttribute(null=False)
    description = UnicodeAttribute(null=True)
    amount = NumberAttribute(null=True, default=0)
    quantity = NumberAttribute(null=True, default=1)
    date = UTCDateTimeAttribute(null=False)
    tags = ListAttribute(default=())

    def get_category(self):
        return f"{get_expense_category()}-{self.id}"
    
    def get_unique_id(self):
        return str(uuid4())


class Expense(BaseModel):
    id: str
    name: str
    description: str | None
    amount: float
    quantity: int
    date: datetime
    created_at: datetime
    updated_at: datetime
    tags: list[str]
    user_id: str

# FOR TESTING ONLY
# if __name__ == "__main__":
#     from datetime import datetime
#     new_expense = ExpenseDB(
#         user_id="default",
#         name="Tender Juicy Hotdog",
#         description="Tender Juicy Hotdog is a brand of hotdog in the Philippines. It is a product of Mekeni Food Corporation.",
#         quantity=1,
#         amount=10.0,
#         tags=["food", "grocery"],
#     )
#     new_expense.save()

#     for expense in ExpenseDB.query("default", ExpenseDB.category.startswith(get_expense_category())):
#         print(expense.name)
#         print(expense.description)
#         print(expense.amount)
#         print(expense.quantity)
#         print(expense.tags)
#         print(expense.date)
#         print(expense.created_at)
#         print(expense.updated_at)
#         print(expense.id)
#         print(expense.category)
#         print(expense.user_id)
#         print("=====")