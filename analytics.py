import pandas as pd
from storage import load_expenses, load_cars
import matplotlib.pyplot as plt

def autopct_format(pct, values):
    """
    Форматирует процентоное значение barPlot для показа реального числа
    """
    total = sum(values)
    value = int(pct / 100 * total)
    return f'{value} руб.\n({pct:.1f}%)'

def show_expenses_categories(car_id):
    """
    Формирует диаграмму расходов по категориям для выбранного А/М
    """
    expenses = load_expenses(car_id, True)
    df = pd.DataFrame.from_records(expenses, columns=['id', 'car_id', 'amount', 'category', 'date', 'description', 'mileage'])
    sum = df.groupby('category', as_index=False)['amount'].sum()
    plt.figure(figsize=(9, 9))
    plt.pie(sum['amount'], labels=sum['category'], autopct=lambda pct: autopct_format(pct, sum['amount']), startangle=90, radius=0.5)
    plt.title('Затраты по категориям')
    plt.show()

def show_expenses_by_year(car_id):
    """
    Формирует график расходов по годам для выбранного А/М
    """
    expenses = load_expenses(car_id, True)
    df = pd.DataFrame.from_records(expenses,
                                   columns=['id', 'car_id', 'amount', 'category', 'date', 'description', 'mileage'])
    df['Year'] = pd.to_datetime(df['date']).dt.year
    grouped = df.groupby('Year', as_index=False)['amount'].sum()
    print(grouped['Year'])
    plt.bar(grouped['Year'], grouped['amount'])
    plt.xticks(grouped['Year'].to_numpy())
    plt.title("Расходны на авто по годам")
    plt.xlabel("Год")
    plt.ylabel("Сумма расходов, ₽")
    plt.show()

