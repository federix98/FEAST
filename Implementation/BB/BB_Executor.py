import os, sys
# Include Component directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\Components")

from Executor import Executor
from SocketConnector import SocketConnector
from DatabaseConnector import DatabaseConnector

planner_host = '127.0.0.1'  # Standard loopback interface address (localhost)
planner_port = 65431        # Port to listen on (non-privileged ports are > 1023)

HOST = "localhost" 
USER = "--- INSERT USER ---"       
PASS = "--- INSERT PASSWORD ---"
DB = "--- INSERT DATABASE ---"

blackboard_executor = Executor(
    planner_connector=DatabaseConnector(HOST=HOST, USER=USER, PASS=PASS, DB=DB, target_table = "planner_data"),
    verbose=1)