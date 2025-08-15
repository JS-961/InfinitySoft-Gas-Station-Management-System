import tkinter as tk
from screens.report_generator import ReportGenerator

class MenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#dbe9f4")
        self.master = master
        self.fade_played = False 

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.banner = tk.Label(
            self,
            text="🚗 Gas Station Management System",
            font=("Segoe UI", 22, "bold"),
            bg="#357ec7",
            fg="white",
            padx=20,
            pady=15
        )
        self.banner.grid(row=0, column=0, sticky="ew")

        
        self.content = tk.Frame(self, bg="#dbe9f4")
        self.content.grid(row=1, column=0, pady=(20, 30))
        self.content.columnconfigure(0, weight=1)

        tk.Label(
            self.content,
            text="Main Menu",
            font=("Segoe UI", 18, "bold"),
            bg="#dbe9f4",
            fg="#2c3e50"
        ).pack(pady=(5, 20))

        
        self.button_grid = tk.Frame(self.content, bg="#dbe9f4")
        self.button_grid.pack()

        
        self.logout_container = tk.Frame(self.content, bg="#dbe9f4")
        self.logout_container.pack(pady=(30, 10))

        self.fade_index = 0
        self.fade_buttons = []

    def refresh(self):
        for widget in self.button_grid.winfo_children():
            widget.destroy()
        for widget in self.logout_container.winfo_children():
            widget.destroy()

        self.fade_buttons.clear()
        self.fade_index = 0

        def on_enter(e):
            e.widget["bg"] = "#c0ddf6"
            e.widget["bd"] = 3

        def on_leave(e):
            e.widget["bg"] = e.widget.default_bg
            e.widget["bd"] = 2

        def make_button(text, command, color=None):
            btn = tk.Button(
                self.button_grid,
                text=text,
                font=("Segoe UI", 11, "bold"),
                relief="ridge",
                bd=2,
                padx=10,
                pady=15,
                bg=color or "#f0f9ff",
                fg="#000",
                activeforeground="#000",
                width=20,
                height=3,
                command=command,
                cursor="hand2"
            )
            btn.default_bg = color or "#f0f9ff"
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            self.fade_buttons.append(btn)

        buttons = [
            ("Expenses", "ExpensesDashboardFrame"),
            ("Liters Plus", "LitersPlusDashboardFrame"),
            ("Gas / Oil / Filter", "GasOilFilterDashboardFrame"),
            ("State Vouchers", "StateVouchersDashboardFrame"),
            ("Customer Vouchers", "CustomerVouchersDashboardFrame"),
            ("Debts", "DebtsDashboardFrame"),
            ("Washing", "WashingDashboardFrame"),
            ("Debt Collection", "DebtCollectionDashboardFrame"),
            ("Generate Report", lambda: ReportGenerator(self.master, self.master)),  # ✅ Corrected call
        ]

        for label, action in buttons:
            make_button(
                label,
                (lambda a=action: self.master.show_frame(a)) if isinstance(a := action, str) else a
            )

        
        if str(getattr(self.master, "logged_in_user_role", "")).lower() == "admin":
            manage_btn = tk.Button(
                self.logout_container,
                text="Manage Users",
                font=("Segoe UI", 11, "bold"),
                relief="ridge",
                bd=2,
                padx=10,
                pady=15,
                bg="#b5f5c5",
                fg="#000",
                activeforeground="#000",
                width=20,
                height=3,
                command=lambda: self.master.show_frame("ManageUsersDashboardFrame"),
                cursor="hand2"
            )
            manage_btn.default_bg = "#b5f5c5"
            manage_btn.bind("<Enter>", on_enter)
            manage_btn.bind("<Leave>", on_leave)
            manage_btn.pack(pady=(0, 20))

        
        logout_btn = tk.Button(
            self.logout_container,
            text="Logout",
            font=("Segoe UI", 11, "bold"),
            relief="ridge",
            bd=2,
            padx=10,
            pady=15,
            bg="#f56262",
            fg="white",
            activeforeground="white",
            width=20,
            height=3,
            command=self.logout,
            cursor="hand2"
        )
        logout_btn.default_bg = "#f56262"
        logout_btn.bind("<Enter>", on_enter)
        logout_btn.bind("<Leave>", on_leave)
        logout_btn.pack()

        
        if not self.fade_played:
            self.fade_played = True
            self.animate_fade_buttons_grid()
        else:
            self.render_buttons_grid()

    def animate_fade_buttons_grid(self):
        cols = 3
        if self.fade_index < len(self.fade_buttons):
            btn = self.fade_buttons[self.fade_index]
            row = self.fade_index // cols
            col = self.fade_index % cols
            btn.grid(row=row, column=col, padx=20, pady=20)
            self.fade_index += 1
            self.after(100, self.animate_fade_buttons_grid)

    def render_buttons_grid(self):
        cols = 3
        for index, btn in enumerate(self.fade_buttons):
            row = index // cols
            col = index % cols
            btn.grid(row=row, column=col, padx=20, pady=20)

    def logout(self):
        self.master.logged_in_user = None
        self.master.logged_in_user_role = None
        self.master.show_frame("LoginFrame")
