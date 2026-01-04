# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from models import Transaction
from storage import save_transaction, load_transactions, save_car, load_cars, delete_car
from utils import validate_amount, validate_date, validate_category


class FinancialPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Финансовый Планер")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)

        # Загружаем существующие операции
        self.transactions = load_transactions()

        # Создаём виджеты
        self.create_widgets()
        self.refresh_cars_tabs()

    def create_widgets(self):
        # === Верхняя панель: форма ввода ===
        input_frame = ttk.LabelFrame(self.root, text=" ➕ Новая операция ", padding=(10, 10))
        input_frame.pack(fill="x", padx=10, pady=(10, 5))

        # Сумма
        ttk.Label(input_frame, text="Сумма (RUB):").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.amount_var = tk.StringVar()
        amount_entry = ttk.Entry(input_frame, textvariable=self.amount_var, width=15)
        amount_entry.grid(row=0, column=1, sticky="w")

        # Категория
        ttk.Label(input_frame, text="Категория:").grid(row=0, column=2, sticky="w", padx=(20, 10))
        self.category_var = tk.StringVar()
        category_entry = ttk.Entry(input_frame, textvariable=self.category_var, width=20)
        category_entry.grid(row=0, column=3, sticky="w")

        # Дата
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        self.date_var = tk.StringVar(value="2025-12-23")  # подставим сегодняшнюю дату позже
        date_entry = ttk.Entry(input_frame, textvariable=self.date_var, width=15)
        date_entry.grid(row=1, column=1, sticky="w", pady=(10, 0))

        # Описание
        ttk.Label(input_frame, text="Описание:").grid(row=1, column=2, sticky="w", padx=(20, 10), pady=(10, 0))
        self.desc_var = tk.StringVar()
        desc_entry = ttk.Entry(input_frame, textvariable=self.desc_var, width=30)
        desc_entry.grid(row=1, column=3, sticky="w", pady=(10, 0))

        # Тип операции
        ttk.Label(input_frame, text="Тип:").grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.type_var = tk.StringVar(value="expense")
        expense_rb = ttk.Radiobutton(input_frame, text="Расход", variable=self.type_var, value="expense")
        income_rb = ttk.Radiobutton(input_frame, text="Доход", variable=self.type_var, value="income")
        expense_rb.grid(row=2, column=1, sticky="w", pady=(10, 0))
        income_rb.grid(row=2, column=1, sticky="w", padx=(80, 0), pady=(10, 0))

        # Кнопка "Добавить"
        # add_btn = ttk.Button(input_frame, text=" Добавить операцию", command=self.create_custom_popup)
        add_btn = ttk.Button(input_frame, text=" Добавить авто", command=self.show_add_car_popup)
        add_btn.grid(row=3, column=0, columnspan=4, pady=(15, 0))

        self.tab_control = ttk.Notebook(self.root, padding=(10, 10))


    def add_transaction(self):
        """Добавляет новую операцию после валидации."""
        try:
            # 1. Получаем и валидируем данные
            amount = validate_amount(self.amount_var.get())
            category = validate_category(self.category_var.get())
            date = validate_date(self.date_var.get())
            description = self.desc_var.get().strip()
            trans_type = self.type_var.get()

            # 2. Создаём объект
            transaction = Transaction(
                amount=amount,
                category=category,
                date=date,
                description=description,
                transaction_type=trans_type
            )

            # 3. Сохраняем
            save_transaction(transaction)
            self.transactions.append(transaction)

            # 4. Обновляем интерфейс
            self.refresh_cars_tabs()
            self.clear_input_fields()

            messagebox.showinfo("Успех", f"Операция добавлена:\n{transaction}")

        except Exception as e:
            messagebox.showerror("Ошибка ввода", f"Не удалось добавить операцию:\n{e}")

    def clear_input_fields(self):
        """Очищает поля ввода."""
        self.amount_var.set("")
        self.category_var.set("")
        self.desc_var.set("")
        # Дату можно оставить или сбросить — оставим как есть

    def refresh_transaction_table(self):
        """Обновляет таблицу операций."""
        # Очищаем текущие строки
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Добавляем все операции
        for t in self.transactions:
            row_type = "Доход" if t.transaction_type == "income" else "Расход"
            self.tree.insert("", "end", values=(
                row_type,
                f"{t.amount:.2f}",
                t.category,
                t.date,
                t.description
            ))

        # Скролл вниз (к новой операции)
        self.tree.yview_moveto(1.0)

    def show_transaction_popup(self):
        # Create a Toplevel window
        top = tk.Toplevel(self.root)
        top.title("Добавить расход")
        top.geometry("650x150")
        # === Верхняя панель: форма ввода ===
        input_frame = ttk.LabelFrame(top, text=" ➕ Новая операция ", padding=(10, 10))
        input_frame.pack(fill="x", padx=10, pady=(10, 5))

        # Сумма
        ttk.Label(input_frame, text="Сумма (RUB):").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.amount_var = tk.StringVar()
        amount_entry = ttk.Entry(input_frame, textvariable=self.amount_var, width=15)
        amount_entry.grid(row=0, column=1, sticky="w")

        # Категория
        ttk.Label(input_frame, text="Категория:").grid(row=0, column=2, sticky="w", padx=(20, 10))
        self.category_var = tk.StringVar()
        category_entry = ttk.Entry(input_frame, textvariable=self.category_var, width=20)
        category_entry.grid(row=0, column=3, sticky="w")

        # Дата
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        self.date_var = tk.StringVar(value="2025-12-23")  # подставим сегодняшнюю дату позже
        date_entry = ttk.Entry(input_frame, textvariable=self.date_var, width=15)
        date_entry.grid(row=1, column=1, sticky="w", pady=(10, 0))

        # Описание
        ttk.Label(input_frame, text="Описание:").grid(row=1, column=2, sticky="w", padx=(20, 10), pady=(10, 0))
        self.desc_var = tk.StringVar()
        desc_entry = ttk.Entry(input_frame, textvariable=self.desc_var, width=30)
        desc_entry.grid(row=1, column=3, sticky="w", pady=(10, 0))

        # Тип операции
        ttk.Label(input_frame, text="Тип:").grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.type_var = tk.StringVar(value="expense")
        expense_rb = ttk.Radiobutton(input_frame, text="Расход", variable=self.type_var, value="expense")
        income_rb = ttk.Radiobutton(input_frame, text="Доход", variable=self.type_var, value="income")
        expense_rb.grid(row=2, column=1, sticky="w", pady=(10, 0))
        income_rb.grid(row=2, column=1, sticky="w", padx=(80, 0), pady=(10, 0))
        # Make the popup modal (optional, but good practice)
        # This prevents interaction with the main window until the popup is closed
        top.grab_set()

        # Add a button to close the popup
        close_button = ttk.Button(top, text="Close", command=top.destroy)
        close_button.pack(pady=10)

        # Wait until the window is destroyed before allowing the main loop to continue (optional)
        self.root.wait_window(top)

    def show_add_car_popup(self):
        top = tk.Toplevel(self.root)
        top.title("Добавить авто")
        top.geometry("320x150")

        ttk.Label(top, text="Модель:").grid(row=0, column=0, sticky="w", padx=(20, 10), pady=(10, 0))
        self.car_model_var = tk.StringVar()
        desc_entry = ttk.Entry(top, textvariable=self.car_model_var, width=30)
        desc_entry.grid(row=0, column=1, sticky="w", pady=(10, 0))

        ttk.Label(top, text="Стоимость (RUB):").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.car_price_var = tk.StringVar()
        amount_entry = ttk.Entry(top, textvariable=self.car_price_var, width=30)
        amount_entry.grid(row=1, column=1, sticky="w", pady=(10, 0))

        ttk.Label(top, text="Пробег (КМ):").grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.car_mileage_var = tk.StringVar()
        mileage_entry = ttk.Entry(top, textvariable=self.car_mileage_var, width=30)
        mileage_entry.grid(row=2, column=1, sticky="w", pady=(10, 0))

        ttk.Label(top, text="Год выпуска:").grid(row=3, column=0, sticky="w", pady=(10, 0))
        self.car_year_var = tk.StringVar()
        year_entry = ttk.Entry(top, textvariable=self.car_year_var, width=30)
        year_entry.grid(row=3, column=1, sticky="w", pady=(10, 0))

        button = ttk.Button(top, text="Добавить", command=self.add_car)
        button.grid(row=4, column=0, sticky="w", pady=(10, 0))

    def add_car(self):
        car = (
            self.car_model_var.get(),
            self.car_year_var.get(),
            self.car_mileage_var.get(),
            self.car_price_var.get(),
        )

        save_car(car)
        self.refresh_cars_tabs()

    def refresh_cars_tabs(self):
        for item in self.tab_control.winfo_children():
            self.tab_control.forget(item)
            item.destroy()

        cars = load_cars()
        for car in cars:
            tab = ttk.Frame(self.tab_control)
            button_delete = ttk.Button(tab, text="Удалить авто", command=lambda car_id=car.id: self.remove_car(car_id))
            button_delete.pack(pady=10)
            self.tab_control.add(tab, text=f"{car.model}")
            self.tab_control.pack(expand=1, fill="both")
            # === Таблица операций ===
            table_frame = ttk.LabelFrame(tab, text=" 📜 История операций ", padding=(10, 10))
            table_frame.pack(fill="both", expand=True, padx=10, pady=5)
            # Создаём Treeview (таблицу)
            columns = ("type", "amount", "category", "date", "description")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

            # Заголовки
            tree.heading("type", text="Тип")
            tree.heading("amount", text="Сумма (RUB)")
            tree.heading("category", text="Категория")
            tree.heading("date", text="Дата")
            tree.heading("description", text="Описание")

            # Ширина колонок
            tree.column("type", width=80, anchor="center")
            tree.column("amount", width=100, anchor="e")
            tree.column("category", width=150)
            tree.column("date", width=100, anchor="center")
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