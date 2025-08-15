import tkinter as tk
import sqlite3
import os
from PIL import Image, ImageTk


class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.password_var = tk.StringVar()
        self.show_password_var = tk.IntVar()

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.canvas.bind("<Configure>", self.draw_gradient)

        
        self.app_title = tk.Label(
            self,
            text="Gas Station Management System",
            font=("Segoe UI", 22, "bold"),
            bg="#003f7f",
            fg="white",
            padx=20,
            pady=10,
        )
        self.app_title.place(relx=0.5, y=0, anchor="n")

        
        self.inner = tk.Frame(self.canvas, bg="white", bd=2, relief="ridge")
        self.inner.place(relx=0.5, rely=0.5, anchor="center")

        
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "..", "infinitysoft_logo.png")
            logo_path = os.path.abspath(logo_path)
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((80, 80), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(self.inner, image=self.logo, bg="white").pack(pady=(20, 5))
        except Exception as e:
            print(f"[DEBUG] Logo load failed: {e}")

        
        tk.Label(
            self.inner,
            text="Login",
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#003f7f"
        ).pack(pady=(5, 15))

        
        user_frame = tk.Frame(self.inner, bg="white")
        user_frame.pack(fill="x", padx=30)
        tk.Label(user_frame, text="Username", bg="white", fg="#003f7f",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.username_entry = tk.Entry(user_frame, font=("Segoe UI", 11), width=35)
        self.username_entry.pack(pady=(0, 5), fill="x")
        self.username_error_label = tk.Label(user_frame, text="", fg="red", bg="white", font=("Segoe UI", 9))
        self.username_error_label.pack(anchor="w")

        
        pass_frame = tk.Frame(self.inner, bg="white")
        pass_frame.pack(fill="x", padx=30, pady=(10, 0))
        tk.Label(pass_frame, text="Password", bg="white", fg="#003f7f",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.password_entry = tk.Entry(pass_frame, show="*", textvariable=self.password_var, font=("Segoe UI", 11), width=35)
        self.password_entry.pack(pady=(0, 5), fill="x")
        self.password_error_label = tk.Label(pass_frame, text="", fg="red", bg="white", font=("Segoe UI", 9))
        self.password_error_label.pack(anchor="w")

        
        tk.Checkbutton(
            self.inner,
            text="Show password",
            bg="white",
            variable=self.show_password_var,
            command=self.toggle_password
        ).pack(pady=(10, 5))

        
        tk.Button(
            self.inner,
            text="Login",
            bg="#0078D7",
            fg="white",
            activebackground="#005a9e",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            width=25,
            command=self.login
        ).pack(pady=(10, 25))

        self.bind_all("<Return>", lambda e: self.login())

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

        card_w = min(420, w - 40)
        self.inner.place_configure(relx=0.5, rely=0.5, anchor="center", width=card_w)
        self.app_title.place_configure(relx=0.5, width=w)

    def toggle_password(self):
        self.password_entry.config(show="" if self.show_password_var.get() else "*")

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        self.username_error_label.config(text="")
        self.password_error_label.config(text="")

        if not username:
            self.username_error_label.config(text="Username is required")
        if not password:
            self.password_error_label.config(text="Password is required")
        if not username or not password:
            return

        conn = sqlite3.connect("gas_station.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result is None:
            self.username_error_label.config(text="Username not found")
        elif result[0] != password:
            self.password_error_label.config(text="Incorrect password")
        else:
            self.master.logged_in_user = username
            self.master.logged_in_user_role = result[1]
            self.master.show_frame("MenuFrame")
