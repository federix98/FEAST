import subprocess

import csv
import sys
import time
import pickle
import socket
from kafka import KafkaConsumer, KafkaProducer

import cProfile, pstats, io
from pstats import SortKey

# Import from my classes
from Initializer import Initialize
from Connector import Connector
from Profiler import Profiler

class Monitor:

    def __init__(self, analyzer_connector):
        print("Constructing Monitor")
        self.init_object = Initialize()
        self.analyzer_connector = analyzer_connector
        self.profiler = Profiler()
        self.profiler.reset("MonitorRT_.txt", "MonitorCPU_.txt")

    def stream_csv_file(self):

        self.analyzer_connector.connect()

        row_list = ""
        count = 0
        with open(self.init_object.energy_path + self.init_object.energy_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            while (True):
                
                for row in csv.reader(iter(csv_file.readline,'')):

                    self.profiler.start_All_Profile()

                    if count > 1:
                        if len(row)>0:
                            text = row[0].strip("\n") # Get the first text
                            if not "Time" in text:
                                row_list = row_list + text
                                line_data = row_list
                                if(len(line_data.split(";"))>23):
                                    if not "Time" in line_data:
                                        #print (line_data)
                                        print("sent")
                                        #print (len(line_data.split(";")))

                                        self.analyzer_connector.send(line_data)

                                        row_list=""

                    count +=1

                    self.profiler.end_All_Profile("MonitorRT_.txt", "MonitorCPU_.txt")
                
