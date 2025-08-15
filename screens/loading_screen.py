import tkinter as tk
from PIL import Image, ImageTk

class LoadingScreen(tk.Frame):
    def __init__(self, master, done_callback):
        super().__init__(master, bg="#072f5f")
        self.master = master
        self.done_callback = done_callback

        self.original_logo = Image.open("assets/logo.png").resize((120, 120))
        self.angle = 0

        self.logo_img = ImageTk.PhotoImage(self.original_logo)
        self.logo_label = tk.Label(self, image=self.logo_img, bg="#072f5f")
        self.logo_label.pack(pady=(150, 10))

        self.text_label = tk.Label(self, text="Loading...", font=("Arial", 14), fg="white", bg="#072f5f")
        self.text_label.pack()

        self.animate_logo()
        self.after(200, self.start_loading)

    def animate_logo(self):
        self.angle = (self.angle + 5) % 360
        rotated = self.original_logo.rotate(self.angle, resample=Image.BICUBIC)
        self.logo_img = ImageTk.PhotoImage(rotated)
        self.logo_label.config(image=self.logo_img)
        self.after(30, self.animate_logo)

    def start_loading(self):
        self.done_callback()
