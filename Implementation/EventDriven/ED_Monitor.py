import os, sys
# Include Component directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\Components")

from Monitor import Monitor
from KafkaConnector import KafkaConnector

HOST = "localhost"  
PORT = 9092       
topic ="CupCarbonEventsTopic"
key = ""

eventdriven_monitor = Monitor(
    KafkaConnector(
        HOST=HOST, 
        PORT=PORT, 
        topic=topic, 
        key=key, 
        tp="Producer"
        ))
    
eventdriven_monitor.stream_csv_file()