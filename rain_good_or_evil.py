from dash import Dash, dcc, Output, Input  
import dash_bootstrap_components as dbc    
import plotly.express as px
import pandas as pd              


df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Other/Dash_Introduction/intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])




app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])
mytitle = dcc.Markdown(children='Rain: Good or Evil?')
graph_left = dcc.Graph(figure={})
graph_right = dcc.Graph(figure={})
dropdown = dcc.Dropdown(
                 options=[
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018}],
                 multi=False,
                 value=2015,
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
    dff = dff[dff["Year"] == option_slctd]
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )

    df2 = px.data.tips() # replace with your own data source
    fig2 = px.histogram(
        df2, x="total_bill", y="tip", color="sex",
        range_x=[-5, 60],
        hover_data=df2.columns)


    return fig, fig, fig2


if __name__=='__main__':
    app.run_server(debug=True, port=8054)