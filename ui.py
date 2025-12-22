# python
import tkinter as tk
from tkinter import simpledialog
import threading

from pynput import keyboard
from pynput.mouse import Controller as MouseController
# import constants used previously or redefine a small set here
BG = "#1f1f1f"
CARD = "#2b2b2b"
HEADER = "#323232"
BTN = "#3a3a3a"
BTN_HOVER = "#505050"
TEXT = "#e6e6e6"
TEXT_MUTED = "#9a9a9a"
BORDER = "#3f3f3f"
FONT_MAIN = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 8)
COLUMNS = 3

def get_mouse_position():
    """
    Zwraca (x, y) pozycji myszy.
    Controller nie wspiera context managera, więc tworzymy instancję i pobieramy .position.
    W razie błędu zwracamy bezpieczną pozycję (0, 0).
    """
    try:
        return MouseController().position
    except Exception:
        return (0, 0)

class PopupUI:
    def __init__(self, config_manager, clipboard_manager):
        self.config_manager = config_manager
        self.clipboard = clipboard_manager

        self.root = tk.Tk()
        self.root.title("MultiPaste")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.92)
        self.root.configure(bg=BG)
        self.root.withdraw()

        self.selected_index = 0
        self.buttons = []
        self.persistent_mode = tk.BooleanVar(value=False)

        self.root.bind("<Left>", lambda e: self.move_selection(-1, 0))
        self.root.bind("<Right>", lambda e: self.move_selection(1, 0))
        self.root.bind("<Up>", lambda e: self.move_selection(0, -1))
        self.root.bind("<Down>", lambda e: self.move_selection(0, 1))
        self.root.bind("<Escape>", lambda e: self.on_escape())
        self.root.bind("<Return>", self.paste_selected)

        self.config_var = tk.StringVar(value=self.config_manager.get_active())
        self.editor_open = False
        self.editor_window = None

        # layout...
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(padx=4, pady=4)
        container = tk.Frame(outer, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        container.pack(fill="both", expand=True)

        header = tk.Frame(container, bg=HEADER, height=28)
        header.pack(fill="x")
        tk.Label(header, text="MultiPaste", bg=HEADER, fg=TEXT_MUTED, font=("Segoe UI", 9, "bold")).pack(side="left", padx=8)
        tk.Label(header, text="Choose what to paste • ESC to exit", bg=HEADER, fg=TEXT_MUTED, font=FONT_SMALL).pack(side="left")
        tk.Label(header, text="Made by: Łukasz Rotko", bg=HEADER, fg=TEXT_MUTED, font=FONT_SMALL).pack(side="right", padx=8)
        gear = tk.Label(header, text="⚙", bg=HEADER, fg=TEXT_MUTED, font=("Segoe UI", 11), cursor="hand2")
        gear.pack(side="right", padx=6)
        gear.bind("<Button-1>", lambda e: self.open_editor())

        tk.Checkbutton(header, text="Persistent", variable=self.persistent_mode, bg=HEADER, fg=TEXT_MUTED, selectcolor=HEADER, font=FONT_SMALL, relief="flat", highlightthickness=0).pack(side="right", padx=8)

        # config menu (simplified)
        configs = self.config_manager.list_configs()
        config_menu = tk.OptionMenu(header, self.config_var, *configs, command=self.on_config_change)
        config_menu.config(bg=HEADER, fg=TEXT_MUTED, font=FONT_SMALL, highlightthickness=0)
        config_menu.pack(side="right", padx=6)

        # scrollable list
        self.canvas = tk.Canvas(container, bg=CARD, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.list_frame = tk.Frame(self.canvas, bg=CARD)
        self.list_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # search
        self.search_var = tk.StringVar()
        search_frame = tk.Frame(container, bg=CARD)
        search_frame.pack(fill="x", padx=6, pady=6)
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, bg=CARD, fg=TEXT_MUTED, insertbackground=TEXT, relief="flat", font=FONT_MAIN)
        self.search_entry.pack(fill="x", ipady=6)
        self.search_entry.insert(0, "Search here...")
        self.search_entry.bind("<KeyRelease>", self.on_search_key)
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.restore_placeholder)

        # data
        self.data = self.config_manager.load_active()
        self.filtered_keys = list(self.data.keys())
        self.render_buttons()

    def on_config_change(self, name):
        self.config_manager.set_active_config(name)
        self.data = self.config_manager.load_active_config()
        self.update_list()

    def open_editor(self):
        if self.editor_open:
            return

        self.editor_window = self.config_manager.ConfigEditor(self)
        self.editor_open = True

    def safe_call(self, fn, *args):
        self.root.after(0, lambda: fn(*args))

    # ---------- Buttons ----------
    def on_search_key(self, event):
        # ignoruj klawisze nawigacyjne
        if event.keysym in ("Up", "Down", "Left", "Right", "Return", "Escape"):
            return
        self.update_list()

    def create_button(self, parent, text, command):
        btn = tk.Label(
            parent,
            text=text,
            bg=BTN,
            fg=TEXT,
            font=FONT_MAIN,
            padx=8,
            pady=5,
            anchor="w"
        )

        def on_enter(e):
            if btn != self.buttons[self.selected_index]:
                btn.config(bg="#444444")

        def on_leave(e):
            self.update_selection()

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", lambda e: command())

        return btn

    def move_selection(self, dx, dy):
        if not self.buttons:
            return

        cols = COLUMNS
        rows = (len(self.buttons) - 1) // cols + 1

        row = self.selected_index // cols
        col = self.selected_index % cols

        new_row = max(0, min(rows - 1, row + dy))
        new_col = max(0, min(cols - 1, col + dx))

        new_index = new_row * cols + new_col

        if new_index < len(self.buttons):
            self.selected_index = new_index
            self.update_selection()
            self.scroll_to_selection()

    def scroll_to_selection(self):
        btn = self.buttons[self.selected_index]
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(btn.winfo_y() / self.list_frame.winfo_height())

    def paste_selected(self, event=None):
        if not self.buttons:
            return

        key = self.filtered_keys[self.selected_index]
        self.use_value(self.data[key])

    def update_selection(self):
        if not self.buttons or self.selected_index >= len(self.buttons):
            return

        for i, btn in enumerate(self.buttons):
            if i == self.selected_index:
                btn.config(
                    bg="#5a5a5a",
                    highlightthickness=2,
                    highlightbackground="#6ea0ff"
                )
            else:
                btn.config(
                    bg=BTN,
                    highlightthickness=0
                )

    def render_buttons(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        visible = self.filtered_keys

        self.buttons = []

        for i, key in enumerate(visible):
            row = i // COLUMNS
            col = i % COLUMNS

            btn = self.create_button(
                self.list_frame,
                key,
                lambda v=self.data[key]: self.use_value(v)
            )

            btn.grid(row=row, column=col, sticky="nsew", padx=6, pady=4)
            self.buttons.append(btn)

        self.update_selection()

        # make columns expand evenly
        for c in range(COLUMNS):
            self.list_frame.grid_columnconfigure(c, weight=1)

    # ---------- Search ----------
    def update_list(self, event=None):
        query = self.search_var.get().lower()
        if query == "search here...":
            query = ""

        self.filtered_keys = [
            k for k in self.data.keys()
            if query in k.lower()
        ]
        self.selected_index = 0
        self.render_buttons()
        self.update_selection()

    def clear_placeholder(self, event):
        if self.search_entry.get() == "Search here...":
            self.search_entry.delete(0, "end")
            self.search_entry.config(fg=TEXT)

    def restore_placeholder(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search here...")
            self.search_entry.config(fg=TEXT_MUTED)

    # ---------- Actions ----------
    def paste_first(self, event=None):
        if self.filtered_keys:
            self.use_value(self.data[self.filtered_keys[0]])

    def use_value(self, value):
        if not self.persistent_mode.get() and not self.editor_open:
            self.hide()
        else:
            # oddaj fokus, ale zostaw okno
            self.root.withdraw()
            self.root.after(1, self.root.deiconify)

        threading.Thread(
            target=self.clipboard.paste_text,
            args=(value,),
            daemon=True
        ).start()

    def handle_global_key(self, key):
        if not self.root.winfo_viewable():
            return

        try:
            if key == keyboard.Key.left:
                self.safe_call(self.move_selection, -1, 0)
            elif key == keyboard.Key.right:
                self.safe_call(self.move_selection, 1, 0)
            elif key == keyboard.Key.up:
                self.safe_call(self.move_selection, 0, -1)
            elif key == keyboard.Key.down:
                self.safe_call(self.move_selection, 0, 1)
            elif key == keyboard.Key.enter:
                self.safe_call(self.paste_selected)
            elif key == keyboard.Key.esc:

                if self.editor_open and self.editor_window:
                    self.safe_call(self.editor_window.close)
                else:
                    self.safe_call(self.on_escape)

        except Exception:
            pass

    # ---------- Visibility ----------
    def show(self):
        self.root.attributes("-alpha", 0.0)
        mx, my = get_mouse_position()
        self.root.update_idletasks()

        w, h = self.root.winfo_width(), self.root.winfo_height()
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        pad = 10

        y = my - h - pad if my > sh * 0.7 else my + pad
        x = mx - w - pad if mx + w + pad > sw else mx + pad

        self.root.geometry(f"+{max(0, x)}+{max(0, y)}")
        self.root.deiconify()
        self.root.lift()
        self.fade_in()
        self.search_entry.focus_set()
        self.selected_index = 0
        self.update_selection()

    def fade_in(self, step=0.1):
        alpha = self.root.attributes("-alpha")
        if alpha < 0.92:
            self.root.attributes("-alpha", alpha + step)
            self.root.after(15, self.fade_in)

    def on_escape(self):
        if self.editor_open:
            return
        print(self.editor_open)
        self.hide()

    def hide(self):
        if not self.root.winfo_viewable() or self.editor_open:
            return
        self.persistent_mode.set(False)
        self.search_var.set("")
        self.update_list()
        self.root.withdraw()

    def run(self):
        self.root.mainloop()

    # metody: on_config_change, open_editor, safe_call, create_button, move_selection, scroll_to_selection,
    # paste_selected, update_selection, render_buttons, update_list, clear_placeholder, restore_placeholder,
    # paste_first, use_value, handle_global_key, show, fade_in, on_escape, hide, run
    # (możesz skopiować implementację tych metod z obecnego pliku, tylko używając self.config_manager i self.clipboard)

    # Dla oszczędności miejsca tu nie kopiuję wszystkich metod; w implementacji przenieś metody z istniejącego `PopupUI`
    # i zamień bezpośrednie wywołania funkcji do zapisu/odczytu i paste_text na self.config_manager / self.clipboard.
