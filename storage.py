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
    """Создаёт папку 'data', если она не существует."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    cur.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT,
        year INTEGER,
        mileage INTEGER,
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
    try:
        cur.execute(
            '''INSERT INTO expenses (car_id, amount, date, category, description, mileage) 
                    VALUES (:car_id, :amount, :date, :category, :description, :mileage)''',
            expense.to_dict())

        conn.commit()
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def load_expenses(car_id:int):
    """
    Загружает транзакции
    """
    expenses = []

    try:
        cur.execute("SELECT car_id, amount, category, date, description, mileage FROM expenses WHERE car_id = :car_id", {"car_id": car_id})
        rows = cur.fetchall()
        for row in rows:
            # Преобразуем строку CSV в объект Transaction
            t = Expense(
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
    print(expenses)
    return expenses

def save_car(car):
    try:
        cur.execute("INSERT INTO cars (model, year, mileage, price) VALUES (?, ?, ?, ?)", car)
        conn.commit()
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def load_cars():
    cars = []
    try:
        cur.execute("SELECT * FROM cars ORDER BY id")
        rows = cur.fetchall()
        for row in rows:
            car = Car(row[0], row[1], row[2], row[3], row[4])
            cars.append(car)
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")

    return cars

def delete_car(car_id):
    print(car_id)
    try:
        cur.execute("DELETE FROM cars WHERE id = ?", (car_id,))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при удалении данных: {e}")