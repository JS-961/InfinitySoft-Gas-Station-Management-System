import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
from base.base_form import BaseForm
from datetime import datetime

class StateVouchersForm(BaseForm):
    def __init__(self, window, app, dashboard):
        super().__init__(window, "Add State Voucher")
        self.master = app
        self.window = window
        self.dashboard = dashboard

        self.voucher_types = ["Morning", "Evening", "Night Shift", "Other"]

        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=2)

    
        ttk.Label(self.content_frame, text="Type:").grid(row=0, column=0, sticky="e", padx=10, pady=(15, 2))
        self.type_dropdown = ttk.Combobox(self.content_frame, values=self.voucher_types, state="readonly")
        self.type_dropdown.current(0)
        self.type_dropdown.grid(row=0, column=1, padx=10, pady=(15, 2))
        self.type_error = ttk.Label(self.content_frame, text="", foreground="red", background="white")
        self.type_error.grid(row=1, column=1, sticky="w", padx=10)

        
        ttk.Label(self.content_frame, text="Quantity (Liters):").grid(row=2, column=0, sticky="e", padx=10, pady=(10, 2))
        self.quantity_entry = ttk.Entry(self.content_frame)
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=(10, 2))
        self.quantity_error = ttk.Label(self.content_frame, text="", foreground="red", background="white")
        self.quantity_error.grid(row=3, column=1, sticky="w", padx=10)

        
        self.price_label = ttk.Label(self.content_frame, text=f"Difference ({self.master.get_currency_label()}):")
        self.price_label.grid(row=4, column=0, sticky="e", padx=10, pady=(10, 2))
        self.difference_entry = ttk.Entry(self.content_frame)
        self.difference_entry.grid(row=4, column=1, padx=10, pady=(10, 2))
        self.difference_error = ttk.Label(self.content_frame, text="", foreground="red", background="white")
        self.difference_error.grid(row=5, column=1, sticky="w", padx=10)

        
        ttk.Label(self.content_frame, text="Date:").grid(row=6, column=0, sticky="e", padx=10, pady=(10, 2))
        self.date_picker = DateEntry(self.content_frame, date_pattern="yyyy-mm-dd")
        self.date_picker.grid(row=6, column=1, padx=10, pady=(10, 2))

        
        ttk.Button(self.content_frame, text="Submit", style="Accent.TButton", command=self.submit).grid(
            row=7, column=0, columnspan=2, pady=20
        )

    def toggle_currency(self):
        self.master.currency_mode = "LL" if self.master.currency_mode == "USD" else "USD"
        self.price_label.config(text=f"Difference ({self.master.get_currency_label()}):")

    def submit(self):
        self.type_error.config(text="")
        self.quantity_error.config(text="")
        self.difference_error.config(text="")

        type_val = self.type_dropdown.get().strip()
        quantity = self.quantity_entry.get().strip()
        difference = self.difference_entry.get().strip()
        date = self.date_picker.get_date()
        date = datetime.combine(date, datetime.now().time()).strftime("%Y-%m-%d %H:%M:%S")
        user = self.master.logged_in_user or "Unknown"

        valid = True

        if not type_val:
            self.type_error.config(text="Please select a type.")
            valid = False

        try:
            quantity = float(quantity)
        except:
            self.quantity_error.config(text="Quantity must be a number.")
            valid = False

        try:
            difference = float(difference)
        except:
            self.difference_error.config(text="Difference must be a number.")
            valid = False

        if not valid:
            return

        if self.master.currency_mode == "LL":
            difference = difference / 89000

        conn = sqlite3.connect("gas_station.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO state_vouchers (type, quantity, difference, date, user) VALUES (?, ?, ?, ?, ?)",
            (type_val, quantity, difference, date, user)
        )
        conn.commit()
        conn.close()

        self.window.destroy()
        self.dashboard.refresh()
        self.master.show_frame("StateVouchersDashboardFrame")

    def go_back(self):
        self.window.destroy()
        self.master.show_frame("StateVouchersDashboardFrame")
