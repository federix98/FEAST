import os, sys
# Include Component directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\Components")

from Planner import Planner
from KafkaConnector import KafkaConnector

analyzer_host = 'localhost'  # Standard loopback interface address (localhost)
analyzer_port = 9092        # Port to listen on (non-privileged ports are > 1023)
analyzer_topic = "BatchDataTopic"
analyzer_key = "data"
analyzer_tp = "Consumer"

executor_host = 'localhost'  # Standard loopback interface address (localhost)
executor_port = 9092        # Port to listen on (non-privileged ports are > 1023)
executor_topic = "PlannerExecutorTopic"
executor_key = "data"
executor_tp = "Producer"

eventdriven_analyzer = Planner(
    analyzer_connector=KafkaConnector(
        HOST=analyzer_host, 
        PORT=analyzer_port, 
        topic=analyzer_topic, 
        key=analyzer_key, 
        tp=analyzer_tp
        ),
    executor_connector=KafkaConnector(
        HOST=executor_host, 
        PORT=executor_port, 
        topic=executor_topic, 
        key=executor_key, 
        tp=executor_tp
        ),
    verbose=0
    )