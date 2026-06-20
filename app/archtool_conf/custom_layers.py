from archtool.global_types import AppModule
from archtool.layers.default_layers import default_layers

APPS: list[AppModule] = [
    AppModule("app.users"),
    AppModule("app.todos"),
]

app_layers = default_layers
