import os, sys
# Include Component directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\Components")

from Analyzer import Analyzer
from KafkaConnector import KafkaConnector

planner_host = 'localhost'  # Standard loopback interface address (localhost)
planner_port = 9092        # Port to listen on (non-privileged ports are > 1023)
planner_topic = "BatchDataTopic"
planner_key = "data"
planner_tp = "Producer"

monitor_host = 'localhost'  # Standard loopback interface address (localhost)
monitor_port = 9092        # Port to listen on (non-privileged ports are > 1023)
monitor_topic = "CupCarbonEventsTopic"
monitor_key = ""
monitor_tp = "Consumer"

eventdriven_analyzer = Analyzer(
    monitor_connector=KafkaConnector(
        HOST=monitor_host, 
        PORT=monitor_port, 
        topic=monitor_topic, 
        key=monitor_key, 
        tp=monitor_tp
        ), 
    planner_connector=KafkaConnector(
        HOST=planner_host, 
        PORT=planner_port, 
        topic=planner_topic, 
        key=planner_key, 
        tp=planner_tp
        )
    )