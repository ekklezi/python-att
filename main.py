import tkinter as tk
from gui import FinancialPlannerApp

def main():
    root = tk.Tk()
    app = FinancialPlannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()