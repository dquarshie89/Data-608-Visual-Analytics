import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import flask
from flask import jsonify, render_template

health_query = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=boroname,health,steward,count(tree_id)' +\
        '&$group=boroname,steward,health').replace(' ', '%20')

df = pd.read_json(health_query)

tree_options = df["boroname"].unique()

server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server, url_base_pathname='/dashapp/')

app.layout = html.Div([
    html.H2("Tree Health by # of Stewards"),
    html.Div(
        [
            dcc.Dropdown(
                id="boroname",
                options=[{
                    'label': i,
                    'value': i
                } for i in tree_options],
                value='All Boros'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    dcc.Graph(id='funnel-graph'),
])

@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('boroname', 'value')])
def update_graph(boroname):
    if boroname == "All Boros":
        df_plot = df.copy()
    else:
        df_plot = df[df['boroname'] == boroname]

    pv = pd.pivot_table(
        df_plot,
        index=['steward'],
        columns=['health'],
        values=['count_tree_id'],
        aggfunc=sum,
        fill_value=0)

    trace1 = go.Bar(x=pv.index, y=pv[('count_tree_id', 'Fair')], name='Fair')
    trace2 = go.Bar(x=pv.index, y=pv[('count_tree_id', 'Good')], name='Good')
    trace3 = go.Bar(x=pv.index, y=pv[('count_tree_id', 'Poor')], name='Poor')

    return {
        'data': [trace1, trace2, trace3],
        'layout':
        go.Layout(
            title='Tree Health for {}'.format(boroname),
            barmode='stack')
    }


@server.route("/dash")
def MyDashApp():
    return app.index()





if __name__ == '__main__':
    server.run(debug=True)