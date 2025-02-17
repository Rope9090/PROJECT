import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import webbrowser
from PIL import Image, ImageTk, ImageFilter, ImageDraw, ImageFont
import datetime
import getpass
import pytz
import os
from multiprocessing import freeze_support

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Use this for all your file paths
DATA_DIR = resource_path('data/data_dlib')
TEMPLATE_DIR = resource_path('templates')

class ModernMainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System")

        # Set background image using resource_path
        try:
            bg_path = resource_path("Att.jpg")
            self.bg_image = Image.open(bg_path)
        except (FileNotFoundError, AttributeError) as e:
            self.bg_image = None
            print(f"Background image not found: {e}. Using default background color.")

        self.setup_background()
        self.root.bind("<Configure>", self.resize_background)

        # Style configuration
        self.style = ttk.Style()
        self.style.configure("TButton",
                            background="#5dade2",
                            foreground="#2c3e50",
                            font=("Arial", 12, "bold"),
                            padding=10,
                            borderwidth=0,
                            relief="flat")
        self.style.map("TButton", background=[("active", "#2e86c1")])

        self.style.configure("TLabel",
                            foreground="#2c3e50",
                            font=("Arial", 16, "bold"))

        # Title Label
        self.title_label = ttk.Label(root, text="Attendance System", style="TLabel")
        self.title_label.pack(pady=20)
        self.create_textured_overlay(self.title_label)

        # Buttons with ttk
        self.create_button("1. Capture Faces", self.run_capture_faces)
        self.create_button("2. Setup Features", self.run_features_extraction)
        self.create_button("3. Take Attendance", self.run_attendance_taker)
        self.create_button("4. Maintain Attendance", self.run_maintain_attendance)

        # Current Date and Time and User Info
        self.date_time_label = ttk.Label(root, text="", style="TLabel", font=("Arial", 10))
        self.date_time_label.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)
        self.create_textured_overlay(self.date_time_label)
        self.update_date_time()

        self.user_info_label = ttk.Label(root, text="", style="TLabel", font=("Arial", 10))
        self.user_info_label.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)
        self.create_textured_overlay(self.user_info_label)
        self.update_user_info()

        # Footer Label
        self.footer_label = ttk.Label(root, text="Developed by Rope9090", style="TLabel", font=("Arial", 10))
        self.footer_label.pack(side=tk.BOTTOM, pady=5)
        self.create_textured_overlay(self.footer_label)

    def create_button(self, text, command):
        btn = ttk.Button(self.root, text=text, command=command)
        btn.pack(pady=8, padx=20, fill="x")
        self.create_textured_overlay(btn)
        return btn

    def setup_background(self):
        if self.bg_image:
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            self.resized_bg = self.bg_image.resize((width, height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.resized_bg)

            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()

    def resize_background(self, event=None):
        if self.bg_image:
            width = event.width if event else self.root.winfo_width()
            height = event.height if event else self.root.winfo_height()
            self.resized_bg = self.bg_image.resize((width, height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.resized_bg)
            self.bg_label.config(image=self.bg_photo)

    def create_textured_overlay(self, widget, texture_alpha=128):
        widget.update_idletasks()
        x, y, width, height = widget.winfo_x(), widget.winfo_y(), widget.winfo_width(), widget.winfo_height()

        texture = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(texture)
        for i in range(width * height // 10):
            x_coord = i % width
            y_coord = i // width
            color = (100, 100, 100, texture_alpha)
            draw.point((x_coord, y_coord), fill=color)

        self.texture_photo = ImageTk.PhotoImage(texture)
        self.texture_label = tk.Label(self.root, image=self.texture_photo, borderwidth=0, highlightthickness=0)
        self.texture_label.place(x=x, y=y)
        self.texture_label.lower(widget)

    def update_date_time(self):
        ist = pytz.timezone('Asia/Kolkata')
        now_ist = datetime.datetime.now(ist)
        formatted_date_time = now_ist.strftime("%Y-%m-%d %H:%M:%S")
        self.date_time_label.config(text=f"Current Date and Time (IST): {formatted_date_time}")
        self.root.after(1000, self.update_date_time)

    def update_user_info(self):
        username = getpass.getuser()
        self.user_info_label.config(text=f"Current User's Login: {username}")

    def run_script(self, script_name):
        try:
            script_path = resource_path(script_name)
            subprocess.Popen([sys.executable, script_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start {script_name}: {str(e)}")

    def run_capture_faces(self):
        self.run_script("Capture.py")

    def run_features_extraction(self):
        self.run_script("Extract.py")

    def run_attendance_taker(self):
        self.run_script("Check.py")

    def run_maintain_attendance(self):
        try:
            self.run_script("Web.py")
            webbrowser.open("http://127.0.0.1:5000")
        except Exception as e:
            messagebox.showerror("Error", f"Could not start attendance maintenance: {e}")

if __name__ == "__main__":
    freeze_support()
    root = tk.Tk()
    root.geometry("400x400")
    app = ModernMainApp(root)
    root.mainloop()