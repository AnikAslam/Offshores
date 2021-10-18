import plotly.graph_objects as go  # or
import plotly.express as px

token = "pk.eyJ1IjoiYW5pa2FzbGFtIiwiYSI6ImNrbnN2czJweDA4OHQyd3BkaXh3aXRyankifQ.JYDl5v48_QoA07QxY_yQHQ"

# Keep this out of source code repository - save in a file or a database
# VALID_USERNAME_PASSWORD_PAIRS = {
#     'AIUniversal': 'Input'
# }

import pandas as pd

off_shores = pd.read_csv("https://raw.githubusercontent.com/AnikAslam/Off-Shores/main/FinalAll.csv")
# d1 = off_shores[(off_shores['year'] >= 2000) & (off_shores['year'] <= 2020)]

fig = px.scatter_mapbox(off_shores, lat="Latitude", lon="Longitude",
                        color="Struc Type Code",
                        height=900, zoom=6, hover_name='Bus Asc Name',
                        hover_data=['Structure Name'],
                        )

fig.update_layout(title_text="Floating off-shores on Gulf of Mexico")
fig.update_layout(mapbox_style="mapbox://styles/mapbox/satellite-streets-v11", mapbox_accesstoken=token)
fig.update_layout(legend_x=0, legend_y=1)
fig.update_layout(legend_title_text='Offshore Structure Type')
# fig.update_layout(showlegend=False)

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


mark_values = {2000: '2000', 2002: '2002', 2004: '2004', 2006: '2006', 2008: '2008',
               2010: '2010', 2012: '2012', 2014: '2014', 2016: '2016', 2018: '2018',
               2020: '2020'}

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
]

dates = ['03-02-2021', '03-03-2021', '03-04-2021', '03-05-2021', '03-06-2021', '03-07-2021']
mytotaldates = {i:datetime.strptime(x, "%m-%d-%Y").date() for i,x in enumerate(dates)}

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# server = app.server
# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

app.layout = html.Div([
    html.Div([
        html.H1(children="Floating Off-Shores on Gulf of Mexico",
                style={"text-align": "center"})
    ]),

    html.Div([
        html.Div([
            dcc.Graph(id="the_graph", figure=fig, config={"displayModeBar": False})],
            style={"width": "75%", "display": "inline-block", "position": "relative"}),
        html.Div([
            html.Div([
                html.H3(children=" Structure Installation Date Range ",
                        style={"marginTop": "15%"}),
                html.Div([
                                dcc.RangeSlider(
                                    id = "the_year",
                                    updatemode = "drag",
                                    vertical = True,
                                    marks = mark_values,
                                    min = 2000,
                                    max = 2020,
                                    step = 1,
                                    value = [2000,2020],
                                    verticalHeight = 600)
                            ],style = {'marginLeft' : '35%'}),
            ], style={"height": "800px"}),
        ],
            style={'width': '25%',
                   'height': '100%'})
    ]),

    html.Div([
        html.H3(children=" Select the Structure ",
                style={}),
        html.H5(children=" (To be shown in table) ",
                style={}),
        dcc.Dropdown(
            id="dropdown",
            options=[
                {"label": "FIXED", "value": "FIXED"},
                {"label": "CAIS", "value": "CAIS"},
                {"label": "SPAR", "value": "SPAR"},
                {"label": "CT", "value": "CT"},
                {"label": "WP", "value": "WP"},
                {"label": "TLP", "value": "TLP"},
                {"label": "MTLP", "value": "MTLP"},
                {"label": "MOPU", "value": "MOPU"},
                {"label": "SEMI", "value": "SEMI"},
                {"label": "FPSO", "value": "FPSO"},
            ],
            value=['FIXED', 'CAIS', 'SPAR', 'CT', 'WP', 'TLP', 'MTLP', 'MOPU', 'SEMI', 'FPSO'],
            multi=True,
            placeholder='Select a Structure',
            style={"height": "30px", "width": "80%"},
        ),
        html.H3(children=" Data Representation in Table ",
                style={"text-align": "center"}),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in d1.columns],
            data=d1.to_dict('records'),
            sort_action='custom',
            sort_mode='multi',
            sort_by=[],
        ),
        html.P(''),
    ], style={"width": "70%", 'marginLeft': '13%'}),

])


@app.callback(
    Output('the_graph', 'figure'),
    [Input('the_year', 'value')]
)
def update_graph(years_chosen):
    dff1 = off_shores[(off_shores['year'] >= years_chosen[0]) & (off_shores['year'] <= years_chosen[1])]
    # filter df rows where column year values are >=1985 AND <=1988
    token = "pk.eyJ1IjoiYW5pa2FzbGFtIiwiYSI6ImNrbnN2czJweDA4OHQyd3BkaXh3aXRyankifQ.JYDl5v48_QoA07QxY_yQHQ"

    scatterplot = px.scatter_mapbox(
        data_frame=dff1,
        lat="Latitude", lon="Longitude",
        color="Struc Type Code",
        height=900, zoom=6, hover_name='Bus Asc Name',
        hover_data=['Structure Name'],
    )

    scatterplot.update_layout(mapbox_style="mapbox://styles/mapbox/satellite-streets-v11", mapbox_accesstoken=token)
    scatterplot.update_layout(legend_x=0, legend_y=1)
    scatterplot.update_layout(legend_title_text='Offshore Structure Type')
    return scatterplot


@app.callback(
    Output("table", "data"),
    [Input("the_year", "value"),
     Input("dropdown", "value")],
)
def update_output(years_chosen, value):
    dff = off_shores[(off_shores['year'] >= years_chosen[0]) & (off_shores['year'] <= years_chosen[1]) & (
        off_shores['Struc Type Code'].isin(value))]
    return dff.to_dict(orient='records')


if __name__ == '__main__':
    app.run_server(debug=True)