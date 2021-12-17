import os, sys
# Include Component directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\Components")

from Planner import Planner
from SocketConnector import SocketConnector
from DatabaseConnector import DatabaseConnector

analyzer_host = '127.0.0.1'  # Standard loopback interface address (localhost)
analyzer_port = 65432        # Port to listen on (non-privileged ports are > 1023)

executor_host = '127.0.0.1'
executor_port = 65431

HOST = "localhost" 
USER = "--- INSERT USER ---"       
PASS = "--- INSERT PASSWORD ---"
DB = "--- INSERT DATABASE ---"

blackboard_planner = Planner(
    analyzer_connector=DatabaseConnector(HOST=HOST, USER=USER, PASS=PASS, DB=DB, target_table = "analyzer_data"),
    executor_connector=DatabaseConnector(HOST=HOST, USER=USER, PASS=PASS, DB=DB, target_table = "planner_data"),
    )