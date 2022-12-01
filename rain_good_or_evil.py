from dash import Dash, dcc, Output, Input  
import dash_bootstrap_components as dbc   
import plotly.express as px
import pandas as pd      


df = pd.read_csv("data_rain_csv.csv")

df = df.groupby(['State', 'Month','value', 'state_code'])[['Rain']].mean()
df.reset_index(inplace=True)
print(df[:5])




app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



mytitle = dcc.Markdown(children='Rain: Good or Evil? A Geospatial Implementation With Customisable Glyphs')

graph_left = dcc.Graph (figure={}) 
graph_right = dcc.Graph(figure={})

dropdown_left = dcc.Dropdown(
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

dropdown_right = dcc.Dropdown(
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
    ], className='heading'),
    dbc.Row([
        dbc.Col([graph_left]),
        dbc.Col([graph_right])
    ]),
    dbc.Row([
        dbc.Col([dropdown_left], width=6),
        dbc.Col([dropdown_right], width=6)
    ]),
    dbc.Row([
        dbc.Col([distplot])
    ], className='bar')
], fluid=True)


@app.callback(
    Output(graph_right, 'figure'),
    Input(dropdown_right, 'value')
)
def update_graph_right(option_slcted_right):
    print(option_slcted_right)
    print(type(option_slcted_right))
    dff = df.copy()
    dff = dff[dff["value"] == option_slcted_right]

    fig_right = px.choropleth(
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

    fig_right.update_layout(geo=dict(bgcolor= '#152236'))
    fig_right.update_layout({
    'paper_bgcolor': 'rgba(0,0,0,0)'
})
    return fig_right


@app.callback(
    Output(graph_left, 'figure'),
    Output(distplot, "figure"), 
    Input(dropdown_left, 'value')
)
def update_graph_left(option_slctd_left):
    print(option_slctd_left)
    print(type(option_slctd_left))

    dff = df.copy()
    dff = dff[dff["value"] == option_slctd_left]

    fig_left = px.choropleth(
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

    fig_left.update_layout(geo=dict(bgcolor= '#152236'))
    fig_left.update_layout({
    'paper_bgcolor': 'rgba(0,0,0,0)'
})

    fig2 = px.histogram(
        df, x="State", y="Rain", color="Month",
        hover_data=df.columns
        )

    fig2.update_layout({
    'plot_bgcolor': '#152336',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})

    return fig_left, fig2


if __name__=='__main__':
    app.run_server(debug=True, port=8054)
