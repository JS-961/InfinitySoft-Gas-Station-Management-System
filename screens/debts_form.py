import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
from base.base_form import BaseForm
from datetime import datetime

class DebtsForm(BaseForm):
    def __init__(self, window, app, dashboard):
        super().__init__(window, "Add Debt Entry")
        self.master = app
        self.window = window
        self.dashboard = dashboard

        form = self.content_frame
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=2)

        
        ttk.Label(form, text="Name:").grid(row=0, column=0, sticky="e", padx=10, pady=(15, 2))
        self.name_entry = ttk.Entry(form)
        self.name_entry.grid(row=0, column=1, padx=10, pady=(15, 2))
        self.name_error = ttk.Label(form, text="", foreground="red", background="white")
        self.name_error.grid(row=1, column=1, sticky="w", padx=10)

        
        self.amount_label = ttk.Label(form, text=f"Amount ({self.master.get_currency_label()}):")
        self.amount_label.grid(row=2, column=0, sticky="e", padx=10, pady=(10, 2))
        self.amount_entry = ttk.Entry(form)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=(10, 2))
        self.amount_error = ttk.Label(form, text="", foreground="red", background="white")
        self.amount_error.grid(row=3, column=1, sticky="w", padx=10)

        
        ttk.Label(form, text="Date:").grid(row=4, column=0, sticky="e", padx=10, pady=(10, 2))
        self.date_picker = DateEntry(form, date_pattern="yyyy-mm-dd")
        self.date_picker.grid(row=4, column=1, padx=10, pady=(10, 2))

        
        ttk.Button(form, text="Submit", style="Accent.TButton", command=self.submit).grid(
            row=5, column=0, columnspan=2, pady=20
        )

    def toggle_currency(self):
        self.master.currency_mode = "LL" if self.master.currency_mode == "USD" else "USD"
        self.amount_label.config(text=f"Amount ({self.master.get_currency_label()}):")

    def submit(self):
        self.name_error.config(text="")
        self.amount_error.config(text="")

        name = self.name_entry.get().strip()
        amount = self.amount_entry.get().strip()
        date = self.date_picker.get_date()
        date = datetime.combine(date, datetime.now().time()).strftime("%Y-%m-%d %H:%M:%S")
        user = self.master.logged_in_user or "Unknown"

        valid = True
        if not name:
            self.name_error.config(text="Name is required.")
            valid = False

        try:
            amount = float(amount)
        except:
            self.amount_error.config(text="Amount must be a number.")
            valid = False

        if not valid:
            return

        if self.master.currency_mode == "LL":
            amount = amount / 89000

        conn = sqlite3.connect("gas_station.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO debts (name, amount, date, user) VALUES (?, ?, ?, ?)",
                       (name, amount, date, user))
        conn.commit()
        conn.close()

        self.window.destroy()
        self.dashboard.refresh()
        self.master.show_frame("DebtsDashboardFrame")

    def go_back(self):
        self.window.destroy()
