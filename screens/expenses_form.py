import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from base.base_form import BaseForm
from datetime import datetime
import sqlite3

EXCHANGE_RATE_LL_TO_USD = 89000.0  

class ExpensesForm(BaseForm):
    def __init__(self, window, app, dashboard):
        super().__init__(window, "Add Expense")

        self.app = app
        self.window = window
        self.dashboard = dashboard

        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=2)

        ttk.Label(self.content_frame, text="Type:").grid(row=0, column=0, sticky="e", padx=15, pady=(20, 5))
        self.type_dropdown = ttk.Combobox(
            self.content_frame,
            values=["Fuel", "Maintenance", "Office Supplies"],
            state="readonly"
        )
        self.type_dropdown.current(0)
        self.type_dropdown.grid(row=0, column=1, padx=15, pady=(20, 5), sticky="we")

        
        ttk.Label(self.content_frame, text=f"Amount ({self._currency_label()}):").grid(row=1, column=0, sticky="e", padx=15, pady=5)
        self.amount_entry = ttk.Entry(self.content_frame)
        self.amount_entry.grid(row=1, column=1, padx=15, pady=5, sticky="we")
        self.amount_error = ttk.Label(self.content_frame, text="", foreground="red", background="white")
        self.amount_error.grid(row=2, column=1, sticky="w", padx=15)

        ttk.Label(self.content_frame, text="Date:").grid(row=3, column=0, sticky="e", padx=15, pady=5)
        self.date_picker = DateEntry(self.content_frame, date_pattern="yyyy-mm-dd")
        self.date_picker.grid(row=3, column=1, padx=15, pady=5, sticky="we")

        ttk.Button(self.content_frame, text="Submit", command=self.submit).grid(
            row=4, column=0, columnspan=2, pady=20
        )

    def _currency_label(self):
        try:
            return self.app.get_currency_label()
        except AttributeError:
            mode = getattr(self.app, "currency_mode", "USD")
            return "L.L" if mode == "LL" else "USD"

    def toggle_currency(self):
        current = getattr(self.app, "currency_mode", "USD")
        setattr(self.app, "currency_mode", "LL" if current == "USD" else "USD")
        self._update_currency_label()

    def _update_currency_label(self):
        self.content_frame.grid_slaves(row=1, column=0)[0].config(
            text=f"Amount ({self._currency_label()}):"
        )

    def submit(self):
        self.amount_error.config(text="")

        amount_text = self.amount_entry.get().strip()
        expense_type = self.type_dropdown.get().strip()
        date = self.date_picker.get_date()
        date = datetime.combine(date, datetime.now().time()).strftime("%Y-%m-%d %H:%M:%S")
        user = getattr(self.app, "logged_in_user", None) or "Unknown"

        if not amount_text:
            self.amount_error.config(text="Amount is required.")
            return
        try:
            amount = float(amount_text)
        except ValueError:
            self.amount_error.config(text="Amount must be a number.")
            return

        
        if getattr(self.app, "currency_mode", "USD") == "LL":
            amount = amount / EXCHANGE_RATE_LL_TO_USD

        
        try:
            conn = self.app.get_db_connection()
        except AttributeError:
            conn = sqlite3.connect("gas_station.db")

        cur = conn.cursor()
        cur.execute(
            "INSERT INTO expenses (type, amount, date, user) VALUES (?, ?, ?, ?)",
            (expense_type, amount, date, user)
        )
        conn.commit()
        conn.close()

    
        self.amount_entry.delete(0, tk.END)
        self.date_picker.set_date(datetime.now())
        self.window.destroy()
        self.dashboard.refresh()
        
        if hasattr(self.app, "show_frame"):
            self.app.show_frame("ExpensesDashboardFrame")

    def go_back(self):
        self.window.destroy()
