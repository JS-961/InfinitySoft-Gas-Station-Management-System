import os
import sqlite3
import platform
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from utils.pdf_exporter import generate_full_report_pdf

DB_PATH = "gas_station.db"

class ReportGenerator:
    def __init__(self, parent, app):
        self.app = app
        self.window = tk.Toplevel(parent)
        self.window.title("Generate Full Report — الجردة اليومية")
        self.window.state("zoomed")
        self.window.resizable(False, False)
        self.window.configure(bg="#e7ecf2")

        self.from_date = tk.StringVar()
        self.to_date = tk.StringVar()
        self.generated_range = ("", "")
        self.generated_data = {}
        self.jarde_rows = []

        self._build_ui()

        today = datetime.now().strftime("%Y-%m-%d")
        self.from_date.set(today)
        self.to_date.set(today)
        try:
            self.from_picker.set_date(datetime.now())
            self.to_picker.set_date(datetime.now())
        except Exception:
            pass

        self.generate_report(auto_init=True)

    # ---------- UI ----------
    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        font=("Segoe UI", 10),
                        background="white",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="white",
                        borderwidth=0)
        style.map("Treeview",
                  background=[("selected", "#1d4ed8")],
                  foreground=[("selected", "white")])
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 10, "bold"),
                        background="#0f4a8a",
                        foreground="white")
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        
        header = tk.Label(
            self.window,
            text="🧾 Generate Full Report / تقرير شامل — الجردة اليومية",
            font=("Segoe UI", 18, "bold"),
            bg="#357ec7",
            fg="black",  
            pady=12
        )
        header.pack(fill="x")

        form_frame = tk.Frame(self.window, bg="#e7ecf2")
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="From:", font=("Segoe UI", 11), background="#e7ecf2").grid(row=0, column=0, padx=5)
        self.from_picker = DateEntry(form_frame, textvariable=self.from_date, width=12, date_pattern="yyyy-mm-dd")
        self.from_picker.grid(row=0, column=1, padx=5)

        ttk.Label(form_frame, text="To:", font=("Segoe UI", 11), background="#e7ecf2").grid(row=0, column=2, padx=5)
        self.to_picker = DateEntry(form_frame, textvariable=self.to_date, width=12, date_pattern="yyyy-mm-dd")
        self.to_picker.grid(row=0, column=3, padx=5)

        self.generate_btn = self._styled_button(form_frame, "Generate", self.generate_report)
        self.generate_btn.grid(row=0, column=4, padx=30)

        preview_container = tk.Frame(self.window, bg="#e7ecf2")
        preview_container.pack(fill="both", expand=True, padx=30, pady=(5, 10))

        self.canvas = tk.Canvas(preview_container, bg="white", bd=2, relief="solid")
        scrollbar = ttk.Scrollbar(preview_container, orient="vertical", command=self.canvas.yview)
        self.report_frame = tk.Frame(self.canvas, bg="white")

        self.report_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.report_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.empty_label = tk.Label(
            self.canvas,
            text="no transactions made today, try filtering by date",
            font=("Segoe UI", 11, "bold"),
            fg="#b91c1c",
            bg="white"
        )

        self.print_btn = self._styled_button(self.window, "Print to PDF", self.export_pdf)
        self.print_btn.pack_forget()

    def _styled_button(self, parent, text, command):
        btn = tk.Button(
            parent, text=text, font=("Segoe UI", 11, "bold"),
            relief="ridge", bd=2, padx=10, pady=10,
            bg="#f0f9ff", fg="#000", activeforeground="#000",
            width=15, height=2, command=command, cursor="hand2"
        )
        btn.default_bg = "#f0f9ff"
        btn.bind("<Enter>", lambda e: e.widget.config(bg="#c0ddf6", bd=3))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=e.widget.default_bg, bd=2))
        return btn

    # ---------- DATA + RENDER ----------
    def generate_report(self, auto_init: bool = False):
        from_date = self.from_date.get()
        to_date = self.to_date.get()
        self.generated_range = (from_date, to_date)

        self.generated_data = self.fetch_sections(from_date, to_date)

        today = datetime.now().strftime("%Y-%m-%d")
        self.jarde_rows = self.compute_jarde_for_today(today)

        for w in self.report_frame.winfo_children():
            w.destroy()
        self.empty_label.place_forget()

        tk.Label(
            self.report_frame,
            text=f"Currency in Use: {self.app.currency_mode}",
            font=("Segoe UI", 11, "bold"),
            bg="white", fg="#0f4a8a", anchor="w"
        ).pack(anchor="w", padx=10, pady=(10, 0))

        has_any_section = bool(self.generated_data)
        has_any_jarde_value = any(
            (isinstance(v, (int, float)) and abs(v) > 1e-9) for _, v in self.jarde_rows
        )

        if not has_any_section and not has_any_jarde_value:
            self.empty_label.place(relx=0.5, rely=0.5, anchor="center")
            self.print_btn.pack_forget()
            return

        for section, table_data in self.generated_data.items():
            tk.Label(
                self.report_frame, text=section, font=("Segoe UI", 12, "bold"),
                bg="white", fg="black", anchor="w"
            ).pack(anchor="w", padx=10, pady=(15, 5))

            cols = table_data[0]
            wrapper = tk.Frame(self.report_frame, bg="white")
            wrapper.pack(fill="x", expand=True, padx=20, pady=5)

            tree = ttk.Treeview(wrapper, columns=cols, show="headings",
                                height=min(max(len(table_data) - 1, 1), 10), style="Treeview")

            col_width = max(int(self.window.winfo_width() / max(len(cols), 1)) - 60, 120)
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=col_width, stretch=True)

            tree.tag_configure("evenrow", background="#f0f4fa")
            tree.tag_configure("oddrow", background="white")

            for i, row in enumerate(table_data[1:]):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                formatted = []
                for val in row:
                    try:
                        num = float(val); formatted.append(f"{num:.3f}")
                    except:
                        formatted.append(val)
                tree.insert("", "end", values=formatted, tags=(tag,))
            tree.pack(fill="both", expand=True)

            summary_frame = tk.Frame(self.report_frame, bg="white")
            summary_frame.pack(fill="x", padx=20, pady=(0, 5))
            summary_text = ""
            for i, col in enumerate(cols):
                try:
                    values = [float(r[i]) for r in table_data[1:] if str(r[i]).replace('.', '', 1).isdigit()]
                    if values: summary_text += f"{col} Total: {round(sum(values), 3)}    "
                except: pass
            if summary_text.strip():
                tk.Label(summary_frame, text=summary_text.strip(), font=("Segoe UI", 10, "bold"),
                         bg="white", fg="#0f4a8a", anchor="w", justify="left").pack(anchor="w")

        # ----- الجردة اليومية (bilingual) -----
        tk.Label(
            self.report_frame,
            text="Daily Inventory / الجردة اليومية",
            font=("Segoe UI", 13, "bold"),
            bg="white", fg="black", anchor="w"
        ).pack(anchor="w", padx=10, pady=(18, 6))

        wrapper = tk.Frame(self.report_frame, bg="white")
        wrapper.pack(fill="x", expand=True, padx=20, pady=(0, 12))

        cols = ["Item / البند", "Value / القيمة"]
        jtree = ttk.Treeview(wrapper, columns=cols, show="headings", height=len(self.jarde_rows), style="Treeview")


        self.canvas.update_idletasks()
        total_w = max(self.canvas.winfo_width() - 110, 520)  
        col_w = total_w // 2

        for col in cols:
            jtree.heading(col, text=col)
            jtree.column(col, anchor="center", width=col_w, stretch=True)

        jtree.tag_configure("evenrow", background="#f0f4fa")
        jtree.tag_configure("oddrow", background="white")

        for i, (label, val) in enumerate(self.jarde_rows):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            display_val = f"{val:.3f}" if isinstance(val, (int, float)) else (val or "")
            jtree.insert("", "end", values=[label, display_val], tags=(tag,))
        jtree.pack(fill="x", expand=True)

        self.print_btn.pack(pady=10)

    # ---------- QUERIES ----------
    def _sum_between(self, cursor, table, column, start_dt, end_dt, date_col="date", where_extra=""):
        query = f"SELECT SUM({column}) FROM {table} WHERE {date_col} >= ? AND {date_col} < ? {where_extra}"
        cursor.execute(query, (start_dt, end_dt))
        r = cursor.fetchone()
        return float(r[0]) if r and r[0] is not None else 0.0

    def column_exists(self, cursor, table, column):
        cursor.execute(f"PRAGMA table_info({table})")
        return any(row[1] == column for row in cursor.fetchall())

    def compute_jarde_for_today(self, yyyy_mm_dd: str):
        """
        Hardcoded 'الجردة اليومية' rows.
        Today window = [YYYY-MM-DD 00:00:00, next_day 00:00:00)
        """
        start = f"{yyyy_mm_dd} 00:00:00"
        end_dt = (datetime.strptime(yyyy_mm_dd, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # Fuel placeholders (0.000 until wired pump tables)
        gas_sales = 0.0
        diesel_sales = 0.0
        fuel_total = gas_sales + diesel_sales

        washing_total = self._sum_between(cur, "washing", "price", start, end_dt)
        gof_total = self._sum_between(cur, "gas_oil_filter", "price", start, end_dt)
        liters_total = self._sum_between(cur, "liters_plus", "price", start, end_dt)
        debt_collection = self._sum_between(cur, "debt_collection", "amount", start, end_dt)
        expenses_total = self._sum_between(cur, "expenses", "amount", start, end_dt)
        new_debts_total = self._sum_between(cur, "debts", "amount", start, end_dt)

        state_qty = self._sum_between(cur, "state_vouchers", "quantity", start, end_dt)
        state_diff = self._sum_between(cur, "state_vouchers", "difference", start, end_dt)

        cust_qty = self._sum_between(cur, "customer_vouchers", "quantity", start, end_dt)
        cust_diff = 0.0
        try:
            if self.column_exists(cur, "customer_vouchers", "difference"):
                cust_diff = self._sum_between(cur, "customer_vouchers", "difference", start, end_dt)
        except Exception:
            cust_diff = 0.0

        vouchers_diff_both = state_diff + cust_diff

        cash_total = (debt_collection + washing_total + gof_total + liters_total + vouchers_diff_both) - expenses_total

        conn.close()

        rows = [
            ("Gasoline Sales / مبيع بنزين", gas_sales),
            ("Diesel Sales / مبيع مازوت", diesel_sales),
            ("Fuel Total / مجموع محروقات", fuel_total),

            ("Washing Total / مجموع غسيل", washing_total),
            ("Oil + Gas Total / مجموع زيت + غاز", gof_total),
            ("Liters Plus / ليترز بلاس", liters_total),

            ("Customer Vouchers (Quantity) / بونات زبائن (Quantity)", cust_qty),
            ("State Vouchers (Quantity) / بونات دولة (Quantity)", state_qty),

            ("Debt Collection / تحصيل ديون", debt_collection),
            ("Voucher Difference (State + Customer) / فرق بونات (State + Customer)", vouchers_diff_both),

            ("Expenses / مصاريف", expenses_total),
            ("New Debts / ديون", new_debts_total),

            ("Cash Total / مجموع نقدي", cash_total),
        ]
        return rows

    def fetch_sections(self, from_date, to_date):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        sections = {}

        def fetch(query, headers, label, arabic_label):
            cursor.execute(query, (from_date, to_date))
            rows = cursor.fetchall()
            if rows:
                sections[f"{label} / {arabic_label}"] = [headers] + [list(r) for r in rows]

        fetch("SELECT type, price, date FROM washing WHERE date BETWEEN ? AND ?",
              ["Type", "Price", "Date"], "Washing", "الغسيل")

        fetch("SELECT type, quantity, difference, date FROM state_vouchers WHERE date BETWEEN ? AND ?",
              ["Type", "Qty", "Difference", "Date"], "State Vouchers", "بونات دولة")

        fetch("SELECT name, amount, date FROM debts WHERE date BETWEEN ? AND ?",
              ["Name", "Amount", "Date"], "Debts", "الديون")

        fetch("SELECT name, amount, date FROM debt_collection WHERE date BETWEEN ? AND ?",
              ["Name", "Amount", "Date"], "Debt Collection", "تحصيل ديون")

        fetch("SELECT name, quantity, price, date FROM customer_vouchers WHERE date BETWEEN ? AND ?",
              ["Name", "Qty", "Price", "Date"], "Customer Vouchers", "بونات زبائن")

        fetch("SELECT type, quantity, price, date FROM liters_plus WHERE date BETWEEN ? AND ?",
              ["Type", "Qty", "Price", "Date"], "Liters Plus", "ليترز بلاس")

        fetch("SELECT type, quantity, price, date FROM gas_oil_filter WHERE date BETWEEN ? AND ?",
              ["Type", "Qty", "Price", "Date"], "Gas/Oil/Filter", "فلتر/زيت/غاز")

        fetch("SELECT type, amount, date FROM expenses WHERE date BETWEEN ? AND ?",
              ["Type", "Amount", "Date"], "Expenses", "مصاريف")

        conn.close()
        return sections

    # ---------- PDF ----------
    def export_pdf(self):
        today = datetime.now().strftime("%Y-%m-%d")
        jarde_rows = self.compute_jarde_for_today(today)

        if not (self.generated_data or any(isinstance(v, (int, float)) and abs(v) > 1e-9 for _, v in jarde_rows)):
            messagebox.showinfo("Nothing to export", "No records for this range and today's jarde is empty.")
            return

        reports_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(reports_dir, exist_ok=True)

        filename = f"Full_Report_{self.generated_range[0]}_to_{self.generated_range[1]}.pdf"
        save_path = os.path.join(reports_dir, filename)

        logo_path = os.path.join("assets", "logo.png")
        generate_full_report_pdf(
            data_dict=self.generated_data,
            from_date=self.generated_range[0],
            to_date=self.generated_range[1],
            logo_path=logo_path,
            save_path=save_path,
            generated_by=self.app.logged_in_user,
            currency_mode=self.app.currency_mode,
            jarde_rows=jarde_rows
        )

        messagebox.showinfo("PDF Exported", f"Report saved to: {save_path}")
        try:
            if platform.system() == "Windows":
                os.startfile(save_path)
            elif platform.system() == "Darwin":
                os.system(f"open '{save_path}'")
            else:
                os.system(f"xdg-open '{save_path}'")
        except Exception as e:
            print("Could not open file:", e)
