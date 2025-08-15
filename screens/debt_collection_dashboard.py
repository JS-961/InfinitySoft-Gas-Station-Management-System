import tkinter as tk
from tkinter import ttk
import sqlite3
from base.base_view import BaseView
from tkinter import messagebox
from screens.debt_collection_form import DebtCollectionForm

class DebtCollectionDashboardFrame(BaseView):
    def __init__(self, master):
        super().__init__(master, "Debt Collection", add_button_command=self.goto_add)

    def build_body(self):
        table_frame = tk.Frame(self.content_frame, bg="#e7ecf2", bd=1, relief="groove")
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal")

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "name", "amount", "date", "user"),
            show="headings",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
            style="Dashboard.Treeview"
        )

        y_scroll.config(command=self.tree.yview)
        x_scroll.config(command=self.tree.xview)
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        for col in ("id", "name", "amount", "date", "user"):
            self.tree.column(col, anchor="center", width=120)

        self.tree.tag_configure("evenrow", background="#f8f9fc")
        self.tree.tag_configure("oddrow", background="white")

        self.count_label = tk.Label(
            self.content_frame,
            text="Total records: 0",
            font=("Segoe UI", 10, "italic"),
            anchor="w"
        )
        self.count_label.pack(fill="x", padx=10, pady=(5, 10))

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("gas_station.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, amount, date, user FROM debt_collection")
        rows = cursor.fetchall()
        conn.close()

        for i, row in enumerate(rows):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            display_amount = self.master.convert_amount(row[2])
            self.tree.insert("", "end", values=(row[0], row[1], display_amount, row[3], row[4]), tags=(tag,))

        currency = self.master.get_currency_label()
        columns = [
            ("id", "ID"),
            ("name", "Name"),
            ("amount", f"Amount ({currency})"),
            ("date", "Date"),
            ("user", "User")
        ]
        for col_key, col_name in columns:
            self.tree.heading(col_key, text=col_name)

        self.count_label.config(text=f"Total records: {len(rows)}")

    def toggle_currency(self):
        self.master.currency_mode = "LL" if self.master.currency_mode == "USD" else "USD"
        self.refresh()

    def goto_add(self):
        if not self.master.logged_in_user:
            messagebox.showerror("Access Denied", "Please login first.")
            return

        window = tk.Toplevel(self.master)
        window.title("Add Debt Collection Entry")
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

        form = DebtCollectionForm(window, self.master, self)
        form.pack(fill="both", expand=True)
