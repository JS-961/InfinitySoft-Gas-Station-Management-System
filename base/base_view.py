import tkinter as tk
from tkinter import ttk

class BaseView(tk.Frame):
    def __init__(self, master, title, add_button_command=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#e8edf1")  


        title_label = tk.Label(
            self, text=title, font=("Segoe UI", 22, "bold"),
            bg="#e8edf1", fg="#003366"
        )
        title_label.pack(pady=(15, 0))

        
        toolbar = tk.Frame(self, bg="#e8edf1")
        toolbar.pack(fill="x", padx=20, pady=(5, 10))

        self.back_btn = tk.Button(toolbar, text="← Back", bg="#0077cc", fg="white", relief="flat", padx=12, command=self.go_back)
        self.back_btn.pack(side="left")

        
        caller_name = self.__class__.__name__.lower()

        if "manageusers" not in caller_name:
            self.toggle_btn = tk.Button(toolbar, text="Toggle Currency", bg="#0077cc", fg="white", relief="flat", padx=12, command=self.toggle_currency)
            self.toggle_btn.pack(side="right")

        if add_button_command:
            label = "+ Add User" if "manageusers" in caller_name else "+ Add Entry"
            self.add_btn = tk.Button(toolbar, text=label, bg="#0077cc", fg="white", relief="flat", padx=12, command=add_button_command)
            self.add_btn.pack(side="right", padx=(0, 10))

        
        self.header_frame = toolbar
        self.build_header()

        
        self.content_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.build_body()

    def build_header(self):
        pass  

    def build_body(self):
        pass

    def go_back(self):
        self.master.show_frame("MenuFrame")

    def toggle_currency(self):
        self.master.currency_mode = "LL" if self.master.currency_mode == "USD" else "USD"
        if hasattr(self, "refresh"):
            self.refresh()
