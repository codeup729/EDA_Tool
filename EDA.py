import pandas as pd 
import numpy as np
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import sweetviz as sv
import os
from pandas_profiling import ProfileReport
# the crux of UI integration is that sometimes you have to have a bridge of sorts, 
# helper methods or drop down to a level where both libraries can talk to each other, 
# in this case a tkinter canvas.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from autoviz.AutoViz_Class import AutoViz_Class

def handle_tools():
    path_ht = values['-IN-']
    df_ht = pd.read_csv(path_ht)

    if values['-TOOL-']=='sweetviz':
        report = sv.analyze(df_ht)
        report.show_html("sweet_report.html")

    if values['-TOOL-']=='autoviz':
        AV = AutoViz_Class()
        av = AV.AutoViz(df_ht)

    if values['-TOOL-']=='pandas profiling':
        design_report = ProfileReport(df_ht)
        design_report.to_file(output_file='report.html')

    # Autoviz and pandas profiling code to be completed

def viz_window():
    all_columns = list(df.columns)
    plot_list = ['scatter','line']
    layout = [
        [
            sg.Text("X axis: "), # command-slash 
            sg.Combo(all_columns,default_value=all_columns[0],
            enable_events=True,key="-X-")
        ],
        [
            sg.Text("Y axis: "),
            sg.Combo(all_columns,default_value=all_columns[0],
            enable_events=True,key="-Y-")
            # sg.Listbox(all_columns,default_values=[all_columns[0]],
            # enable_events=True,select_mode='multiple',size=(25,1),key="-Y-")
        ],
        [
            sg.Text("Plot: "),
            sg.Combo(plot_list,default_value=plot_list[0],enable_events=True,
            size=(25,1),key="-PLOT-")
        ],
        [
            sg.Button("Show",enable_events=True,key="-SHOW_PLT-")
        ]
    ]
    window = sg.Window("Visualization",layout,size=(650,200))
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "-SHOW_PLT-":
            handle_plot(values)
        #add visualisation functionality with matplotlib
        
    window.close()


def handle_plot(values):
    _VARS = {'window': False}
    layout = [
        [sg.Canvas(key='figCanvas')],
        [sg.Button('Exit')]
        ]
    _VARS['window'] = sg.Window('Graph Window',layout,finalize=True,resizable=True,
    element_justification="right")

    if values["-PLOT-"] == 'scatter':
        f, ax = plt.subplots(figsize=(15,15))
        plt.title('Scatter Plot')
        ax2 = ax.twinx()

        ax.scatter(df[values["-X-"]], df[values["-Y-"]])
        ax.set_xlabel(values["-X-"])
        ax.legend(loc='upper right')
        # Instead of plt.show
        draw_figure(_VARS['window']['figCanvas'].TKCanvas, f)

    elif values["-PLOT-"] == 'line':
        f, ax = plt.subplots(figsize=(20,15))
        plt.title('Line Plot')
        ax2 = ax.twinx()

        ax.plot(df[values["-X-"]], df[values["-Y-"]])
        ax.set_xlabel(values["-X-"])
        ax.legend(loc='upper right')
         # Instead of plt.show
        draw_figure(_VARS['window']['figCanvas'].TKCanvas, f)

    while True:
        event, values = _VARS['window'].read(timeout=200)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    
    _VARS['window'].close()



def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


file_choose = [
    [
        sg.Text("Data File"),
        sg.In(size=(25,1),enable_events=True,key="-FILE-"),
        sg.FileBrowse(key="-IN-")
    ]
]

tool_list = ['sweetviz','autoviz','pandas profiling']
tool_choose = [
    [
        sg.Text("Choose Tool"),
        sg.Combo(tool_list,default_value='sweetviz',size=(25,1),
        key="-TOOL-")
    ],
    [sg.Button("Perform EDA",enable_events=True,key="-EDA-")]
]

plot_choose = [
    [sg.Text("   ")],
    [sg.Text("To Visualize:")],
    [sg.Button("Visualisation options",enable_events=True,
    key="-VIZ-")]

        # sg.Text("X axis"), # command-slash 
        # sg.Combo(all_columns,default_value=all_columns[0],
        # enable_events=True,key="-X-"),
]

model_list = ['Linear Regression',"Classification"]
model_choose = [
    [sg.Text("   ")],
    [sg.Text("To Fit a Model:")],
    [
        sg.Text("Choose Model: "),
        sg.Combo(model_list,default_value=model_list[0],size=(25,1),
        key='-MODEL-')
    ],
    [sg.Button("Fit",enable_events=True,size=(25,1),key="-VIZ-")]
]


layout = [
    file_choose,tool_choose,plot_choose,model_choose
]

window = sg.Window("EDA Report",layout,size=(750,350))
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED,'Exit'):
        break
    if event == '-FILE-':
        path = values['-IN-']
        df = pd.read_csv(path)
    if event == '-EDA-':
        handle_tools()
    if event == '-VIZ-':
        viz_window()

window.close()