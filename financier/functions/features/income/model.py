import os
from datetime import datetime

APP_NAME = os.getenv("APP_NAME")
STAGE = os.getenv("STAGE")

from uuid import uuid4

from pydantic import BaseModel
from pynamodb.attributes import (
    ListAttribute,
    NumberAttribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
)
from pynamodb.indexes import AllProjection, LocalSecondaryIndex
from pynamodb.models import Model


def get_income_category():
    return "income"


class IncomeDBIDIndex(LocalSecondaryIndex):
    class Meta:
        index_name = f"{APP_NAME}-{STAGE}-table-main-id-index"
        projection = AllProjection()

    user_id = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)


class IncomeDB(Model):
    class Meta:
        table_name = f"{APP_NAME}-{STAGE}-table-main"

    income_id_index = IncomeDBIDIndex()

    def __init__(
        self, hash_key=None, range_key=None, _user_instantiated=True, **attributes
    ):
        super().__init__(hash_key, range_key, _user_instantiated, **attributes)
        self.id = self.get_unique_id() if not self.id else self.id
        self.category = self.get_category()
        if self.created_at is None:
            self.created_at = datetime.now()
        else:
            self.updated_at = datetime.now()
        self.date = datetime.now() if not self.date else self.date

    user_id = UnicodeAttribute(hash_key=True)
    category = UnicodeAttribute(range_key=True, default=get_income_category)
    created_at = UTCDateTimeAttribute(null=False)
    updated_at = UTCDateTimeAttribute(null=True)

    # Income attributes
    id = UnicodeAttribute(null=False)
    name = UnicodeAttribute(null=False)
    description = UnicodeAttribute(null=True)
    amount = NumberAttribute(null=True, default=0)
    quantity = NumberAttribute(null=True, default=1)
    source = ListAttribute(default=(), null=True)
    date = UTCDateTimeAttribute(null=False)
    tags = ListAttribute(default=())

    def get_category(self):
        return f"{get_income_category()}-{self.id}"

    def get_unique_id(self):
        return str(uuid4())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now()
        self.save()


class Income(BaseModel):
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
    source: list[str] | None


class IncomeRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    amount: float | None = None
    quantity: int | None = None
    date: datetime | None = None
    tags: list[str] | None = None
    source: list[str] | None = None


# FOR TESTING ONLY
if __name__ == "__main__":
    from datetime import datetime

    new_income = IncomeDB(
        user_id="default",
        name="Salary",
        amount=1000,
        description="Monthly salary",
        date=datetime.now(),
        tags=["salary", "income"],
        source="Employer",
    )
    new_income.save()

    income = IncomeDB.income_id_index.query(
        "default", IncomeDBIDIndex.id == new_income.id
    ).next()
    print("Income", income.attribute_values)
