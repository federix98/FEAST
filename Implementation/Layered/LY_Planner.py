import os, sys
# Include Component directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\Components")

from Planner import Planner
from SocketConnector import SocketConnector

analyzer_host = '127.0.0.1'  # Standard loopback interface address (localhost)
analyzer_port = 65432        # Port to listen on (non-privileged ports are > 1023)

executor_host = '127.0.0.1'
executor_port = 65431

layered_analyzer = Planner(
    analyzer_connector=SocketConnector(
        HOST=analyzer_host, 
        PORT=analyzer_port, 
        tp="SERVER",
        ),
    executor_connector=SocketConnector(
        HOST=executor_host, 
        PORT=executor_port, 
        tp="CLIENT",
        )
    )