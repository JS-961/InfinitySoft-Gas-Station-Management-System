import tkinter as tk
from PIL import Image, ImageTk
import threading
import time
from theme import apply_theme

# Screens
from screens.login import LoginFrame
from screens.menu import MenuFrame
from screens.expenses_dashboard import ExpensesDashboardFrame
from screens.liters_plus_dashboard import LitersPlusDashboardFrame
from screens.gas_oil_filter_dashboard import GasOilFilterDashboardFrame
from screens.statevouchers_dashboard import StateVouchersDashboardFrame
from screens.customer_vouchers_dashboard import CustomerVouchersDashboardFrame
from screens.debts_dashboard import DebtsDashboardFrame
from screens.washing_dashboard import WashingDashboardFrame
from screens.debt_collection_dashboard import DebtCollectionDashboardFrame
from screens.manage_users_dashboard import ManageUsersDashboardFrame

class SplashScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="black")
        self.master = master

        self.original_logo = Image.open("assets/logo.png").resize((100, 100))
        self.angle = 0

        self.logo_img = ImageTk.PhotoImage(self.original_logo)
        self.logo_label = tk.Label(self, image=self.logo_img, bg="black")
        self.logo_label.place(relx=0.5, rely=0.5, anchor="center")

        self.after(0, self.rotate_logo)

    def rotate_logo(self):
        self.angle = (self.angle + 10) % 360
        rotated = self.original_logo.rotate(self.angle, resample=Image.BICUBIC)
        self.logo_img = ImageTk.PhotoImage(rotated)
        self.logo_label.config(image=self.logo_img)
        self.after(40, self.rotate_logo)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gas Station Management System")
        self.state("zoomed")
        self.resizable(False, False) 
        self.currency_mode = "USD"
        self.logged_in_user = None
        self.logged_in_user_role = None
        self.frames = {}

        apply_theme(self)
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.splash = SplashScreen(self.container)
        self.splash.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.after(100, self.start_main_app)

    def start_main_app(self):
        def build_frames():
            frame_classes = [
                LoginFrame, MenuFrame,
                ExpensesDashboardFrame,
                LitersPlusDashboardFrame,
                GasOilFilterDashboardFrame,
                StateVouchersDashboardFrame,
                CustomerVouchersDashboardFrame,
                DebtsDashboardFrame,
                WashingDashboardFrame,
                DebtCollectionDashboardFrame,
                ManageUsersDashboardFrame]
            
            for FrameClass in frame_classes:
                frame = FrameClass(self)
                frame.place(relx=0, rely=0, relwidth=1, relheight=1)
                self.frames[FrameClass.__name__] = frame

            self.splash.destroy()
            self.show_frame("LoginFrame")

        threading.Thread(target=build_frames, daemon=True).start()

    def open_add_form_window(self, title, form_builder_callback):
        form_window = tk.Toplevel(self)
        form_window.title(title)
        form_window.geometry("600x500")
        form_window.configure(bg="#f2f2f2")
        form_window.resizable(False, False)
        form_window.transient(self)
        form_window.grab_set()

        form_window.update_idletasks()
        w, h = 600, 500
        x = (form_window.winfo_screenwidth() // 2) - (w // 2)
        y = (form_window.winfo_screenheight() // 2) - (h // 2)
        form_window.geometry(f"{w}x{h}+{x}+{y}")

        wrapper = tk.Frame(form_window, bg="#f2f2f2", padx=30, pady=30)
        wrapper.pack(fill="both", expand=True)

        form_builder_callback(wrapper, form_window)

    
    def show_frame(self, name):
        
        if name != "LoginFrame" and self.logged_in_user is None:
            print("Unauthorized access blocked. Redirecting to login.")
            name = "LoginFrame"
        
        frame = self.frames[name]
        if hasattr(frame, "refresh"):
            frame.refresh()
        frame.tkraise()

    def get_currency_label(self):
        return "USD" if self.currency_mode == "USD" else "L.L"

    def convert_amount(self, amount):
        return round(amount, 2) if self.currency_mode == "USD" else round(amount * 89000)


if __name__ == "__main__":
    app = App()
    app.mainloop()
