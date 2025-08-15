import tkinter as tk
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry
from base.base_form import BaseForm
from datetime import datetime

class LitersPlusForm(BaseForm):
    def __init__(self, window, app, dashboard):
        super().__init__(window, "Add Liters Plus Entry")
        self.master = app
        self.window = window
        self.dashboard = dashboard

        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=2)

        fuel_types = ["Diesel", "Octane 95", "Octane 98"]

    
        ttk.Label(self.content_frame, text="Fuel Type:").grid(row=0, column=0, sticky="e", padx=10, pady=(15, 2))
        self.type_dropdown = ttk.Combobox(self.content_frame, values=fuel_types, state="readonly")
        self.type_dropdown.current(0)
        self.type_dropdown.grid(row=0, column=1, padx=10, pady=(15, 2))
        self.type_error = ttk.Label(self.content_frame, text="", foreground="red", background="white")
        self.type_error.grid(row=1, column=1, sticky="w", padx=10)

        
        ttk.Label(self.content_frame, text="Quantity (Liters):").grid(row=2, column=0, sticky="e", padx=10, pady=(10, 2))
        self.quantity_entry = ttk.Entry(self.content_frame)
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=(10, 2))
        self.quantity_error = ttk.Label(self.content_frame, text="", foreground="red", background="white")
        self.quantity_error.grid(row=3, column=1, sticky="w", padx=10)

        
        self.price_label = ttk.Label(self.content_frame, text=f"Price ({self.master.get_currency_label()}):")
        self.price_label.grid(row=4, column=0, sticky="e", padx=10, pady=(10, 2))
        self.price_entry = ttk.Entry(self.content_frame)
        self.price_entry.grid(row=4, column=1, padx=10, pady=(10, 2))
        self.price_error = ttk.Label(self.content_frame, text="", foreground="red", background="white")
        self.price_error.grid(row=5, column=1, sticky="w", padx=10)

        
        ttk.Label(self.content_frame, text="Date:").grid(row=6, column=0, sticky="e", padx=10, pady=(10, 2))
        self.date_picker = DateEntry(self.content_frame, date_pattern="yyyy-mm-dd")
        self.date_picker.grid(row=6, column=1, padx=10, pady=(10, 2))

        
        ttk.Button(self.content_frame, text="Submit", style="Accent.TButton", command=self.submit).grid(
            row=7, column=0, columnspan=2, pady=20
        )


    def toggle_currency(self):
        self.master.currency_mode = "LL" if self.master.currency_mode == "USD" else "USD"
        self.price_label.config(text=f"Price ({self.master.get_currency_label()}):")

    def submit(self):
        self.type_error.config(text="")
        self.quantity_error.config(text="")
        self.price_error.config(text="")

        fuel_type = self.type_dropdown.get().strip()
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()
        date = self.date_picker.get_date()
        date = datetime.combine(date, datetime.now().time()).strftime("%Y-%m-%d %H:%M:%S")
        user = self.master.logged_in_user or "Unknown"

        valid = True

        if not fuel_type:
            self.type_error.config(text="Please select a fuel type.")
            valid = False

        if not quantity:
            self.quantity_error.config(text="Quantity is required.")
            valid = False
        else:
            try:
                quantity = float(quantity)
            except ValueError:
                self.quantity_error.config(text="Quantity must be a number.")
                valid = False

        if not price:
            self.price_error.config(text="Price is required.")
            valid = False
        else:
            try:
                price = float(price)
            except ValueError:
                self.price_error.config(text="Price must be a number.")
                valid = False

        if not valid:
            return

        if self.master.currency_mode == "LL":
            price = price / 89000

        conn = sqlite3.connect("gas_station.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO liters_plus (type, quantity, price, date, user) VALUES (?, ?, ?, ?, ?)",
            (fuel_type, quantity, price, date, user)
        )
        conn.commit()
        conn.close()

        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.date_picker.set_date(datetime.now())
        
        self.window.destroy()
        self.dashboard.refresh()
        self.master.show_frame("LitersPlusDashboardFrame")

    def go_back(self):
        self.window.destroy()

