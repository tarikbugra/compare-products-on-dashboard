import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash_data import Data


data = Data()
plant_basis_data_w_ps = data.prepare_plant_data()
plant_basis_data = plant_basis_data_w_ps.loc[:, plant_basis_data_w_ps.columns != 'Max_PTF_SMF']

group_basis_data_w_ps = data.prepare_group_data()
group_basis_data = group_basis_data_w_ps.loc[:, group_basis_data_w_ps.columns != 'Max_PTF_SMF']


app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1('Kgup Cost Analysis',
            style={'text-align': 'center'}),

    html.Br(),

    dcc.Markdown('''**Choose to Compare:**'''),

    # html.Div([
    #     html.Button('Show TOP 30 of the month', id='button', style={'width': '%40', 'horizontal-align': 'middle'}),
    #
    # ]),

    dcc.RadioItems(
        id='radio',
        value='Power Plant Basis',
        options=[{'label': x, 'value': x} for x in ['Power Plant Basis', 'Group Basis']]
    ),

    html.Br(),

    dcc.Dropdown(id='dropdown_1',
                 style={'width': '40%'},
                 multi=True
                 ),

    dcc.Graph(id="graph"),

])


@app.callback(
    [Output('dropdown_1', 'options'),
     Output('dropdown_1', 'value')],
    Input('radio', 'value'))
def dropdown_options(radio_value):
    if radio_value == 'Power Plant Basis':
        options = [{'label': x, 'value': x} for x in list(plant_basis_data.columns)]
        value = ['poweplant1', 'powerplant2']
    else:
        options = [{'label': x, 'value': x} for x in list(group_basis_data.columns)]
        value = ['compnay1', 'compnay2']

    return options, value


@app.callback(
     Output("graph", "figure"),
    [Input("dropdown_1", "value")])
def display_(dropdown_value_1):

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if dropdown_value_1 is not None and set(dropdown_value_1).issubset(list(plant_basis_data.columns)):

        for k in dropdown_value_1:

            fig.add_trace(
                go.Scatter(x=plant_basis_data['date'],
                           y=plant_basis_data[k],
                           mode='lines+markers',
                           name=k),
                secondary_y=False
            )

        fig.add_trace(
            go.Scatter(x=plant_basis_data_w_ps['date'],
                       y=plant_basis_data_w_ps['Max_PTF_SMF'],
                       mode='markers+text',
                       text=[str(i) for i in list(
                           plant_basis_data_w_ps['Max_PTF_SMF'].round().astype(str).replace('\.0', '', regex=True))],
                       marker=dict(color='LightSkyBlue',
                                   size=30,
                                   line=dict(color='MediumPurple',
                                             width=3)),
                       name="PTF-SMF"), secondary_y=True,
        )

    elif dropdown_value_1 is not None and set(dropdown_value_1).issubset(list(group_basis_data.columns)):

        for k in dropdown_value_1:
            fig.add_trace(
                go.Bar(x=group_basis_data['date'],
                       y=group_basis_data[k],
                       name=k), secondary_y=False
            )

        fig.add_trace(
            go.Scatter(x=group_basis_data_w_ps['date'],
                       y=group_basis_data_w_ps['Max_PTF_SMF'],
                       mode='markers+text',
                       text=[str(i) for i in list(
                           group_basis_data_w_ps['Max_PTF_SMF'].round().astype(str).replace('\.0', '', regex=True))],
                       marker=dict(color='White',
                                   size=30,
                                   line=dict(color='MediumPurple',
                                             width=3)),
                       name="PTF-SMF"), secondary_y=True,
        )

    fig.update_xaxes(
        title_text="<b>Date</b>",
        tickvals=list(plant_basis_data_w_ps['date'])
    )

    if dropdown_value_1 is not None and set(dropdown_value_1).issubset(list(plant_basis_data.columns)):
        fig.update_yaxes(
            title_text="<b>Kgup Cost</b>",
            automargin=True,
            secondary_y=False,
        )
    else:
        fig.update_yaxes(
            title_text="<b>WACK</b>",
            automargin=True,
            secondary_y=False,
        )

    fig.update_yaxes(
        title_text="<b>PTF-SMF</b>",
        visible=False,
        secondary_y=True,
        showgrid=False
    )

    fig.update_layout(width=2000,
                      height=600,
                      legend=dict(yanchor="top",
                                  y=0.99,
                                  xanchor="left",
                                  x=0.01
                                  )
                      )

    fig.layout.template = 'plotly_white'

    return fig


app.run_server(debug=True)




