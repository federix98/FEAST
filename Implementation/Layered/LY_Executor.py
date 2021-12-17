import os, sys
# Include Component directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\Components")

from Executor import Executor
from SocketConnector import SocketConnector

planner_host = '127.0.0.1'  # Standard loopback interface address (localhost)
planner_port = 65431        # Port to listen on (non-privileged ports are > 1023)

layered_executor = Executor(
    planner_connector=SocketConnector(
        HOST=planner_host, 
        PORT=planner_port, 
        tp="SERVER"
        ),
    verbose=1)