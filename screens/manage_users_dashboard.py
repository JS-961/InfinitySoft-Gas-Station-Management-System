# screens/manage_users_dashboard.py

import tkinter as tk
from tkinter import ttk
import sqlite3
from base.base_view import BaseView
from tkinter import messagebox
from screens.add_user_form import AddUserForm

class ManageUsersDashboardFrame(BaseView):
    def __init__(self, master):
        super().__init__(master, "Manage Users", add_button_command=self.goto_add_user)

        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal")

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "username", "role"),
            show="headings",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        y_scroll.config(command=self.tree.yview)
        x_scroll.config(command=self.tree.xview)
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        for col in ("id", "username", "role"):
            self.tree.column(col, anchor="center", width=150)

        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Username")
        self.tree.heading("role", text="Role")

        self.tree.tag_configure("evenrow", background="#f5f5f5")
        self.tree.tag_configure("oddrow", background="white")

        self.count_label = tk.Label(self.content_frame, text="Total users: 0", font=("Segoe UI", 10, "italic"))
        self.count_label.pack(anchor="w", padx=20, pady=(0, 10))

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("gas_station.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users")
        rows = cursor.fetchall()
        conn.close()

        for i, row in enumerate(rows):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=row, tags=(tag,))

        self.count_label.config(text=f"Total users: {len(rows)}")

    def goto_add_user(self):
        if not self.master.logged_in_user or self.master.logged_in_user_role.lower() != "admin":
            messagebox.showerror("Access Denied", "Only admins can add users.")
            return

        window = tk.Toplevel(self.master)
        window.title("Add New User")
        window.geometry("750x500")
        window.configure(bg="white")
        window.resizable(False, False)
        window.transient(self.master)
        window.grab_set()

        
        window.update_idletasks()
        w, h = 750, 500
        x = (window.winfo_screenwidth() // 2) - (w // 2)
        y = (window.winfo_screenheight() // 2) - (h // 2)
        window.geometry(f"{w}x{h}+{x}+{y}")

        form = AddUserForm(window, self.master, self)
        form.pack(fill="both", expand=True)
