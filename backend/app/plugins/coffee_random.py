import random

from app.plugins.base import ServicePlugin


class CoffeeRandomPlugin(ServicePlugin):
    plugin_type = "coffee_random"

    def validate_config(self, config: dict) -> None:
        return None

    def generate(self, config: dict) -> dict:
        choices = config.get("choices") or ["Latte", "Americano", "Flat White", "Mocha"]
        return {
            "title": config.get("title", "Coffee Suggestion"),
            "message": random.choice(choices),
            "signature": config.get("signature", "DotFlow"),
        }
