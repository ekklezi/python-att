# models.py
import datetime
from typing import Optional

class Transaction:
    def __init__(
        self,
        amount: float,
        category: str,
        date: str,
        description: str = "",
        transaction_type: str = "expense"  # expense / income
    ):
        if transaction_type not in ("expense", "income"):
            raise ValueError("transaction_type must be 'expense' or 'income'")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.amount = amount
        self.category = category.strip()
        self.date = self._validate_date(date)
        self.description = description.strip()
        self.transaction_type = transaction_type

    @staticmethod
    def _validate_date(date_str: str) -> str:
        """Принимает дату в формате YYYY-MM-DD"""
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description,
            "transaction_type": self.transaction_type
        }

    def __repr__(self):
        return f"<Transaction: {self.transaction_type} {self.amount} RUB in '{self.category}' on {self.date}>"

class Car:
    def __init__(
        self,
        id: int,
        model: str,
        year: int,
        mileage: int,
        price: float,
    ):
        self.id = id
        self.model = model.strip()
        self.year = year
        self.mileage = mileage
        self.price = price