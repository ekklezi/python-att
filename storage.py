# storage.py
import os
import csv
from models import Transaction, Car
import sqlite3

# Путь к файлу данных
DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "app.db")
conn = sqlite3.connect(DB_FILE)
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
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_id INTEGER,
        amount REAL,
        date TEXT,
        description TEXT,
        category TEXT
    )
    ''')

def save_transaction(transaction:Transaction):
    try:
        cur.execute("INSERT INTO transactions (car_id, amount, date, description, category) VALUES (?, ?, ?, ?, ?)", transaction.to_dict())
        conn.commit()
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def load_transactions():
    """
    Загружает транзакции
    """
    transactions = []

    try:
        cur.execute("SELECT * FROM transactions ORDER BY id")
        rows = cur.fetchall()
        for row in rows:
            # Преобразуем строку CSV в объект Transaction
            t = Transaction(
                amount=float(row["amount"]),
                category=row["category"],
                date=row["date"],
                description=row.get("description", ""),
                transaction_type=row["transaction_type"]
            )
            transactions.append(t)

    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return []  # возвращаем пустой список при ошибке

    return transactions

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