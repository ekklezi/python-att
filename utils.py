# utils.py
import re


def validate_amount(amount_str: str) -> float:
    """
    Проверяет и преобразует строку в число.
    Поддерживает точки и запятые как десятичный разделитель.
    Примеры: "100", "100.50", "100,50" → 100.5
    """
    if not isinstance(amount_str, str):
        raise ValueError("Сумма должна быть строкой")

    amount_str = amount_str.strip()
    if not amount_str:
        raise ValueError("Сумма не может быть пустой")

    # Заменяем запятую на точку (для русскоязычных пользователей)
    amount_str = amount_str.replace(',', '.')

    # Регулярное выражение: число, возможно с десятичной частью
    if not re.fullmatch(r"^\d+(\.\d+)?$", amount_str):
        raise ValueError("Неверный формат суммы. Используйте цифры и, при необходимости, точку или запятую.")

    amount = float(amount_str)
    if amount <= 0:
        raise ValueError("Сумма должна быть больше нуля")
    return amount


def validate_date(date_str: str) -> str:
    """
    Проверяет, что дата в формате YYYY-MM-DD с помощью регулярного выражения.
    """
    if not isinstance(date_str, str):
        raise ValueError("Дата должна быть строкой")

    date_str = date_str.strip()
    if not date_str:
        raise ValueError("Дата не может быть пустой")

    # Регулярное выражение: 4 цифры, дефис, 2 цифры, дефис, 2 цифры
    if not re.fullmatch(r"^\d{4}-\d{2}-\d{2}$", date_str):
        raise ValueError("Дата должна быть в формате ГГГГ-ММ-ДД (например, 2025-12-23)")

    # Дополнительная проверка: реальная дата (например, не 2025-99-99)
    from datetime import datetime
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Дата некорректна (например, 31 февраля)")

    return date_str


def validate_category(category_str: str) -> str:
    """
    Проверяет и очищает категорию.
    Не допускает пустые строки и только пробелы.
    """
    if not isinstance(category_str, str):
        raise ValueError("Категория должна быть строкой")

    category_str = category_str.strip()
    if not category_str:
        raise ValueError("Категория не может быть пустой")

    return category_str

def validate_year(year_str: str) -> int:
    year_pattern = re.compile(r'^[1-2]\d{3}$')
    if not year_pattern.fullmatch(year_str):
        raise ValueError("Год указан в некорректном формате")
    year = int(year_str)
    if year < 1885:
        raise ValueError("Первый автомобиль появился в 1885 г.")
    return year
