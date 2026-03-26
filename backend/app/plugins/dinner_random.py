import random

from app.plugins.base import ServicePlugin


class DinnerRandomPlugin(ServicePlugin):
    plugin_type = "dinner_random"

    def validate_config(self, config: dict) -> None:
        return None

    def generate(self, config: dict) -> dict:
        choices = config.get("choices") or ["Noodles", "Hot Pot", "Rice Bowl", "Dumplings"]
        return {
            "title": config.get("title", "Dinner Suggestion"),
            "message": random.choice(choices),
            "signature": config.get("signature", "DotFlow"),
        }
