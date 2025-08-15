import tkinter as tk

def open_add_form_window(root, title, form_builder_callback):
    form_window = tk.Toplevel(root)
    form_window.title(title)
    form_window.geometry("600x500")
    form_window.configure(bg="#f2f2f2")
    form_window.resizable(False, False)
    form_window.transient(root)
    form_window.grab_set()

    form_window.update_idletasks()
    w, h = 600, 500
    x = (form_window.winfo_screenwidth() // 2) - (w // 2)
    y = (form_window.winfo_screenheight() // 2) - (h // 2)
    form_window.geometry(f"{w}x{h}+{x}+{y}")

    wrapper = tk.Frame(form_window, bg="#f2f2f2", padx=30, pady=30)
    wrapper.pack(fill="both", expand=True)

    form_builder_callback(wrapper, form_window)
