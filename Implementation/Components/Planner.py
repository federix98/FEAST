from Custom_Logger import logger
import numpy as np
from numpy import array
from Initializer import Initialize
import socket
import random
import pandas as pd
import time
import os
from os import listdir
from os.path import isfile, join

import cProfile, pstats, io
from pstats import SortKey

from Connector import Connector
from Profiler import Profiler
from UtilLib import Utils
# The purpose of this class is to implement the adaptation logic depending on the type of adaptation that needs to be executed


class Planner():
    def __init__(self, analyzer_connector, executor_connector, project_path="./NdR_CO", verbose=0, clean=0):

        # ALWAYS POSITIVE PREDICTION TRICK
        self.last_energy_pred = 0

        self.verbose = verbose
        self.clean = clean

        self.analyzer_connector = analyzer_connector
        self.executor_connector = executor_connector
        self.profiler = Profiler()
        self.profiler.reset("PlannerRT_.txt", "PlannerCPU_.txt")

        self.project_path = project_path
        sensorfiles_path = self.project_path + "/config/nodes/"
        sensorfiles = [f for f in listdir(sensorfiles_path) if isfile(join(sensorfiles_path, f))]

        self.dict_sensor_freq_keys = {}
        self.sensor_id_key_map = {}
        self.sensor_mapping = {}
        self.reverse_sensor_map = {}
        
        sensor_count = 0
        
        for sfile in sensorfiles:
            if "sensor" in sfile:
                sfile_struct = {}
                with open(sensorfiles_path + sfile) as f:
                    line = f.readline()
                    while line:
                        if ":" in line:
                            sfile_par = line.split(":")[0]
                            sfile_val = line.split(":")[1]
                            sfile_struct[sfile_par] = sfile_val.replace("\n", "")
                        line = f.readline()
                
                device_name = sfile_struct["device_script_file_name"]
                sensor_count += 1
                s_id = "S" + str(sensor_count)
                s_orig_id = "S" + str(sfile_struct["device_id"])

                self.sensor_mapping[s_orig_id] = s_id
                self.reverse_sensor_map[s_id] = s_orig_id
                
                if "_" in device_name:
                    valid_sensor = device_name.replace("_", "").replace(".csc", "")
                    norm_loc = valid_sensor + "Normal"
                    crit_loc = valid_sensor + "Critical"
                    self.dict_sensor_freq_keys[norm_loc] = 15000
                    self.dict_sensor_freq_keys[crit_loc] = 5000
                    self.sensor_id_key_map[s_orig_id] = valid_sensor
        self.init_obj = Initialize()
        self.sensor_id_list = [] # Integere values just containing the id of the sensors
        for key in self.sensor_id_key_map:
            sensor_id = int(self.sensor_mapping[key].split("S")[1])
            self.sensor_id_list.append(sensor_id)

        self.high_power = self.init_obj.energy_hp

        self.base_power = self.init_obj.energy_bp

        # Define the reduction frequency values
        self.reduction_freq_normal_hp = 20000
        self.reduction_freq_critical_hp = 10000
        self.reduction_freq_normal_bp = 10000
        self.reduction_freq_critical_bp = 5000
        self.adapation_count  = 0   # Keep a count on the total adaptations performed
        self.time_count  = 0 # Keep a check on the time lapsed
        self.bp_time = 0 # If a sensor has stayed in bp for 20 instances reset this value and restore to old frequency
        self.bp_count = self.init_obj.bp_count

        self.listen_and_plan()

    def reactive(self,in_energy_list):
        # Get the list of energy consumption and decide on the adaptation
        # Change the frequency of sensors in CupCarbon

        # Ignore the index which has not to be accounted for computing the increase

        # Energy list consists of 1 lists with energy of each component
        '''
        energy_list = []
        for index in range(22):
            sum_val = 0
            for i in range (len(in_energy_list)):
                sum_val = sum_val + in_energy_list[i][index]
            energy_list.append(sum_val)

        '''
        max_value  = 0
        max_index = 0
        energy_list = in_energy_list[0]
        
        for index in range(0,len(energy_list)):
            if (index!=20):
                if energy_list[index] > max_value:
                    max_value = energy_list[index]
                    max_index = index
        
        frequency_map = self.dict_sensor_freq_keys.copy()
        # print("frequency map created", frequency_map)
        
        total_energy_consumed = sum(energy_list)
        print ("plan")
        logger.info("Inside Adaptation Planner")
        print (total_energy_consumed)
        self.time_count += self.init_obj.lag
        if total_energy_consumed>= self.high_power:
            for index in self.sensor_id_list:
                reduction_freq_critical = 0
                reduction_freq_normal = 0
                self.adapation_count += 1

                if energy_list[index] == max_value:
                    print ("here")
                    reduction_freq_normal = self.reduction_freq_normal_hp
                    reduction_freq_critical = self.reduction_freq_critical_hp
                else:
                    reduction_percent = ((max_value - energy_list[index]) / max_value)
                    reduction_freq_normal = int(self.reduction_freq_normal_hp * reduction_percent)
                    reduction_freq_critical = int(self.reduction_freq_critical_hp * reduction_percent)

                sensor_key = "S" + str(index)  # Form the sensor id to be used to get data from the reverse map
                sensor_freq_key = self.sensor_id_key_map[self.reverse_sensor_map[sensor_key]]
                frequency_map[sensor_freq_key + "Normal"] = frequency_map[
                                                              sensor_freq_key + "Normal"] + reduction_freq_normal
                frequency_map[sensor_freq_key + "Critical"] = frequency_map[
                                                              sensor_freq_key + "Critical"] + reduction_freq_critical

            # Write the adaptation to the file
            write_string = ""
            for key in frequency_map:
                write_string = write_string + key + " " + str(frequency_map[key]) + "\n"
            write_string = write_string[:-1]

            # print("SENDING 159", write_string)
            self.executor_connector.send(write_string)


        elif total_energy_consumed < self.high_power and total_energy_consumed >= self.base_power:
            self.adapation_count += 1


            for index in self.sensor_id_list:
                reduction_freq_critical = 0
                reduction_freq_normal = 0
                if energy_list[index] == max_value:
                    reduction_freq_normal = self.reduction_freq_normal_bp
                    reduction_freq_critical = self.reduction_freq_critical_bp
                else:
                    reduction_percent = ((max_value - energy_list[index]) / max_value)
                    reduction_freq_normal = int(self.reduction_freq_normal_bp * reduction_percent)
                    reduction_freq_critical = int(self.reduction_freq_critical_bp * reduction_percent)

                sensor_key = "S" + str(index)  # Form the sensor id to be used to get data from the reverse map
                sensor_freq_key = self.sensor_id_key_map[self.reverse_sensor_map[sensor_key]]
                frequency_map[sensor_freq_key + "Normal"] = frequency_map[
                                                              sensor_freq_key + "Normal"] + reduction_freq_normal
                frequency_map[sensor_freq_key + "Critical"] = frequency_map[
                                                              sensor_freq_key + "Critical"] + reduction_freq_critical

            # Write the adaptation to the file
            write_string = ""
            for key in frequency_map:
                write_string = write_string + key + " " + str(frequency_map[key]) + "\n"
            write_string = write_string[:-1]
            # print("SENDING 190", write_string)
            self.executor_connector.send(write_string)


        elif total_energy_consumed < self.base_power:
            # Means no need to perform any adaptation the original frequency remains as it is
            self.bp_time +=1
            if (self.bp_time>=self.init_obj.bp_count): # Change this depending on the lag value
                # Restore back to original frequencies
                # Write the adaptation to the file
                write_string = ""
                for key in frequency_map:
                    write_string = write_string + key + " " + str(frequency_map[key]) + "\n"
                write_string = write_string[:-1]
                # print("SENDING 204", write_string)
                self.executor_connector.send(write_string)

        logger.info("Adaptation reactive executor")

    def proactive(self,inverse_forecast_features,energy_forecast_total,horizon=10):
        self.time_count += self.init_obj.lag
        # First form the list with the accumulated sum of each forecast for the time horizon
        #print (inverse_forecast_features)
        in_energy_list = []
        energy_value_list = []

        for j in range(0, inverse_forecast_features.shape[1]):
            energy_value_list.append(inverse_forecast_features[0, j])
            if (len(energy_value_list)==22):
                in_energy_list.append(energy_value_list)
                energy_value_list = []

        energy_list = []
        if self.verbose:
            print ("IN ENERGY LIST", in_energy_list)
        for index in range(22):
            sum_val = 0
            for i in range(horizon):
                sum_val = sum_val + in_energy_list[i][index]
            energy_list.append(sum_val)


        #print (energy_list)
        if self.verbose:
            print ("ENERGY FORECAST TOTAL", energy_forecast_total)
        max_value  = 0
        max_index = 0
        for index in range(0,len(energy_list)):
            if (index!=20):
                if energy_list[index] > max_value:
                    max_value = energy_list[index]
                    max_index = index
        # Calculate the frequency reduction and write to the text file
        frequency_map = self.dict_sensor_freq_keys.copy()
        # print("frequency map created", frequency_map)
        # Calculate the data transfer frequency reduction
        total_energy_consumed = sum(energy_list)

        # -------------------------------------
        #   ALWAYS POSITIVE PREDICTION TRICK
        # -------------------------------------
        if energy_forecast_total < 0:
            if self.verbose:
                print("NEGATIVE PREDICTION", energy_forecast_total)
            energy_forecast_total = self.last_energy_pred
        else:
            self.last_energy_pred = energy_forecast_total

        if self.verbose:
            print ("proactive plan")
        logger.info("Inside Adaptation Planner --proactive")
        #total_energy_consumed = total_energy_consumed + random.randint(0,3)
        total_energy_consumed = energy_forecast_total
        #if self.verbose:
        print("Totally energy consumed", total_energy_consumed)
        print("High power", self.high_power)
        if total_energy_consumed>= self.high_power:
            #self.time_count += self.init_obj.lag
            self.adapation_count += 1
            for index in self.sensor_id_list:
                reduction_freq_critical = 0
                reduction_freq_normal = 0
                if energy_list[index] == max_value:
                    #print ("here")
                    reduction_freq_normal = self.reduction_freq_normal_hp
                    reduction_freq_critical = self.reduction_freq_critical_hp
                else:
                    reduction_percent = ((max_value - energy_list[index]) / max_value)
                    reduction_freq_normal = int(self.reduction_freq_normal_hp * reduction_percent)
                    reduction_freq_critical = int(self.reduction_freq_critical_hp * reduction_percent)

                sensor_key = "S" + str(index)  # Form the sensor id to be used to get data from the reverse map
                sensor_freq_key = self.sensor_id_key_map[self.reverse_sensor_map[sensor_key]]
                # print("FREQ MAP", frequency_map)
                frequency_map[sensor_freq_key + "Normal"] = frequency_map[
                                                              sensor_freq_key + "Normal"] + reduction_freq_normal
                frequency_map[sensor_freq_key + "Critical"] = frequency_map[
                                                              sensor_freq_key + "Critical"] + reduction_freq_critical


            # --------------------------------------------
            #   COMMUNICATION WITH THE EXECUTOR COMPONENT
            # --------------------------------------------
            # Write the adaptation to the file
            write_string = ""
            for key in frequency_map:
                write_string = write_string + key + " " + str(frequency_map[key]) + "\n"
            write_string = write_string[:-1]

            # print("SENDING 298", write_string)
            self.executor_connector.send(write_string)


        elif total_energy_consumed < self.high_power and total_energy_consumed >= self.base_power:
            self.adapation_count += 1
            for index in self.sensor_id_list:
                reduction_freq_critical = 0
                reduction_freq_normal = 0
                if energy_list[index] == max_value:
                    reduction_freq_normal = self.reduction_freq_normal_bp
                    reduction_freq_critical = self.reduction_freq_critical_bp
                else:
                    reduction_percent = ((max_value - energy_list[index]) / max_value)
                    reduction_freq_normal = int(self.reduction_freq_normal_bp * reduction_percent)
                    reduction_freq_critical = int(self.reduction_freq_critical_bp * reduction_percent)

                sensor_key = "S" + str(index)  # Form the sensor id to be used to get data from the reverse map
                sensor_freq_key = self.sensor_id_key_map[self.reverse_sensor_map[sensor_key]]
                frequency_map[sensor_freq_key + "Normal"] = frequency_map[
                                                              sensor_freq_key + "Normal"] + reduction_freq_normal
                frequency_map[sensor_freq_key + "Critical"] = frequency_map[
                                                              sensor_freq_key + "Critical"] + reduction_freq_critical

            # Write the adaptation to the file
            write_string = ""
            for key in frequency_map:
                write_string = write_string + key + " " + str(frequency_map[key]) + "\n"
            write_string = write_string[:-1]
            # text_file = open("config.txt", "w")
            # text_file.write(write_string)
            # text_file.close()

            # print("SENDING 331", write_string)
            self.executor_connector.send(write_string)




        elif total_energy_consumed < self.base_power:
            # Means no need to perform any adaptation the original frequency remains as it is
            self.bp_time +=1
            if (self.bp_time>=self.bp_count):
                # Restore back to original frequencies
                # Write the adaptation to the file
                write_string = ""
                #print(frequency_map)
                for key in frequency_map:
                    write_string = write_string + key + " " + str(frequency_map[key]) + "\n"
                write_string = write_string[:-1]
                # print("SENDING 347", write_string)
                self.executor_connector.send(write_string)

        logger.info("Adaptation reactive executor")
    
    def listen_and_plan(self):

        self.analyzer_connector.connect()   
        self.executor_connector.connect()
        while True:

            

            if self.clean:
                Utils.screen_clear

            #print("Planner is listening")

            kafka_flag = 0

            # Trick to speedup the Event Driven part
            if hasattr(self.analyzer_connector, 'tp') and self.analyzer_connector.tp == "Consumer":
                results = self.analyzer_connector.consumer
                #print("KafkaConnector detected")
                kafka_flag = 1
            else:
                #print("Socket or DB connector detected")
                results = self.analyzer_connector.receive()
                if not isinstance(results, list):
                    results = [results]

            if self.verbose:
                print(results)

            for res in results:

                # ------------ START PROFILING -------------
                self.profiler.start_All_Profile()
                # ------------------------------------------

                #print(res)

                # EVENT DRIVEN SPEEDUP
                if kafka_flag:
                    res = str(res.value, 'utf-8')  

                #print(res) 

                if res == None:
                    break

                lst = res.split(" ")
                inverse_forecast_features = np.array(lst[:(len(lst) - 3)],).astype('f').reshape(( int(lst[len(lst) - 3]), int(lst[len(lst) - 2]) )) #.astype('float32') 
                energy_forecast_total = float(lst[len(lst) - 1])   
                self.proactive(inverse_forecast_features,energy_forecast_total,horizon=10) # Edit the orizon 

                # ------------ END PROFILING ---------------
                self.profiler.end_All_Profile("PlannerRT_.txt", "PlannerCPU_.txt")
                # ------------------------------------------