import csv
import sys
import time
import socket
from kafka import KafkaConsumer, KafkaProducer
from Initializer import Initialize
from Custom_Logger import logger
import numpy as np
from numpy import array
import pandas as pd
from datetime import datetime
import joblib
import mysql.connector
import sklearn

import tensorflow as tf

from tensorflow.python.keras.models import model_from_json
from tensorflow.python.keras import backend as K

from Initializer import Initialize


import json
from Initializer import Initialize
import KafkaConnector

import cProfile, pstats, io
from pstats import SortKey

from Connector import Connector
from Profiler import Profiler
from UtilLib import Utils



main_energy_list = []
class Analyzer():
    # Class that will perform the prediction in near-real time
    def __init__(self, monitor_connector, planner_connector, verbose=0, slow=0):
        print("Constructing Analyzer")
        self.monitor_connector = monitor_connector
        self.planner_connector = planner_connector
        self.profiler = Profiler()
        self.profiler.reset("AnalyzerRT_.txt", "AnalyzerCPU_.txt")
        self.init_obj = Initialize()
        self.verbose = verbose
        self.slow = slow

        self.prev_vals = [19160.0, 19160.0, 19160.0, 19160.0, 19160.0, 19160.0, 19160.0, 19160.0, 19160.0, 19160.0, 19160.0,
             19160.0, 19160.0, 19160.0, 19160.0, 19160.0, 19160.0, 19160.0, 19160.0, 19160.0, 19160.0,
             19160.0]  # Initialize the inital energy configuration

        # Set the ML model
        energy_model_file_json = self.init_obj.adaptation_model_json
        energy_model_file_h5 = self.init_obj.adaptation_model_h5

        self.scalar_energy = joblib.load(self.init_obj.scalar_path + self.init_obj.adaptation_model_scalar)

        self.graph = tf.compat.v1.get_default_graph()
        with self.graph.as_default():
            json_file_energy = open(self.init_obj.model_path + energy_model_file_json, 'r')
            loaded_model_energy_json = json_file_energy.read()
            json_file_energy.close()
            # Now loaded_model_energy_json contains json_file_energy data

            self.loaded_model_energy = model_from_json(loaded_model_energy_json)
            self.loaded_model_energy.load_weights(self.init_obj.model_path + energy_model_file_h5)
        
        print("Loaded model from disk")
        self.gather_data(adaptation_type=self.init_obj.adaptation_type,horizon=self.init_obj.horizon,lag=self.init_obj.lag,decision_period=self.init_obj.decision_period) # adaptation_type denotes the type of adaptation to be performed

    

    def process_sensor_data(self):
        # This will process the data from the sensor and then perform the management of the data
        print ("processing")
    def gather_data(self,adaptation_type,horizon=10,lag=10,decision_period=10):
        global main_energy_forecast
        global main_traffic_forecast
        main_energy_list = []

        self.monitor_connector.connect()
        self.planner_connector.connect()

        while True:
            
            #if isinstance(self.monitor_connector, KafkaConnector)

            kafka_flag = 0

            # Trick to speedup the Event Driven part
            if hasattr(self.monitor_connector, 'tp') and self.monitor_connector.tp == "Consumer":
                results = self.monitor_connector.consumer
                #print("KafkaConnector detected")
                kafka_flag = 1
                # for x in results:
                #     print("element", x)
            else:
                #print("Socket or DB connector detected")
                results = self.monitor_connector.receive()
                if not isinstance(results, list):
                    results = [results]

            #print("Starting loop")
            for res in results:

                # ------------ START PROFILING -------------
                self.profiler.start_All_Profile()
                # ------------------------------------------

                if res == None:
                    break
            
                if kafka_flag:
                    res = str(res.value)   
                
                row = res.split(";")
                #print(row)
                if (len(row) > 3):
                    if self.verbose:
                        print("\n\nrow", row)
                    time_string = row[0]
                    second_level_data = []
                    row.pop()  # remove the unwanted last element
                    vals = [x1 - float(x2) for (x1, x2) in zip(self.prev_vals, row[1:])]
                    # print (len (vals))
                    if (len(vals) == 22):
                        # Check if we have 22 elements always
                        # spark_predictor.main_energy_list.append(vals)
                        main_energy_list.append(vals)
                        #final_energy_list = [x + y for x, y in zip(final_energy_list, vals)] ## Keep addding them
                        self.prev_vals = [float(i) for i in row[1:]]

                if adaptation_type == "reactive":
                    if (len(main_energy_list) == 1):
                        #print (main_energy_list)
                        # Compute the energy consumed by each sensor
                        ada_obj.reactive(main_energy_list)
                        logger.info("adaptation count " + str(ada_obj.adapation_count) + " " + str(ada_obj.time_count))
                        main_energy_list = [] # This will mean only every 10 minutes an adaptation will be performed

                elif adaptation_type == "proactive":
                    #print (ada_obj.adapation_count)
                    if (len(main_energy_list) == lag):
                        print ("reached")
                        predict_array = np.array(main_energy_list)
                        predict_array = self.scalar_energy.fit_transform(predict_array)
                        # print (predict_array.shape)
                        predict_array = predict_array.reshape(1, lag, 22)
                        with self.graph.as_default():
                            energy_forecast = self.loaded_model_energy.predict(predict_array)
                        # K.clear_session()
                        inverse_forecast = energy_forecast.reshape(horizon, 22)
                        inverse_forecast = self.scalar_energy.inverse_transform(inverse_forecast)
                        inverse_forecast_features = inverse_forecast.reshape(energy_forecast.shape[0], 22*horizon)
                        energy_forecast_total = 0
                        for j in range(0, inverse_forecast_features.shape[1]):
                        #for j in range(0, 22*horizon): # Number of components * horizon equals inverse_forecast_Features.shape[1]
                            if j not in [20,42,64,86,108,130,152,174,196,218,240,262,284,306,328,350,372,394,416,438,460,482,504,526,548,570,592,614,636,658]:
                                # Ignore the database forecasts
                                energy_forecast_total = energy_forecast_total + inverse_forecast_features[0, j]

                        _list = Utils.reshape_tolist(inverse_forecast_features[0], inverse_forecast_features.shape)
                        # Try to append the EFT number in the list
                        _list.append(energy_forecast_total)
                        iff_toSend = " ".join(str(x) for x in _list)
                        
                        self.planner_connector.send(iff_toSend)
                        if self.verbose:
                            print("IFF and EFT Messages Sent")

                        main_energy_list = main_energy_list[decision_period:]  # This will mean only every 10 minutes an adaptation will be performed

                self.profiler.end_All_Profile("AnalyzerRT_.txt", "AnalyzerCPU_.txt")
                
            if self.slow:
                time.sleep(2)

            
