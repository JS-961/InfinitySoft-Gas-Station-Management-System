import tkinter as tk
from tkinter import ttk

class BaseForm(tk.Frame):
    def __init__(self, master, title="", show_nav=True, hide_currency_toggle=False):
        super().__init__(master)
        self.master = master
        self.title = title
        self.show_nav = show_nav
        self.hide_currency_toggle = hide_currency_toggle

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.draw_gradient)

        self.header = tk.Label(
            self,
            text=title,
            font=("Segoe UI", 20, "bold"),
            bg="#003f7f",
            fg="white",
            padx=20,
            pady=12
        )
        self.header.place(relx=0.5, y=0, anchor="n")

        self.form_frame = tk.Frame(self.canvas, bg="white", bd=2, relief="ridge")
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.content_frame = self.form_frame  

        if self.show_nav:
            self.back_btn = tk.Button(
                self, text="← Back", command=self.go_back,
                bg="#0077cc", fg="white"
            )
            self.back_btn.place(x=15, rely=1.0, anchor="sw", y=-15)

        if not self.hide_currency_toggle:
            self.currency_btn = tk.Button(
                self, text="Toggle Currency", command=self.toggle_currency,
                bg="#0077cc", fg="white"
            )
            self.currency_btn.place(relx=1.0, rely=1.0, anchor="se", x=-15, y=-15)

    def draw_gradient(self, event):
        self.canvas.delete("gradient")
        w, h = event.width, event.height
        r1, g1, b1 = (10, 50, 100)
        r2, g2, b2 = (100, 150, 255)

        for i in range(h):
            r = int(r1 + (r2 - r1) * i / h)
            g = int(g1 + (g2 - g1) * i / h)
            b = int(b1 + (b2 - b1) * i / h)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, w, i, fill=color, tags="gradient")

        card_w = min(500, w - 40)
        self.form_frame.place_configure(relx=0.5, rely=0.5, anchor="center", width=card_w)
        self.header.place_configure(relx=0.5, width=w)

    def toggle_currency(self):
        if hasattr(self.master, "currency_mode") and hasattr(self.master, "get_currency_label"):
            self.master.currency_mode = "LL" if self.master.currency_mode == "USD" else "USD"
            if hasattr(self, "update_currency_label"):
                self.update_currency_label()

    def go_back(self):
        if hasattr(self.master, "show_frame"):
            self.master.show_frame("MainMenuFrame")
