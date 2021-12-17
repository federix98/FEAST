import plotly.graph_objects as go
import pandas as pd
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
        xaxis_title = 'Adaptation Cycles',
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


if __name__ == '__main__':
    #graph_generator()


    BB_Folder = "BB/perf_data"
    ED_Folder = "EventDriven/perf_data"
    LI_Folder = "Layered/perf_data"

    ress = {}

    MONITOR_LAYERED_RESPTIME = pd.read_csv(LI_Folder + '/MonitorRT_.txt', delimiter=";", header=None).values[0][:-1]
    MONITOR_LAYERED_CPUTIME = pd.read_csv(LI_Folder + '/MonitorCPU_.txt', delimiter=";", header=None).values[0][:-1]
    MONITOR_BB_RESPTIME = pd.read_csv(BB_Folder + '/MonitorRT_.txt', delimiter=";", header=None).values[0][:-1]
    MONITOR_BB_CPUTIME = pd.read_csv(BB_Folder + '/MonitorCPU_.txt', delimiter=";", header=None).values[0][:-1]
    MONITOR_ED_RESPTIME = pd.read_csv(ED_Folder + '/MonitorRT_.txt', delimiter=";", header=None).values[0][:-1]
    MONITOR_ED_CPUTIME = pd.read_csv(ED_Folder + '/MonitorCPU_.txt', delimiter=";", header=None).values[0][:-1]

    ANALYZER_LAYERED_RESPTIME = pd.read_csv(LI_Folder + '/AnalyzerRT_.txt', delimiter=";", header=None).values[0][:-1]
    ANALYZER_LAYERED_CPUTIME = pd.read_csv(LI_Folder + '/AnalyzerCPU_.txt', delimiter=";", header=None).values[0][:-1]
    ANALYZER_BB_RESPTIME = pd.read_csv(BB_Folder + '/AnalyzerRT_.txt', delimiter=";", header=None).values[0][:-1]
    ANALYZER_BB_CPUTIME = pd.read_csv(BB_Folder + '/AnalyzerCPU_.txt', delimiter=";", header=None).values[0][:-1]
    ANALYZER_ED_RESPTIME = pd.read_csv(ED_Folder + '/AnalyzerRT_.txt', delimiter=";", header=None).values[0][:-1]
    ANALYZER_ED_CPUTIME = pd.read_csv(ED_Folder + '/AnalyzerCPU_.txt', delimiter=";", header=None).values[0][:-1]

    PLANNER_LAYERED_RESPTIME = pd.read_csv(LI_Folder + '/PlannerRT_.txt', delimiter=";", header=None).values[0][:-1]
    PLANNER_LAYERED_CPUTIME = pd.read_csv(LI_Folder + '/PlannerCPU_.txt', delimiter=";", header=None).values[0][:-1]
    PLANNER_BB_RESPTIME = pd.read_csv(BB_Folder + '/PlannerRT_.txt', delimiter=";", header=None).values[0][:-1]
    PLANNER_BB_CPUTIME = pd.read_csv(BB_Folder + '/PlannerCPU_.txt', delimiter=";", header=None).values[0][:-1]
    PLANNER_ED_RESPTIME = pd.read_csv(ED_Folder + '/PlannerRT_.txt', delimiter=";", header=None).values[0][:-1]
    PLANNER_ED_CPUTIME = pd.read_csv(ED_Folder + '/PlannerCPU_.txt', delimiter=";", header=None).values[0][:-1]

    EXECUTOR_LAYERED_RESPTIME = pd.read_csv(LI_Folder + '/ExecutorRT_.txt', delimiter=";", header=None).values[0][:-1]
    EXECUTOR_BB_RESPTIME = pd.read_csv(BB_Folder + '/ExecutorRT_.txt', delimiter=";", header=None).values[0][:-1]
    EXECUTOR_ED_RESPTIME = pd.read_csv(ED_Folder + '/ExecutorRT_.txt', delimiter=";", header=None).values[0][:-1]
    EXECUTOR_LAYERED_CPUTIME = pd.read_csv(LI_Folder + '/ExecutorRT_.txt', delimiter=";", header=None).values[0][:-1]
    EXECUTOR_BB_CPUTIME = pd.read_csv(BB_Folder + '/ExecutorRT_.txt', delimiter=";", header=None).values[0][:-1]
    EXECUTOR_ED_CPUTIME = pd.read_csv(ED_Folder + '/ExecutorRT_.txt', delimiter=";", header=None).values[0][:-1]


    ln = min(len(MONITOR_LAYERED_RESPTIME), len(MONITOR_BB_RESPTIME), len(MONITOR_ED_RESPTIME))

    __monitor_resp_time = [
        cumulate_data(equation_filter(MONITOR_LAYERED_RESPTIME[:ln])),
        cumulate_data(equation_filter(MONITOR_BB_RESPTIME[:ln])),
        cumulate_data(equation_filter(MONITOR_ED_RESPTIME[:ln]))
    ]

    __analyzer_resp_time = [
        cumulate_data(equation_filter(ANALYZER_LAYERED_RESPTIME[:ln])),
        cumulate_data(equation_filter(ANALYZER_BB_RESPTIME[:ln])),
        cumulate_data(equation_filter(ANALYZER_ED_RESPTIME[:ln]))
    ]

    __planner_resp_time = [
        cumulate_data(equation_filter(PLANNER_LAYERED_RESPTIME[:ln])),
        cumulate_data(equation_filter(PLANNER_BB_RESPTIME[:ln])),
        cumulate_data(equation_filter(PLANNER_ED_RESPTIME[:ln]))
    ]

    __executor_resp_time = [
        cumulate_data(equation_filter(EXECUTOR_LAYERED_RESPTIME[:ln])),
        cumulate_data(equation_filter(EXECUTOR_BB_RESPTIME[:ln])),
        cumulate_data(equation_filter(EXECUTOR_ED_RESPTIME[:ln]))
    ]

    graph_generator("Monitor Response Time", __monitor_resp_time, ["Layered", "Blackboard", "EventDriven"], "monitor_resp_time")
    graph_generator("Analyzer Response Time", __analyzer_resp_time, ["Layered", "Blackboard", "EventDriven"], "analyzer_resp_time")
    graph_generator("Planner Response Time", __planner_resp_time, ["Layered", "Blackboard", "EventDriven"], "planner_resp_time")
    graph_generator("Executor Response Time", __executor_resp_time, ["Layered", "Blackboard", "EventDriven"], "executor_resp_time")



