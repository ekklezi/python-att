import tkinter as tk
from gui import FinancialPlannerApp
from storage import init_storage

def main():
    init_storage()
    root = tk.Tk()
    app = FinancialPlannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()