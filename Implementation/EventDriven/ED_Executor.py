import os, sys
# Include Component directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\Components")

from Executor import Executor
from KafkaConnector import KafkaConnector

planner_host = 'localhost'  # Standard loopback interface address (localhost)
planner_port = 9092        # Port to listen on (non-privileged ports are > 1023)
planner_topic = "PlannerExecutorTopic"
planner_key = "data"
planner_tp = "Consumer"

eventdriven_executor = Executor(
    planner_connector=KafkaConnector(
        HOST=planner_host, 
        PORT=planner_port, 
        topic=planner_topic, 
        key=planner_key, 
        tp=planner_tp
        ),
    verbose=0)