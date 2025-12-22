# python
import threading
from config_manager import ConfigManager
from clipboard_manager import ClipboardManager
from ui import PopupUI
from tray_hotkeys import TrayHotkeys
from pynput import keyboard

def main():
    cfg = ConfigManager()
    clip = ClipboardManager(paste_delay=0.01)
    ui = PopupUI(cfg, clip)

    tray = TrayHotkeys(show_callback=lambda: ui.safe_call(ui.show), quit_callback=lambda: ui.root.quit(), icon_path="icon_32.png")
    tray.start()

    # global key listener (for UI navigation)
    def start_global_keys():
        with keyboard.Listener(on_press=ui.handle_global_key) as listener:
            listener.join()

    threading.Thread(target=start_global_keys, daemon=True).start()

    ui.run()

if __name__ == "__main__":
    main()
