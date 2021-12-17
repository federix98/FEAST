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
from statistics import mean



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
        xaxis_title = 'Time intervals',
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

def equation_filter(data, threshold = 0.04, penality = 1):
    #print(data[:10])
    _result = []
    for val in data:
        if val >= threshold:
            _result.append((threshold - val))
        else:
            _result.append((threshold - val))
    #print(_result[:10])
    return _result

def cumulate_data(data):
    _result, act_sum = [], 0
    for idx, val in enumerate(data):
        if idx == 0:
            _result.append(data[0])
            act_sum = data[0]
        else:
            #print(act_sum)
            _result.append(act_sum + val)
            act_sum += val
    return _result

### THIS IS FOR CONSUMPTION GENERATION DATA
def generate_data(component_layered_val, component_bb_val, component_ed_val, component_std_val, penality = 1, threshold = 0.1):
    return [
        ["Layered Implementation", component_layered_val],
        ["Blackboard Implementation", component_bb_val],
        ["Event Driven Implementation", component_ed_val],
        ["Without adaptation", component_std_val]
    ],[
        ["Layered Implementation", equation_filter(component_layered_val, threshold = threshold, penality = penality)],
        ["Blackboard Implementation", equation_filter(component_bb_val, threshold = threshold, penality = penality)],
        ["Event Driven Implementation", equation_filter(component_ed_val, threshold = threshold, penality = penality)],
        ["Without adaptation", equation_filter(component_std_val, threshold = threshold, penality = penality)]
    ],[
        ["Layered Implementation filtered", cumulate_data(equation_filter(component_layered_val, threshold = threshold, penality = penality))],
        ["Blackboard Implementation filtered", cumulate_data(equation_filter(component_bb_val, threshold = threshold, penality = penality))],
        ["Event Driven Implementation filtered", cumulate_data(equation_filter(component_ed_val, threshold = threshold, penality = penality))],
        ["Without adaptation", cumulate_data(equation_filter(component_std_val, threshold = threshold, penality = penality))]
    ],[
        ["Layered Implementation", cumulate_data(component_layered_val)],
        ["Blackboard Implementation", cumulate_data(component_bb_val)],
        ["Event Driven Implementation", cumulate_data(component_ed_val)],
        ["Without adaptation", cumulate_data(component_std_val)]
    ]

def read_consumption_files(files, timeword = "Time", with_input = False, separator = ';'):
    count = 0
    row_list = ""

    sm_ly = []

    for file in files:
        print("ANALYZING FILE", file)
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv.reader(iter(csv_file.readline,'')):
                if count > 1:
                    if len(row)>0:
                        text = ','.join(row)
                        if not timeword in text:
                            row_list = row_list + text
                            line_data = row_list
                            data_array = line_data.split(',')
                            if(len(data_array)>23):
                                if not timeword in line_data:
                                    #print(data_array)
                                    ts = data_array[0]
                                    vals = [float(i) for i in data_array[1:-1] if '-' not in i]
                                    #print (len(line_data.split(";")))
                                    row_list=""
                                    #print(line_data.split(";"))
                                    sm_ly.append(mean(vals))
                count+=1

    #print(sm_ly)
    return sm_ly


if __name__ == '__main__':
    #graph_generator()
    files = [
        ["Consumption/results_LY/processed_data.csv"], 
        ["Consumption/results_BB/processed_data.csv"], 
        ["Consumption/results_ED/processed_data.csv"], 
        ["Consumption/results_STD/processed_data.csv"],
    ]

    

    CONSUMPTION_LY = read_consumption_files(files[0])
    CONSUMPTION_BB = read_consumption_files(files[1])
    CONSUMPTION_ED = read_consumption_files(files[2])
    CONSUMPTION_STD = read_consumption_files(files[3])

    ln = min(len(CONSUMPTION_LY), len(CONSUMPTION_BB), len(CONSUMPTION_ED), len(CONSUMPTION_STD))

    __consumption = [
        cumulate_data(equation_filter(CONSUMPTION_LY[:ln])),
        cumulate_data(equation_filter(CONSUMPTION_BB[:ln])),
        cumulate_data(equation_filter(CONSUMPTION_ED[:ln])),
        cumulate_data(equation_filter(CONSUMPTION_STD[:ln]))
    ]

    graph_generator("Energy Consumption (In Joules)", __consumption, ["Layered", "Blackboard", "EventDriven", "Standard"], "energy_consumption_24h")



