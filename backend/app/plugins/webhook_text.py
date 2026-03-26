from app.plugins.base import ServicePlugin


class WebhookTextPlugin(ServicePlugin):
    plugin_type = "webhook_text"

    def validate_config(self, config: dict) -> None:
        if not config.get("url"):
            raise ValueError("webhook_text requires url")

    def generate(self, config: dict) -> dict:
        self.validate_config(config)
        # TODO: Replace with real webhook fetching once the upstream contract is finalized.
        return {
            "title": config.get("title", "Webhook Message"),
            "message": config.get("mock_message", "Webhook integration scaffolded"),
            "signature": config.get("signature", "DotFlow"),
        }
