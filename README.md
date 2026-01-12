
<img width="1024" height="1024" alt="MultiPasteLogo" src="https://github.com/user-attachments/assets/c27d2e93-95a6-44c0-815c-fc3dedf4b2e3" />

# MultiPaste - v.0.7 - Alpha
**MultiPaste** is a lightweight background clipboard & snippet manager designed for fast, keyboard-driven workflows.  
Paste predefined snippets, manage multiple profiles (configs), and access your clipboard history — all from a minimal popup UI.

Built for developers, recruiters, power users, and anyone who pastes the same things over and over again.



## ✨ Features

### 🔹 Snippet-based multi-paste
- Store key → value pairs (e.g. `email`, `github`, `linkedin`)
- Paste values instantly using keyboard navigation
- No need to copy first — just select and paste

### 🔹 Multiple configs (profiles)
- Separate configs for:
  - CV / job applications
  - Work / private use
  - Different languages or contexts
- Active config is remembered between app launches
- Easy switching from dropdown menu

### 🔹 Built-in config editor
- Add, edit, and remove snippet entries
- JSON-based storage (human readable & portable)
- Editor opens in a separate modal window
- Safe focus handling (ESC behavior, no accidental closes)

### 🔹 Clipboard history (planned / v1 target)
- Automatically save recent `Ctrl+C` entries
- Configurable maximum history size
- Optional auto-record toggle
- Manual record shortcut (e.g. `Ctrl+C+Alt`)
- Clear single or all history entries
- Convert clipboard history into a reusable config

### 🔹 Persistent mode
- Keep popup open after pasting
- Paste multiple items without reopening the UI

### 🔹 Fast keyboard navigation
- Arrow keys to navigate grid
- Enter to paste
- ESC to close (editor first, popup second)
- Search-as-you-type filtering

### 🔹 Runs in background
- System tray integration
- Global hotkeys
- Always available, never in the way



## 🖥️ How it works

- Press **Ctrl + Alt** to open the popup near your cursor
- Choose what you want to paste
- Hit **Enter** — done
- No mouse required

Configs and data are stored as simple `.json` files inside the `configs/` directory.
More in-depth instructions to all features are included in Instructions.txt in the main folder.



## 📂 Project structure (simplified)

```text
MultiPaste/
├─ configs/
│  ├─ default.json
│  ├─ active_config.json
│  └─ your_other_configs.json
├─ main.py
└─ README.md
```

## 🔐 Privacy & Security

- ❌ No cloud
- ❌ No telemetry
- ❌ No background uploads
- ✅ Everything stays **on your machine**

MultiPaste never sends or stores your data anywhere outside your computer.



## 🤝 Contributing

Contributions are welcome ❤️

You can:
- Report bugs
- Suggest features
- Submit pull requests


## 📜 License

This project is licensed under a **non-commercial open source license**.

✔ Free for personal use  
✔ Source code visible  
✔ Community contributions allowed  

❌ Commercial use not allowed  
❌ Repackaging / selling not allowed  

See the `LICENSE` file for full details.

---

## 👤 Author

Created by **Łukasz Rotko**

If you like the project:
- ⭐ Star the repository  
- 💬 Share feedback  
- 🛠️ Contribute ideas or code  

---

## 🛣️ Roadmap (v1)

- [ ] Clipboard history with limits  
- [ ] Clipboard → config merge  
- [ ] Config duplication & deletion  
- [ ] Improved config management UI  
- [ ] Windows executable build  

---

