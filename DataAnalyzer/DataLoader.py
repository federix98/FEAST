import pandas as pd
import numpy as np
from UtilityAnalyzer import UtilityAnalyzer
import os
import csv
from statistics import mean

class DataLoader:

    def __init__(self, parent_folder):
        self.parent_folder = parent_folder
        self.BB_Folder = "BB"
        self.ED_Folder = "ED"
        self.LI_Folder = "LY"
        self.consumption_files = [
            [self.parent_folder + "/LY/processed_data.csv"], 
            [self.parent_folder + "/BB/processed_data.csv"], 
            [self.parent_folder + "/ED/processed_data.csv"], 
            [self.parent_folder + "/STD/processed_data.csv"]
        ]
        self.data = {}

    def mean_aggregation(self, data, n = 10):
        #return list(np.mean(data.reshape(-1, num), axis=1))
        xp = np.r_[data, np.nan + np.zeros((-len(data) % n,))]
        return np.nanmean(xp.reshape(-1, n), axis=-1)
        #return list(itertools.chain.from_iterable([i]*n for i in [sum(data[i:i+n])//n for i in range(0,len(data),n)]))

    def align(self, mon, an, pl, ex):
        ln = min(len(mon), len(an), len(pl), len(ex))
        return mon[:ln], an[:ln], pl[:ln], ex[:ln]

    def sum_up(self, mon, an, pl, ex):
        mon, an, pl, ex = self.align(mon, an, pl, ex)
        res = np.add(np.add(np.add(mon, an), pl), ex)
        return res
    
    def read_consumption_files(self, files, timeword = "Time", with_input = False, separator = ';', interval = 10):
        count = 0
        row_list = ""

        sm_ly = []

        for file in files:
            print("ANALYZING FILE", file)
            with open(file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                c = 0
                for row in csv.reader(iter(csv_file.readline,'')):
                    if count > 1:
                        if len(row)>0:
                            text = ','.join(row)
                            if not timeword in text:
                                
                                #print(count)
                                #print(text)
                                #input()
                                row_list = row_list + text
                                line_data = row_list
                                data_array = line_data.split(',')
                                #print(data_array)
                                #input()
                                #if(len(data_array)>23):
                                #print(data_array)
                                #print(count)
                                ts = data_array[0]
                                vals = [float(i) for i in data_array[1:-1] if '-' not in i]
                                #print (len(line_data.split(";")))
                                row_list=""
                                #print(line_data.split(";"))
                                sm_ly.append(sum(vals))
                                #print("len", len(sm_ly))
                                #sm_ly.append(mean(vals))
                    count+=1

        #print(sm_ly)
        dat = np.add.reduceat(sm_ly, np.arange(0, len(sm_ly), interval))
        print("Numrows", len(dat))
        return dat

    def load(self):

        if self.parent_folder == "24h":
            interval = 10
            mon_interval = 16
            an_interval = 10
            pl_interval = 1
            ex_interval = 1
        else:
            mon_interval = 750
            an_interval = 600
            pl_interval = 60
            ex_interval = 60
            interval = 600

        print("Loading...")
        self.data["MONITOR_LAYERED_RESPTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.LI_Folder + '/MonitorRT_.txt', delimiter=";", header=None).values[0][:-1], n = mon_interval)
        self.data["MONITOR_LAYERED_CPUTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.LI_Folder + '/MonitorCPU_.txt', delimiter=";", header=None).values[0][:-1], n = mon_interval)
        self.data["MONITOR_BB_RESPTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.BB_Folder + '/MonitorRT_.txt', delimiter=";", header=None).values[0][:-1], n = mon_interval)
        self.data["MONITOR_BB_CPUTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.BB_Folder + '/MonitorCPU_.txt', delimiter=";", header=None).values[0][:-1], n = mon_interval)
        self.data["MONITOR_ED_RESPTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.ED_Folder + '/MonitorRT_.txt', delimiter=";", header=None).values[0][:-1], n = mon_interval)
        self.data["MONITOR_ED_CPUTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.ED_Folder + '/MonitorCPU_.txt', delimiter=";", header=None).values[0][:-1], n = mon_interval)
        print("Monitor data loaded!")
        self.data["ANALYZER_LAYERED_RESPTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.LI_Folder + '/AnalyzerRT_.txt', delimiter=";", header=None).values[0][:-1], n = an_interval)
        self.data["ANALYZER_LAYERED_CPUTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.LI_Folder + '/AnalyzerCPU_.txt', delimiter=";", header=None).values[0][:-1], n = an_interval)
        self.data["ANALYZER_BB_RESPTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.BB_Folder + '/AnalyzerRT_.txt', delimiter=";", header=None).values[0][:-1], n = an_interval)
        self.data["ANALYZER_BB_CPUTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.BB_Folder + '/AnalyzerCPU_.txt', delimiter=";", header=None).values[0][:-1], n = an_interval)
        self.data["ANALYZER_ED_RESPTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.ED_Folder + '/AnalyzerRT_.txt', delimiter=";", header=None).values[0][:-1], n = an_interval)
        self.data["ANALYZER_ED_CPUTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.ED_Folder + '/AnalyzerCPU_.txt', delimiter=";", header=None).values[0][:-1], n = an_interval)
        print("Analyzer data loaded!")
        self.data["PLANNER_LAYERED_RESPTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.LI_Folder + '/PlannerRT_.txt', delimiter=";", header=None).values[0][:-1], n = pl_interval)
        self.data["PLANNER_LAYERED_CPUTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.LI_Folder + '/PlannerCPU_.txt', delimiter=";", header=None).values[0][:-1], n = pl_interval)
        self.data["PLANNER_BB_RESPTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.BB_Folder + '/PlannerRT_.txt', delimiter=";", header=None).values[0][:-1], n = pl_interval)
        self.data["PLANNER_BB_CPUTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.BB_Folder + '/PlannerCPU_.txt', delimiter=";", header=None).values[0][:-1], n = pl_interval)
        self.data["PLANNER_ED_RESPTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.ED_Folder + '/PlannerRT_.txt', delimiter=";", header=None).values[0][:-1], n = pl_interval)
        self.data["PLANNER_ED_CPUTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.ED_Folder + '/PlannerCPU_.txt', delimiter=";", header=None).values[0][:-1], n = pl_interval)
        print("Planner data loaded!")
        self.data["EXECUTOR_LAYERED_RESPTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.LI_Folder + '/ExecutorRT_.txt', delimiter=";", header=None).values[0][:-1], n = ex_interval)
        self.data["EXECUTOR_BB_RESPTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.BB_Folder + '/ExecutorRT_.txt', delimiter=";", header=None).values[0][:-1], n = ex_interval)
        self.data["EXECUTOR_ED_RESPTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.ED_Folder + '/ExecutorRT_.txt', delimiter=";", header=None).values[0][:-1], n = ex_interval)
        self.data["EXECUTOR_LAYERED_CPUTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.LI_Folder + '/ExecutorRT_.txt', delimiter=";", header=None).values[0][:-1], n = ex_interval)
        self.data["EXECUTOR_BB_CPUTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.BB_Folder + '/ExecutorRT_.txt', delimiter=";", header=None).values[0][:-1], n = ex_interval)
        self.data["EXECUTOR_ED_CPUTIME"] = self.mean_aggregation(pd.read_csv(self.parent_folder + '/' + self.ED_Folder + '/ExecutorRT_.txt', delimiter=";", header=None).values[0][:-1], n = ex_interval)
        print("Executor data loaded!")
        

        print("Interval", interval)
        self.data["CONSUMPTION_LY"] = self.read_consumption_files(self.consumption_files[0], interval = interval)
        self.data["CONSUMPTION_BB"] = self.read_consumption_files(self.consumption_files[1], interval = interval)
        self.data["CONSUMPTION_ED"] = self.read_consumption_files(self.consumption_files[2], interval = interval)
        self.data["CONSUMPTION_STD"] = self.read_consumption_files(self.consumption_files[3], interval = interval)
        print("Consumption data loaded! Success")

    def apply_utility(self, RT_Thresh, E_Thresh, verbose = 1):
        utility = UtilityAnalyzer()

        normalize_roof = max([max(v) for k, v in self.data.items()])

        REAL_RT_LY = self.sum_up(self.data["MONITOR_LAYERED_RESPTIME"], self.data["ANALYZER_LAYERED_RESPTIME"], self.data["PLANNER_LAYERED_RESPTIME"], self.data["EXECUTOR_LAYERED_RESPTIME"])
        REAL_RT_BB = self.sum_up(self.data["MONITOR_BB_RESPTIME"], self.data["ANALYZER_BB_RESPTIME"], self.data["PLANNER_BB_RESPTIME"], self.data["EXECUTOR_BB_RESPTIME"])
        REAL_RT_ED = self.sum_up(self.data["MONITOR_ED_RESPTIME"], self.data["ANALYZER_ED_RESPTIME"], self.data["PLANNER_ED_RESPTIME"], self.data["EXECUTOR_ED_RESPTIME"])


        RT_LY = utility.utility_function(REAL_RT_LY, threshold = RT_Thresh)
        RT_BB = utility.utility_function(REAL_RT_BB, threshold = RT_Thresh)
        RT_ED = utility.utility_function(REAL_RT_ED, threshold = RT_Thresh)


        ln = min(len(self.data["CONSUMPTION_LY"]), len(self.data["CONSUMPTION_BB"]), len(self.data["CONSUMPTION_ED"]), len(self.data["CONSUMPTION_STD"]))

        __consumption = [
            utility.utility_function(self.data["CONSUMPTION_LY"][:ln], threshold = E_Thresh, roof = 25, min_val = 10),
            utility.utility_function(self.data["CONSUMPTION_BB"][:ln], threshold = E_Thresh, roof = 25, min_val = 10),
            utility.utility_function(self.data["CONSUMPTION_ED"][:ln], threshold = E_Thresh, roof = 25, min_val = 10),
            utility.utility_function(self.data["CONSUMPTION_STD"][:ln], threshold = E_Thresh, roof = 25 ,min_val = 10)
        ]


        #print("VALUES", RT_LY, RT_BB, RT_ED)
        RRT_LY = utility.reverse(RT_LY)
        RRT_BB = utility.reverse(RT_BB)
        RRT_ED = utility.reverse(RT_ED)


        ROI_LY = np.divide(__consumption[0][:min(len(RRT_LY), len(__consumption[0]))], RRT_LY[:min(len(RRT_LY), len(__consumption[0]))])
        ROI_BB = np.divide(__consumption[1][:min(len(RRT_BB), len(__consumption[1]))], RRT_BB[:min(len(RRT_BB), len(__consumption[1]))])
        ROI_ED = np.divide(__consumption[2][:min(len(RRT_ED), len(__consumption[2]))], RRT_ED[:min(len(RRT_ED), len(__consumption[2]))])

        CROI_LY = utility.cumulate_data(ROI_LY)
        CROI_BB = utility.cumulate_data(ROI_BB)
        CROI_ED = utility.cumulate_data(ROI_ED)

        print("Accumulated ROI for different strategies")
        print("THRESHOLDS:", "RT", RT_Thresh, "ENERGY", E_Thresh)
        print("Layered", round(sum(ROI_LY), 2))
        print("Centralized", round(sum(ROI_BB), 2))
        print("Event Driven", round(sum(ROI_ED), 2))

        print("TOTAL AVERAGE RESPONSE TIME LY", round(sum(REAL_RT_LY) / len(REAL_RT_LY), 3))
        print("TOTAL AVERAGE RESPONSE TIME BB", round(sum(REAL_RT_BB) / len(REAL_RT_BB), 3))
        print("TOTAL AVERAGE RESPONSE TIME ED", round(sum(REAL_RT_ED) / len(REAL_RT_ED), 3))
        print("TOTAL ENERGY CONSUMED LY", round(sum(self.data["CONSUMPTION_LY"]), 3))
        print("TOTAL ENERGY CONSUMED BB", round(sum(self.data["CONSUMPTION_BB"]), 3))
        print("TOTAL ENERGY CONSUMED ED", round(sum(self.data["CONSUMPTION_ED"]), 3))
        print("TOTAL UTILITY COST LY", round(sum(RRT_LY), 3))
        print("TOTAL UTILITY COST BB", round(sum(RRT_BB), 3))
        print("TOTAL UTILITY COST ED", round(sum(RRT_ED), 3))
        print("TOTAL UTILITY BENEFIT LY", round(sum(__consumption[0]), 3))
        print("TOTAL UTILITY BENEFIT BB", round(sum(__consumption[1]), 3))
        print("TOTAL UTILITY BENEFIT ED", round(sum(__consumption[2]), 3))


        return RT_LY, RT_BB, RT_ED, __consumption, CROI_LY, CROI_BB, CROI_ED
