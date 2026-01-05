# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from models import Expense, Car
from storage import save_expense, load_expenses, save_car, load_cars, delete_car
from utils import validate_amount, validate_date, validate_category
import tkinter.font as font

class FinancialPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Финансовый Планер")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        self.create_widgets()
        self.refresh_cars_tabs()
        self.refresh_car_expenses_table(list(self.cars_frames.keys())[0])

    def create_widgets(self):
        # === Верхняя панель: форма ввода ===
        input_frame = ttk.LabelFrame(self.root, padding=(10, 10))
        input_frame.pack(fill="x", padx=10, pady=(10, 5))
        my_font = font.Font(family="Helvetica", size=20, weight="bold")
        add_btn = ttk.Button(input_frame, text=" Добавить авто", command=self.show_add_car_popup)
        add_btn.grid(row=0, column=0, columnspan=4)

        self.tab_control = ttk.Notebook(self.root, padding=(10, 10))


    def add_expense(self, car_id):
        """Добавляет новую операцию после валидации."""
        try:
            # 1. Получаем и валидируем данные
            amount = validate_amount(self.amount_var.get())
            category = validate_category(self.category_var.get())
            date = validate_date(self.date_var.get())
            description = self.desc_var.get().strip()
            mileage = validate_amount(self.mileage_var.get())

            # 2. Создаём объект
            expense = Expense(
                car_id=car_id,
                amount=amount,
                category=category,
                date=date,
                description=description,
                mileage=mileage
            )

            # 3. Сохраняем
            save_expense(expense)

            self.refresh_car_expenses_table(car_id)
            self.expense_popup.destroy()
            messagebox.showinfo("Успех", f"Трата добавлена:\n{expense}")

        except Exception as e:
            messagebox.showerror("Ошибка ввода", f"Не удалось добавить операцию:\n{e}")

    def refresh_car_expenses_table(self, car_id):
        tree = self.cars_frames.get(car_id)['tree']
        for item in tree.get_children():
            tree.delete(item)
        transactions = load_expenses(car_id)
        # Добавляем все операции
        for t in transactions:
            tree.insert("", "end", values=(
                f"{t.amount:.2f}",
                t.category,
                t.date,
                t.mileage,
                t.description
            ))

        # Скролл вниз (к новой операции)
        tree.yview_moveto(1.0)

    def show_transaction_popup(self, car_id):
        self.expense_popup = tk.Toplevel(self.root)
        self.expense_popup.title("Добавить расход")
        self.expense_popup.geometry("340x180")

        # Сумма
        ttk.Label(self.expense_popup, text="Сумма (RUB):").grid(row=0, column=0, sticky="w", padx=(10, 10), pady=(10, 0))
        self.amount_var = tk.StringVar()
        amount_entry = ttk.Entry(self.expense_popup, textvariable=self.amount_var, width=15)
        amount_entry.grid(row=0, column=1, sticky="w")

        # Категория
        ttk.Label(self.expense_popup, text="Категория:").grid(row=1, column=0, sticky="w", padx=(10, 10), pady=(10, 0))
        self.category_var = tk.StringVar()
        category_entry = ttk.Entry(self.expense_popup, textvariable=self.category_var, width=20)
        category_entry.grid(row=1, column=1, sticky="w")

        # Дата
        ttk.Label(self.expense_popup, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, sticky="w", padx=(10, 10), pady=(10, 0))
        self.date_var = tk.StringVar(value="2025-12-23")  # подставим сегодняшнюю дату позже
        date_entry = ttk.Entry(self.expense_popup, textvariable=self.date_var, width=15)
        date_entry.grid(row=2, column=1, sticky="w", pady=(10, 0))

        # Описание
        ttk.Label(self.expense_popup, text="Описание:").grid(row=3, column=0, sticky="w", padx=(10, 10), pady=(10, 0))
        self.desc_var = tk.StringVar()
        desc_entry = ttk.Entry(self.expense_popup, textvariable=self.desc_var, width=30)
        desc_entry.grid(row=3, column=1, sticky="w", pady=(10, 0))

        # Пробег
        ttk.Label(self.expense_popup, text="Пробег (КМ):").grid(row=4, column=0, sticky="w", padx=(10, 10), pady=(10, 0))
        self.mileage_var = tk.StringVar()
        amount_entry = ttk.Entry(self.expense_popup, textvariable=self.mileage_var, width=15)
        amount_entry.grid(row=4, column=1, sticky="w")

        button = ttk.Button(self.expense_popup, text="Добавить", command=lambda car_id=car_id: self.add_expense(car_id))
        button.grid(row=5, column=0, sticky="w", padx=(10, 0), pady=(10, 0))

        self.expense_popup.grab_set()

        self.root.wait_window(self.expense_popup)

    def show_add_car_popup(self):
        self.add_car_popup = tk.Toplevel(self.root)
        self.add_car_popup.title("Добавить авто")
        self.add_car_popup.geometry("320x180")

        ttk.Label(self.add_car_popup, text="Модель:").grid(row=0, column=0, sticky="w", padx=(10, 0), pady=(10, 0))
        self.car_model_var = tk.StringVar()
        desc_entry = ttk.Entry(self.add_car_popup, textvariable=self.car_model_var, width=30)
        desc_entry.grid(row=0, column=1, sticky="w", pady=(10, 0))

        ttk.Label(self.add_car_popup, text="Стоимость (RUB):").grid(row=1, column=0, sticky="w", padx=(10, 0), pady=(10, 0))
        self.car_price_var = tk.StringVar()
        amount_entry = ttk.Entry(self.add_car_popup, textvariable=self.car_price_var, width=30)
        amount_entry.grid(row=1, column=1, sticky="w", pady=(10, 0))

        ttk.Label(self.add_car_popup, text="Пробег (КМ):").grid(row=2, column=0, sticky="w", padx=(10, 0), pady=(10, 0))
        self.car_mileage_var = tk.StringVar()
        mileage_entry = ttk.Entry(self.add_car_popup, textvariable=self.car_mileage_var, width=30)
        mileage_entry.grid(row=2, column=1, sticky="w", pady=(10, 0))

        ttk.Label(self.add_car_popup, text="Год выпуска:").grid(row=3, column=0, sticky="w", padx=(10, 0), pady=(10, 0))
        self.car_year_var = tk.StringVar()
        year_entry = ttk.Entry(self.add_car_popup, textvariable=self.car_year_var, width=30)
        year_entry.grid(row=3, column=1, sticky="w", pady=(10, 0))

        button = ttk.Button(self.add_car_popup, text="Добавить", command=self.add_car)
        button.grid(row=4, column=0, sticky="w", padx=(10, 0), pady=(10, 0))

        self.add_car_popup.grab_set()
        self.root.wait_window(self.add_car_popup)

    def add_car(self):
        car = (
            self.car_model_var.get(),
            self.car_year_var.get(),
            self.car_mileage_var.get(),
            self.car_price_var.get(),
        )

        save_car(car)
        self.refresh_cars_tabs()
        self.add_car_popup.destroy()

    def refresh_cars_tabs(self):
        self.cars_frames = {}
        for item in self.tab_control.winfo_children():
            self.tab_control.forget(item)
            item.destroy()

        cars = load_cars()
        for car in cars:
            tab = ttk.Frame(self.tab_control)
            button_delete = ttk.Button(tab, text="Удалить авто", command=lambda car_id=car.id: self.remove_car(car_id))
            button_delete.pack(pady=10)

            button_add_expense = ttk.Button(tab, text="Добавить трату", command=lambda car_id=car.id: self.show_transaction_popup(car_id))
            button_add_expense.pack(pady=10)

            self.tab_control.add(tab, text=f"{car.model} {car.year}")
            self.tab_control.pack(expand=1, fill="both")
            # === Таблица операций ===
            table_frame = ttk.LabelFrame(tab, text=" 📜 История операций ", padding=(10, 10))
            table_frame.pack(fill="both", expand=True, padx=10, pady=5)
            # Создаём Treeview (таблицу)
            columns = ("amount", "category", "date", "mileage", "description")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

            self.cars_frames[car.id] = {
                "tree": tree,
                "tab": tab
            }

            # Заголовки
            tree.heading("amount", text="Сумма (RUB)")
            tree.heading("category", text="Категория")
            tree.heading("date", text="Дата")
            tree.heading("mileage", text="Пробег (км)")
            tree.heading("description", text="Описание")

            # Ширина колонок
            tree.column("amount", width=100, anchor="e")
            tree.column("category", width=150)
            tree.column("date", width=100, anchor="center")
            tree.column("mileage", width=100, anchor="center")
            tree.column("description", width=250)

            # Полоса прокрутки
            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
            tree.configure(yscroll=scrollbar.set)

            # Размещение
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

    def remove_car(self, car_id):
        delete_car(car_id)
        self.refresh_cars_tabs()