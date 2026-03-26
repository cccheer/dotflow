from app.plugins.base import ServicePlugin
from app.plugins.coffee_random import CoffeeRandomPlugin
from app.plugins.custom_text import CustomTextPlugin
from app.plugins.dinner_random import DinnerRandomPlugin
from app.plugins.webhook_text import WebhookTextPlugin


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, ServicePlugin] = {}
        self.register(CoffeeRandomPlugin())
        self.register(DinnerRandomPlugin())
        self.register(CustomTextPlugin())
        self.register(WebhookTextPlugin())

    def register(self, plugin: ServicePlugin) -> None:
        self._plugins[plugin.plugin_type] = plugin

    def get(self, plugin_type: str) -> ServicePlugin:
        try:
            return self._plugins[plugin_type]
        except KeyError as exc:
            raise ValueError(f"Unsupported service type: {plugin_type}") from exc

    def list_types(self) -> list[str]:
        return sorted(self._plugins.keys())


plugin_registry = PluginRegistry()
