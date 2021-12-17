import os, sys
# Include Component directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\Components")

from Monitor import Monitor
from SocketConnector import SocketConnector

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65433       # Port to listen on (non-privileged ports are > 1023)

layered_monitor = Monitor(SocketConnector(HOST=HOST, PORT=PORT, tp="CLIENT"))
layered_monitor.stream_csv_file()