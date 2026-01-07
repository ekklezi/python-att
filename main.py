import tkinter as tk
from gui import CarExpensesApp
from storage import init_storage

def main():
    init_storage()
    root = tk.Tk()
    app = CarExpensesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()