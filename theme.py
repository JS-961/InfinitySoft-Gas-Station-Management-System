from tkinter import ttk


def apply_theme(root):
    style = ttk.Style(root)
    style.theme_use("default")  

    style.configure("TButton",
        background="#0078D7",
        foreground="white",
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
        padding=8
    )
    style.map("TButton",
        background=[("active", "#005a9e"), ("disabled", "#d9d9d9")],
        foreground=[("disabled", "#a3a3a3")]
    )

    style.configure("TFrame", background="#f0f2f5")

    style.configure("TLabel",
        font=("Segoe UI", 10),
        background="#f0f2f5",
        foreground="#222"
    )

    style.configure("TEntry",
        padding=5,
        font=("Segoe UI", 10)
    )

    style.configure("Header.TLabel",
        font=("Segoe UI", 16, "bold"),
        background="#003f7f",
        foreground="white",
        padding=10
    )
