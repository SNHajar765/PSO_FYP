import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import json

plot_layout = html.Div([
    html.H1('PSO 3D Plot'),
    html.Button('Display', id='button_b', n_clicks= 2),
    html.Div([dcc.Graph(id='display-plot')])
])

########################## PSO PLOT ######################################################################################################## 
