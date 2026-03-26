from app.plugins.base import ServicePlugin


class CustomTextPlugin(ServicePlugin):
    plugin_type = "custom_text"

    def validate_config(self, config: dict) -> None:
        if not config.get("message"):
            raise ValueError("custom_text requires message")

    def generate(self, config: dict) -> dict:
        self.validate_config(config)
        return {
            "title": config.get("title", "Custom Message"),
            "message": config["message"],
            "signature": config.get("signature", "DotFlow"),
        }
