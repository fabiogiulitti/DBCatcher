import yaml

class ConfigManager:
    def __init__(self):
        self.config_file = "config/config.yaml"
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                config = yaml.safe_load(file)
                return config
        except FileNotFoundError:
            print(f"File '{self.config_file}' non trovato.")
            return {}
        except yaml.YAMLError as e:
            print(f"Errore nel caricamento del file YAML: {e}")
            return {}

    def get_value(self, key):
        return self.config.get(key)

    def set_value(self, key, value):
        self.config[key] = value
        self.save_config()

    def save_config(self):
        try:
            with open(self.config_file, 'w') as file:
                yaml.dump(self.config, file, default_flow_style=False)
        except yaml.YAMLError as e:
            print(f"Errore nel salvataggio del file YAML: {e}")

config = ConfigManager()