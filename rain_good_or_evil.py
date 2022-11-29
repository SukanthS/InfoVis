from dash import Dash, dcc, Output, Input  
import dash_bootstrap_components as dbc    
import plotly.express as px
import pandas as pd              


df = pd.read_csv("data_rain_csv.csv")

df = df.groupby(['State', 'Month','value', 'state_code'])[['Rain']].mean()
df.reset_index(inplace=True)
print(df[:5])




app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])
mytitle = dcc.Markdown(children='Rain: Good or Evil?')
graph_left = dcc.Graph(figure={})
graph_right = dcc.Graph(figure={})
dropdown = dcc.Dropdown(
                 options=[
                     {"label": "January", "value": 1},
                     {"label": "February", "value": 2},
                     {"label": "March", "value": 3},
                     {"label": "April", "value": 4},
                     {"label": "May", "value": 5},
                     {"label": "June", "value": 6},
                     {"label": "July", "value": 7},
                     {"label": "August", "value": 8},
                     {"label": "September", "value": 9},
                     {"label": "October", "value": 10},
                     {"label": "November", "value": 11},
                     {"label": "December", "value": 12}],
                 multi=False,
                 value=1,
                 style={'width': "40%"})

distplot = dcc.Graph(figure={})




app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle])
    ], justify='center'),
    dbc.Row([
        dbc.Col([graph_left]),
        dbc.Col([graph_right]),
    ]),
    dbc.Row([
        dbc.Col([dropdown], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([distplot]),
    ])
], fluid=True)




@app.callback(
    Output(graph_left, 'figure'),
    Output(graph_right, 'figure'),
    Output(distplot, "figure"), 
    Input(dropdown, 'value')
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    dff = df.copy()
    dff = dff[dff["value"] == option_slctd]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Rain',
        hover_data=['State', 'Rain'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Rain': 'Amount of rainfall'},
        template='plotly_dark'
    )

    fig2 = px.histogram(
        df, x="State", y="Rain", color="Month",
        hover_data=df.columns)


    return fig, fig, fig2


if __name__=='__main__':
    app.run_server(debug=True, port=8054)
