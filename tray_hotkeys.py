# python
import threading
import sys
import pystray
from PIL import Image
from pynput import keyboard

class TrayHotkeys:
    def __init__(self, show_callback, quit_callback, icon_path="icon_32.png"):
        self.show_callback = show_callback
        self.quit_callback = quit_callback
        self.icon_path = icon_path

    def _create_icon(self):
        img = Image.open(self.icon_path).convert("RGBA")
        return img

    def _on_quit(self, icon, item):
        icon.stop()
        self.quit_callback()

    def _on_show(self, icon, item):
        self.show_callback()

    def start_tray(self):
        def run():
            icon = pystray.Icon(
                "MultiPaste",
                self._create_icon(),
                menu=pystray.Menu(
                    pystray.MenuItem("MultiPaste", None, enabled=False),
                    pystray.Menu.SEPARATOR,
                    pystray.MenuItem("Show", lambda icon, item: self._on_show(icon, item)),
                    pystray.MenuItem("Quit", lambda icon, item: self._on_quit(icon, item))
                )
            )
            icon.run()
        threading.Thread(target=run, daemon=True).start()

    def start_hotkeys(self):
        def run():
            with keyboard.GlobalHotKeys({
                '<ctrl>+<alt>': self.show_callback
            }) as h:
                h.join()
        threading.Thread(target=run, daemon=True).start()

    def start(self):
        self.start_tray()
        self.start_hotkeys()
