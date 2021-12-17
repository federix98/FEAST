import os, sys
# Include Component directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\Components")

from Analyzer import Analyzer
from SocketConnector import SocketConnector

planner_host = '127.0.0.1'  # Standard loopback interface address (localhost)
planner_port = 65432        # Port to listen on (non-privileged ports are > 1023)

monitor_host = '127.0.0.1'  # Standard loopback interface address (localhost)
monitor_port = 65433        # Port to listen on (non-privileged ports are > 1023)

layered_analyzer = Analyzer(
    monitor_connector=SocketConnector(HOST=monitor_host, PORT=monitor_port, tp="SERVER"), 
    planner_connector=SocketConnector(HOST=planner_host, PORT=planner_port, tp="CLIENT"))