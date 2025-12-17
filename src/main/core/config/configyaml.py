import logging
from typing import Any
import yaml

class ConfigManager:
    def __init__(self, config_file):
        if config_file:
            self.config_file = config_file
        else:
            self.config_file = "src/config/config.yaml"
        self.config = self.load_config()

    def load_config(self) -> dict:
        try:
            with open(self.config_file, 'r') as file:
                config = yaml.safe_load(file)
                return config
        except FileNotFoundError:
            logging.warn(f"File '{self.config_file}' not found")
            return {}
        except yaml.YAMLError as e:
            logging.error(f"Errore loading YAML file: {e}")
            raise e

    def get_value(self, key) -> Any:
        return self.config.get(key)

    def set_value(self, key, value):
        self.config[key] = value
        self.save_config()

    def save_config(self):
        try:
            with open(self.config_file, 'w') as file:
                yaml.dump(self.config, file, default_flow_style=False)
        except yaml.YAMLError as e:
            logging.info("Errore nel salvataggio del file YAML: %s", e)
