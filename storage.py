# storage.py
import os
import csv
from models import Transaction

# Путь к файлу данных
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "transactions.csv")

def ensure_data_dir():
    """Создаёт папку 'data', если она не существует."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_transactions(transactions):
    """
    Сохраняет список объектов Transaction в CSV-файл.
    Добавляет новые записи в конец файла.
    """
    if not transactions:
        return  # нечего сохранять

    ensure_data_dir()
    file_exists = os.path.isfile(CSV_FILE)

    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
            fieldnames = ["amount", "category", "date", "description", "transaction_type"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            # Записываем заголовок только при создании файла
            if not file_exists:
                writer.writeheader()

            # Записываем каждую транзакцию
            for t in transactions:
                writer.writerow(t.to_dict())

    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def load_transactions():
    """
    Загружает все операции из CSV-файла и возвращает список объектов Transaction.
    """
    transactions = []

    if not os.path.exists(CSV_FILE):
        return transactions  # первый запуск — файла ещё нет

    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
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