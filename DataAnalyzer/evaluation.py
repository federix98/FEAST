import plotly.graph_objects as go
import pandas as pd
from statistics import mean
import pstats
import itertools
import numpy as np
import math
#from psutil import cpu_percent
import os
import csv
from sklearn.preprocessing import MinMaxScaler

from DataLoader import DataLoader

def graph_generator(y_title, y_values, names, img_name):
    fig = go.Figure()  # create the base
    minutes = 120
    intervals = 10
    #x_axis_time_list = [index for index in range(0, minutes, 1) if index % intervals == 0]
    #y_values = [[1, 2, 3, 4, 5, 6], [1.5, 2.4, 3.6, 3.9, 4.9,6.8]]
    x_axis_time_list = list(range(len(y_values[0])))

    # Edit the layout
    fig.update_layout(
        # title='Energy Consumption for Scenario ' + scenario_name,
        #xaxis_title='Time intervals (Aggregated over 10 minutes)',
        xaxis_title = 'Time intervals (Aggregated over 10 minutes)',
        #yaxis_title='Energy Consumption (In Joules)', 
        yaxis_title = y_title,
        font=dict(
            family="sans serif",
            size=14,
            color="black",
        ), margin={"r": 0, "t": 0, "l": 0, "b": 0}, legend=
        dict(
            # orientation="v",
            # anchor="bottom",
            # y=1.02,
            # xanchor="right",
            # x=1.0,
            font=dict(size=12)
        ))
    graph_id = "2"

    num_plots = len (y_values)
    for index in range (0, num_plots):
        fig.add_trace(go.Scatter(x=x_axis_time_list, y=y_values[index], name=names[index])) #,line=dict(color='firebrick', width=4)) -- color choices can be given


    # save the image locally with good resolution
    fig.write_image(img_name + ".png", format="png",#"energy_consumption_" + graph_id + "_cumul.png", format="png",
                    engine="kaleido",
                    width=640, height=480,
                    scale=10.0)
    #print (x_axis_time_list)

if __name__ == "__main__":
    print("Starting evaluation of Simulation Data...")

    RT_Thresh = 0.08
    E_Thresh = 14  # Joules per 10 min

    loader24 = DataLoader("24h")
    loader24.load()

    loader2 = DataLoader("2h")
    loader2.load()


    # =========================================

    RT_Thresh = 0.06
    E_Thresh = 15  # Joules per 10 min

    print("\n\nScenario --> 2")

    RT_LY, RT_BB, RT_ED, __consumption, CROI_LY, CROI_BB, CROI_ED = loader2.apply_utility(RT_Thresh = RT_Thresh, E_Thresh = E_Thresh, verbose = 1)
    # graph_generator("Cumulated ROI", [CROI_LY, CROI_BB, CROI_ED], ["Socket", "Centralized", "PublishSubscribe"], "CROI_2h")
    # print("IMAGES GENERATED")

    print("\n\nScenario --> 24")
    
    RT_LY, RT_BB, RT_ED, __consumption, CROI_LY, CROI_BB, CROI_ED = loader24.apply_utility(RT_Thresh = RT_Thresh, E_Thresh = E_Thresh, verbose = 1)
    # graph_generator("Cumulated ROI", [CROI_LY, CROI_BB, CROI_ED], ["Socket", "Centralized", "PublishSubscribe"], "CROI_24h")
    # print("IMAGES GENERATED")
    
    #dat = loader24.read_consumption_files(loader24.consumption_files[0])
    #print(len(dat))

    # =========================================

    RT_Thresh = 0.08
    E_Thresh = 14  # Joules per 10 min

    print("\n\nScenario --> 2")

    RT_LY, RT_BB, RT_ED, __consumption, CROI_LY, CROI_BB, CROI_ED = loader2.apply_utility(RT_Thresh = RT_Thresh, E_Thresh = E_Thresh, verbose = 1)
    # graph_generator("Cumulated ROI", [CROI_LY, CROI_BB, CROI_ED], ["Socket", "Centralized", "PublishSubscribe"], "CROI_2h")
    # print("IMAGES GENERATED")

    print("\n\nScenario --> 24")
    
    RT_LY, RT_BB, RT_ED, __consumption, CROI_LY, CROI_BB, CROI_ED = loader24.apply_utility(RT_Thresh = RT_Thresh, E_Thresh = E_Thresh, verbose = 1)
    # graph_generator("Cumulated ROI", [CROI_LY, CROI_BB, CROI_ED], ["Socket", "Centralized", "PublishSubscribe"], "CROI_24h")
    # print("IMAGES GENERATED")
    
    #dat = loader24.read_consumption_files(loader24.consumption_files[0])
    #print(len(dat))

    # =========================================

    RT_Thresh = 0.05
    E_Thresh = 18  # Joules per 10 min

    print("\n\nScenario --> 2")

    RT_LY, RT_BB, RT_ED, __consumption, CROI_LY, CROI_BB, CROI_ED = loader2.apply_utility(RT_Thresh = RT_Thresh, E_Thresh = E_Thresh, verbose = 1)
    # graph_generator("Cumulated ROI", [CROI_LY, CROI_BB, CROI_ED], ["Socket", "Centralized", "PublishSubscribe"], "CROI_2h")
    # print("IMAGES GENERATED")

    print("\n\nScenario --> 24")
    
    RT_LY, RT_BB, RT_ED, __consumption, CROI_LY, CROI_BB, CROI_ED = loader24.apply_utility(RT_Thresh = RT_Thresh, E_Thresh = E_Thresh, verbose = 1)
    # graph_generator("Cumulated ROI", [CROI_LY, CROI_BB, CROI_ED], ["Socket", "Centralized", "PublishSubscribe"], "CROI_24h")
    # print("IMAGES GENERATED")
    
    #dat = loader24.read_consumption_files(loader24.consumption_files[0])
    #print(len(dat))