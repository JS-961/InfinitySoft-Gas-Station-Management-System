import tkinter as tk
from tkinter import ttk
import sqlite3
from base.base_form import BaseForm

class AddUserForm(BaseForm):
    def __init__(self, window, app, dashboard):
        super().__init__(window, "Add New User", hide_currency_toggle=True)  # 👈 key change
        self.master = app
        self.window = window
        self.dashboard = dashboard

        form = self.content_frame
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=2)

        
        ttk.Label(form, text="Username:").grid(row=0, column=0, sticky="e", padx=10, pady=(15, 2))
        self.username_entry = ttk.Entry(form)
        self.username_entry.grid(row=0, column=1, padx=10, pady=(15, 2))
        self.username_error = ttk.Label(form, text="", foreground="red", background="white")
        self.username_error.grid(row=1, column=1, sticky="w", padx=10)

        
        ttk.Label(form, text="Password:").grid(row=2, column=0, sticky="e", padx=10, pady=(10, 2))
        self.password_entry = ttk.Entry(form, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=(10, 2))
        self.password_error = ttk.Label(form, text="", foreground="red", background="white")
        self.password_error.grid(row=3, column=1, sticky="w", padx=10)

        
        ttk.Label(form, text="Role:").grid(row=4, column=0, sticky="e", padx=10, pady=(10, 2))
        self.role_dropdown = ttk.Combobox(form, values=["Admin", "Employee"], state="readonly")
        self.role_dropdown.current(0)
        self.role_dropdown.grid(row=4, column=1, padx=10, pady=(10, 2))
        self.role_error = ttk.Label(form, text="", foreground="red", background="white")
        self.role_error.grid(row=5, column=1, sticky="w", padx=10)

        
        ttk.Button(form, text="Add User", style="Accent.TButton", command=self.submit).grid(
            row=6, column=0, columnspan=2, pady=20
        )

        
        self.back_btn = ttk.Button(self, text="← Back", command=self.go_back)
        self.back_btn.place(x=15, rely=1.0, anchor="sw", y=-15)

    def submit(self):
        self.username_error.config(text="")
        self.password_error.config(text="")
        self.role_error.config(text="")

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_dropdown.get().strip().lower()

        valid = True

        if not username:
            self.username_error.config(text="Username is required.")
            valid = False
        if not password:
            self.password_error.config(text="Password is required.")
            valid = False
        if not role:
            self.role_error.config(text="Role must be selected.")
            valid = False

        if not valid:
            return

        conn = sqlite3.connect("gas_station.db")
        cursor = conn.cursor()

        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            self.username_error.config(text="Username already exists.")
            conn.close()
            return

    
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, password, role))
        conn.commit()
        conn.close()

        self.window.destroy()
        self.dashboard.refresh()
        self.master.show_frame("ManageUsersDashboardFrame")

    def go_back(self):
        self.window.destroy()
