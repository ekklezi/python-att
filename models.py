# models.py
from datetime import datetime
import re

class Expense:
    def __init__(
        self,
        id:int,
        car_id: int,
        amount: float,
        category: str,
        date: str,
        mileage: float,
        description: str = "",
    ):
        if amount <= 0:
            raise ValueError("Число должно быть положительным")
        self.id = id
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
            datetime.strptime(date_str, "%Y-%m-%d")
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
        return f"Expense: {self.amount} RUB in '{self.category}' on {self.date}"

class Car:
    def __init__(
        self,
        id: int,
        model: str,
        year: str|int,
        mileage: float,
        price: float,
    ):
        self.id = id
        self.model = model.strip()
        self.year = self._validate_year(year)
        self.mileage = mileage
        self.price = price
        self.expenses = []

    def to_dict(self):
        return {
            "id": self.id,
            "model": self.model,
            "mileage": self.mileage,
            "price": self.price,
            "year": self.year,
        }

    def calculate_expense(self):
        """Высчитывает стоимость содержания в рублях на километр (руб/км)"""
        current_mileage = sum_amount = 0
        for expense in self.expenses:
            sum_amount += expense.amount
            if expense.mileage > current_mileage:
                current_mileage = expense.mileage

        return sum_amount / (current_mileage - self.mileage)

    def __repr__(self):
        car_repr = f"А/М: {self.model} {self.year} г. \nПробег на момент покупки: {self.mileage:.1f} км"
        if self.expenses:
            car_repr += f"\nСтоимость содержания: {self.calculate_expense():.2f} руб/км"
        return car_repr

    @staticmethod
    def _validate_year(year_str: str|int) -> int:
        """
        Валидирует год выпуска А/М. Принимает строку либо целое число
        """
        year_pattern = re.compile(r'^[1-2]\d{3}$')
        now = int(datetime.now().strftime("%Y"))
        if not year_pattern.fullmatch(str(year_str)):
            raise ValueError("Год указан в некорректном формате")
        year = int(year_str)
        if year < 1885:
            raise ValueError("Первый автомобиль появился в 1885 г.")
        if year > now:
            raise ValueError("Год выпуска не может быть больше текущего")
        return year