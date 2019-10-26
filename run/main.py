import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from tabs import tab_1_PSO
from tabs import tab_2_Plot
import pandas as pd
import plotly.graph_objs as go
import json
from dash.exceptions import PreventUpdate

app = dash.Dash()

app.config['suppress_callback_exceptions'] = True
global trace

app.layout = html.Div([
    html.H1('PSO Algorithm App'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Run PSO Algorithm', value='tab-1-example'),
        dcc.Tab(label='Plot PSO', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example')
])

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return tab_1_PSO.pso_layout
    elif tab == 'tab-2-example':
        return tab_2_Plot.plot_layout

#Tab 1
@app.callback(
    Output('output-disp','children'),
    [Input('button_a', 'n_clicks'),
     Input('min_val', 'value'),
     Input('max_val', 'value')]
)

def do_calc(n_clicks,min_val,max_val):
    return u'''Best Solution: {}'''.format(tab_1_PSO.calc(n_clicks,min_val,max_val))

# Tab 2 callback
@app.callback(Output('display-plot', 'figure'),
              [Input('button_b', 'n_clicks')])

def plot_graph(n_clicks):
    trace = None
    if n_clicks > 1:
        df = pd.read_json('C:/Users/QA/Desktop/PSO_Py/run/tabs/Export_DataFrame.json')
        trace = [go.Scatter3d ( x = df['X'], y = df['Y'], z=df['Z'], mode='markers', 
                    marker=dict(size=5,line=dict(color='rgba(217,217,217,0.14)',width = 0.5), opacity = 0.8))]
        
        return {"data":trace}
    elif n_clicks is None:
          raise PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)