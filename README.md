# MultiPaste
PasteDeck 🧩

Fast, keyboard-driven multi-paste & snippet manager

PasteDeck is a lightweight desktop utility that lets you paste predefined snippets, clipboard history items, and custom fields instantly — without breaking your workflow.

Designed for speed, keyboard navigation, and background usage, PasteDeck lives quietly in your system tray and appears exactly when you need it.

✨ Key Features
🔹 Snippet-based multi-paste

Store reusable text snippets (e.g. CV fields, emails, templates)

Paste any value instantly with keyboard navigation

Organize snippets using multiple JSON configs (profiles)

🔹 Popup UI near your cursor

Appears next to the mouse position

Fully keyboard-driven (arrows + Enter)

Searchable list with instant filtering

🔹 Multiple configs (profiles)

Separate configs for:

CV / job applications

Work

Personal use

Active config persists between sessions

🔹 Config editor (built-in)

Add / edit / remove fields visually

Changes are saved directly to JSON

No need to edit files manually

🔹 Persistent mode

Paste multiple items without closing the popup

Ideal for filling long forms

🔹 Runs in background

Tray icon (Show / Quit)

Global hotkeys

Minimal system footprint

🧠 Clipboard History (Planned / v1+)

PasteDeck is evolving beyond static snippets.

Upcoming features include:

📋 Clipboard history tracking

Automatically save copied text (Ctrl+C)

Optional toggle (on/off)

Alternative shortcut (e.g. Ctrl+Alt+C)

🧹 Manage recent clipboard items

Remove single entries

Clear all

Set max history size (FIFO)

🔀 Merge clipboard entries

Combine multiple clipboard items into one snippet

📦 Convert clipboard history into a regular config

Duplicate / merge into existing snippet profiles

⌨️ Default Shortcuts
Action	Shortcut
Show popup	Ctrl + Alt
Navigate	Arrow keys
Paste	Enter
Close popup	Esc
Persistent paste	Toggle in UI

(Shortcuts will be configurable in future versions)

🗂️ Project Structure
PasteDeck/
├── configs/
│   ├── default.json
│   ├── active_config.json
│   └── other_profiles.json
├── main.py
├── README.md
└── LICENSE

🛠️ Tech Stack

Python

Tkinter (UI)

pynput (global hotkeys)

pyperclip (clipboard access)

pystray (system tray)

JSON-based storage

No external services. No telemetry. Fully offline.

🚧 Roadmap
v1

✅ Multi-paste popup

✅ Multiple configs

✅ Config editor

✅ Persistent mode

✅ Tray app

v1.1+

⏳ Clipboard history

⏳ Clipboard merge

⏳ Config CRUD (add / duplicate / delete)

⏳ Import / export configs

⏳ Settings panel

🤝 Contributing

Contributions are welcome!

You can help by:

Reporting bugs

Proposing UX improvements

Implementing new features

Refactoring / cleanup

Please open an issue or submit a pull request.

Note: This project uses a non-commercial license.
Contributions are accepted under the same license.

📄 License

This project is licensed under a Non-Commercial Open Source License.

✔ Free to use

✔ Source code visible

✔ Contributions allowed

❌ Commercial use forbidden

❌ Repackaging / selling forbidden

See LICENSE file for details.

👤 Author

Created by Łukasz Rotko

If you like the idea or use it daily — ⭐ the repo!
