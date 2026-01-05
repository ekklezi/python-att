# models.py
import datetime
from typing import Optional

class Expense:
    def __init__(
        self,
        car_id: int,
        amount: float,
        category: str,
        date: str,
        mileage: float,
        description: str = "",
    ):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.car_id = car_id
        self.amount = amount
        self.category = category.strip()
        self.date = self._validate_date(date)
        self.description = description.strip()
        self.mileage = mileage

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
            "car_id": self.car_id,
            "amount": self.amount,
            "date": self.date,
            "category": self.category,
            "description": self.description,
            "mileage": self.mileage
        }

    def __repr__(self):
        return f"<Expense: {self.amount} RUB in '{self.category}' on {self.date}>"

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