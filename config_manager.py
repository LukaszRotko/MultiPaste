# python
import os
import json
import sys

class ConfigManager:
    def __init__(self, configs_dir="configs"):
        self.configs_dir = configs_dir
        self.active_file = os.path.join(self.configs_dir, "active_config.json")
        os.makedirs(self.configs_dir, exist_ok=True)
        self._ensure_default()

    def _ensure_default(self):
        default = os.path.join(self.configs_dir, "default.json")
        if not os.path.exists(default):
            with open(default, "w", encoding="utf-8") as f:
                json.dump({"name": "", "email": ""}, f, indent=2)
        if not os.path.exists(self.active_file):
            self.set_active("default.json")

    def list_configs(self):
        return [f for f in os.listdir(self.configs_dir) if f.endswith(".json")]

    def get_active(self):
        try:
            with open(self.active_file, "r", encoding="utf-8") as f:
                return json.load(f).get("active", "default.json")
        except Exception:
            return "default.json"

    def set_active(self, name):
        with open(self.active_file, "w", encoding="utf-8") as f:
            json.dump({"active": name}, f)

    def load_active(self):
        name = self.get_active()
        path = os.path.join(self.configs_dir, name)
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_active(self, data):
        name = self.get_active()
        path = os.path.join(self.configs_dir, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def create_config(self, name):
        if not name.endswith(".json"):
            name += ".json"
        path = os.path.join(self.configs_dir, name)
        if os.path.exists(path):
            return False
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)
        self.set_active(name)
        return True

    def set_active_config(self,name):
        with open(self.active_file, "w", encoding="utf-8") as f:
            json.dump({"active": name}, f)
