import tkinter as tk
from tkinter import ttk
import sqlite3
from base.base_view import BaseView
from tkinter import messagebox
from screens.expenses_form import ExpensesForm

class ExpensesDashboardFrame(BaseView):
    def __init__(self, master):
        super().__init__(master, "Expenses", add_button_command=self.goto_add_expense)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        font=("Segoe UI", 10),
                        background="white",
                        foreground="black",
                        rowheight=32,
                        fieldbackground="white",
                        borderwidth=0)

        style.map("Treeview",
                  background=[("selected", "#1d4ed8")],
                  foreground=[("selected", "white")])

        style.configure("Treeview.Heading",
                        font=("Segoe UI", 10, "bold"),
                        background="#0f4a8a",
                        foreground="white")

        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # clean borderless

    def build_body(self):
        card = tk.Frame(self.content_frame, bg="#e8edf5", bd=1, relief="ridge")
        card.pack(fill="both", expand=True, padx=15, pady=(10, 15))

        table_frame = tk.Frame(card, bg="#e8edf5")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal")

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "type", "amount", "date", "user"),
            show="headings",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
            style="Treeview"
        )

        y_scroll.config(command=self.tree.yview)
        x_scroll.config(command=self.tree.xview)
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        for col in ("id", "type", "amount", "date", "user"):
            self.tree.column(col, anchor="center", width=130)

        self.tree.tag_configure("evenrow", background="#f0f4fa")
        self.tree.tag_configure("oddrow", background="white")

        self.count_label = tk.Label(
            card,
            text="Total records: 0",
            font=("Segoe UI", 10, "italic"),
            bg="#e8edf5",
            anchor="w"
        )
        self.count_label.pack(fill="x", pady=(4, 5), padx=10)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("gas_station.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, type, amount, date, user FROM expenses")
        rows = cursor.fetchall()
        conn.close()

        for i, row in enumerate(rows):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            display_amount = self.master.convert_amount(row[2])
            self.tree.insert("", "end", values=(row[0], row[1], display_amount, row[3], row[4]), tags=(tag,))

        currency_label = "L.L" if self.master.currency_mode == "LL" else "USD"
        self.tree.heading("id", text="ID")
        self.tree.heading("type", text="Type")
        self.tree.heading("amount", text=f"Amount ({currency_label})")
        self.tree.heading("date", text="Date")
        self.tree.heading("user", text="User")

        self.count_label.config(text=f"Total records: {len(rows)}")

    def toggle_currency(self):
        self.master.currency_mode = "LL" if self.master.currency_mode == "USD" else "USD"
        self.refresh()

    def goto_add_expense(self):
        if not self.master.logged_in_user:
            messagebox.showerror("Access Denied", "Please login first.")
            return

        window = tk.Toplevel(self.master)
        window.title("Add Expense")
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

        form = ExpensesForm(window, self.master, self)
        form.pack(fill="both", expand=True)
