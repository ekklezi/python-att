# storage.py
import os
import csv
from models import Expense, Car
import sqlite3

# Путь к файлу данных
DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "app.db")
conn = sqlite3.connect(DB_FILE)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def init_storage():
    """
    Создаёт папку 'data', если она не существует.
    Создает таблицы БД, если не существуют
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    cur.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT,
        year INTEGER,
        mileage REAL,
        price REAL
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_id INTEGER,
        amount REAL,
        date TEXT,
        description TEXT,
        category TEXT,
        mileage REAL
    )
    ''')

def save_expense(expense:Expense):
    """
    Сохраняет в БД строку расхода
    """
    try:
        cur.execute(
            '''INSERT INTO expenses (car_id, amount, date, category, description, mileage) 
                    VALUES (:car_id, :amount, :date, :category, :description, :mileage)''',
            expense.to_dict())

        conn.commit()
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def load_expenses(car_id:int, raw:bool=False):
    """
    Получает из БД строки расходов по ID А/М
    Возвращает список объектов Expense, при передаче raw = true возвращает сырые данные для DataFrame
    """
    expenses = []
    try:
        cur.execute("SELECT id, car_id, amount, category, date, description, mileage FROM expenses WHERE car_id = :car_id ORDER BY mileage ASC", {"car_id": car_id})
        rows = cur.fetchall()
        if raw:
            return rows
        for row in rows:
            t = Expense(
                id=row['id'],
                car_id=row["car_id"],
                amount=float(row["amount"]),
                category=row["category"],
                date=row["date"],
                description=row["description"],
                mileage=row["mileage"]
            )
            expenses.append(t)

    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return []  # возвращаем пустой список при ошибке
    return expenses

def save_car(car):
    """
    Сохраняет в БД строку с данными А/М
    """
    try:
        cur.execute("INSERT INTO cars (model, year, mileage, price) VALUES (:model, :year, :mileage, :price)", car.to_dict())
        conn.commit()
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def load_cars():
    """
    Получает из БД строки расходов по ID А/М
    Возвращает список объектов Car
    """
    cars = []
    try:
        cur.execute("SELECT id, model, year, mileage, price FROM cars ORDER BY id")
        rows = cur.fetchall()
        for row in rows:
            car = Car(
                id=row['id'],
                model=row["model"],
                year=row["year"],
                mileage=row["mileage"],
                price=row["price"]
            )
            cars.append(car)
    except Exception as e:
        print(f"Ошибка при получении данных: 123{e}")

    return cars

def delete_car(car_id:int):
    """
    Удаляет из БД строку данных об А/М по переданному car_id
    Так же удаляет связанные строки расходов (по ключу car_id)
    """
    try:
        cur.execute("DELETE FROM cars WHERE id = ?", (car_id,))
        cur.execute("DELETE FROM expenses WHERE car_id = ?", (car_id,))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при удалении данных: {e}")

def delete_expense(expense_id:int):
    """
    Удаляет из БД строку данных о расходе по переданному id
    """
    try:
        cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при удалении данных: {e}")