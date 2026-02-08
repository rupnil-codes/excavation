import os
from textual_serve.server import Server

server = Server(
    command = "python -m textual",
    host = "0.0.0.0",
    port = int(os.environ.get("PORT", 10000)),
)
server.serve()