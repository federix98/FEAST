import os, sys
# Include Component directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\Components")

from Monitor import Monitor
from SocketConnector import SocketConnector
from DatabaseConnector import DatabaseConnector

HOST = "localhost" 
USER = "--- INSERT USER ---"       
PASS = "--- INSERT PASSWORD ---"
DB = "--- INSERT DATABASE ---"

blackboard_monitor = Monitor(DatabaseConnector(HOST=HOST, USER=USER, PASS=PASS, DB=DB))
blackboard_monitor.stream_csv_file()