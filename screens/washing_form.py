import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
from base.base_form import BaseForm
from datetime import datetime

class WashingForm(BaseForm):
    def __init__(self, window, app, dashboard):
        super().__init__(window, "Add Washing Entry")
        self.master = app
        self.window = window
        self.dashboard = dashboard

        form = self.content_frame
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=2)

        
        ttk.Label(form, text="Car Type:").grid(row=0, column=0, sticky="e", padx=10, pady=(15, 2))
        self.car_type_dropdown = ttk.Combobox(form, values=[
            "Sedan", "SUV", "Truck", "Van", "Motorcycle", "Jeep", "Pickup", "Other"
        ], state="readonly")
        self.car_type_dropdown.current(0)
        self.car_type_dropdown.grid(row=0, column=1, padx=10, pady=(15, 2))
        self.car_type_error = ttk.Label(form, text="", foreground="red", background="white")
        self.car_type_error.grid(row=1, column=1, sticky="w", padx=10)

        
        self.price_label = ttk.Label(form, text=f"Price ({self.master.get_currency_label()}):")
        self.price_label.grid(row=2, column=0, sticky="e", padx=10, pady=(10, 2))
        self.price_entry = ttk.Entry(form)
        self.price_entry.grid(row=2, column=1, padx=10, pady=(10, 2))
        self.price_error = ttk.Label(form, text="", foreground="red", background="white")
        self.price_error.grid(row=3, column=1, sticky="w", padx=10)

        
        ttk.Label(form, text="Date:").grid(row=4, column=0, sticky="e", padx=10, pady=(10, 2))
        self.date_picker = DateEntry(form, date_pattern="yyyy-mm-dd")
        self.date_picker.grid(row=4, column=1, padx=10, pady=(10, 2))

        
        ttk.Button(form, text="Submit", style="Accent.TButton", command=self.submit).grid(
            row=5, column=0, columnspan=2, pady=20
        )
        
    def update_currency_label(self):
        self.price_label.config(text=f"Price ({self.master.get_currency_label()}):")

    def submit(self):
        self.car_type_error.config(text="")
        self.price_error.config(text="")

        car_type = self.car_type_dropdown.get().strip()
        price = self.price_entry.get().strip()
        date = self.date_picker.get_date()
        date = datetime.combine(date, datetime.now().time()).strftime("%Y-%m-%d %H:%M:%S")
        user = self.master.logged_in_user or "Unknown"

        valid = True

        if not car_type:
            self.car_type_error.config(text="Car type is required.")
            valid = False

        try:
            price = float(price)
        except:
            self.price_error.config(text="Price must be a number.")
            valid = False

        if not valid:
            return

        if self.master.currency_mode == "LL":
            price = price / 89000

        conn = sqlite3.connect("gas_station.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO washing (type, price, date, user) VALUES (?, ?, ?, ?)",
            (car_type, price, date, user)
        )
        conn.commit()
        conn.close()

        self.window.destroy()
        self.dashboard.refresh()
        self.master.show_frame("WashingDashboardFrame")

    def go_back(self):
        self.window.destroy()
