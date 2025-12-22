# python
import time
import pyperclip
from pynput.keyboard import Controller, Key
import threading

class ClipboardManager:
    def __init__(self, paste_delay=0.01):
        self.controller = Controller()
        self.paste_delay = paste_delay

    def paste_text(self, text, async_=True):
        def _do():
            pyperclip.copy(text)
            time.sleep(self.paste_delay)
            self.controller.press(Key.ctrl)
            self.controller.press('v')
            self.controller.release('v')
            self.controller.release(Key.ctrl)
        if async_:
            threading.Thread(target=_do, daemon=True).start()
        else:
            _do()
