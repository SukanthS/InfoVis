from dash import Dash, dcc, Output, Input  
import dash_bootstrap_components as dbc   
import plotly.express as px
import pandas as pd      

df = pd.read_csv("data_rain_tmp_csv.csv")

df = df.groupby(['State', 'value','Month', 'RainTmp','RainTmp2','Year', 'state_code'])[['Rain']].mean()
#df.reset_index(inplace=False)
df.reset_index(inplace=True)
print(df[:5])




app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



mytitle = dcc.Markdown(children='Rain: Good or Evil? A Geospatial Implementation With Customisable Glyphs')
graph_left = dcc.Graph(figure={})
graph_right = dcc.Graph(figure={})
dropdown_left = dcc.Dropdown(
                 options=[
                     {"label": "2020", "value": 2020},
                     {"label": "2021", "value": 2021}
                     ],
                 multi=False,
                 value=2020,
                 style={'width': "40%"})
dropdown_right = dcc.Dropdown(
                 options=[
                     {"label": "2020", "value": 2020},
                     {"label": "2021", "value": 2021}
                     ],
                 multi=False,
                 value=2020,
                 style={'width': "40%"})

distplot = dcc.Graph(figure={})

sunburst = dcc.Graph(figure={})

scatter = dcc.Graph(figure={})





app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle])
    ], className='heading'),
    dbc.Row([
        dbc.Col([graph_left]),
        dbc.Col([graph_right]),
    ]),
    dbc.Row([
        dbc.Col([dropdown_left], className='mapdrop', width=6),
        dbc.Col([dropdown_right], className='mapdrop2', width=6)
    ]),
    dbc.Row([
        dbc.Col([distplot]),
    ], className='bar'),
    dbc.Row([
        dbc.Col([sunburst]),
    ], justify='center'),
    dbc.Row([
        dbc.Col([scatter]),
    ], justify='center')  
], fluid=True)


@app.callback(
    Output(graph_right, 'figure'),
    Input(dropdown_right, 'value')
)
def update_graph_right(option_slcted_right):
    print(option_slcted_right)
    print(type(option_slcted_right))
    dff = df.copy()
    dff = dff[dff["Year"] == option_slcted_right]
    fig_right = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Rain',
        hover_data=['State', 'Rain'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Rain': 'Amount of rainfall'},
        template='plotly_dark',
        animation_frame='Month'
    )
    fig_right.update_layout(geo=dict(bgcolor= '#152236'))
    fig_right.update_layout({
    'paper_bgcolor': '#152336'})
    return fig_right



@app.callback(
    Output(graph_left, 'figure'),
    Output(distplot, "figure"),
    Output(sunburst, 'figure'),
    Output(scatter, 'figure'), 
    Input(dropdown_left, 'value')
)
def update_graph_left(option_slctd_left):
    print(option_slctd_left)
    print(type(option_slctd_left))

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd_left]

    # Plotly Express
    fig_left = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Rain',
        hover_data=['State', 'Rain'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Rain': 'Amount of rainfall'},
        template='plotly_dark',
        animation_frame='Month'
    )
    fig_left.update_layout(geo=dict(bgcolor= '#152236'))
    fig_left.update_layout({
    'paper_bgcolor': '#152336'
})

    fig2 = px.histogram(
        df, x="State", y="Rain", color="Month",
        hover_data=df.columns, animation_frame='Year')
    fig2.update_layout({
    'plot_bgcolor': '#152336',
    'paper_bgcolor': '#152336'
})


    fig3 = px.sunburst(df, path=['State', 'Month', 'Year','Rain'], values='Rain', color='State') 
    fig3.update_layout({
    'plot_bgcolor': '#152336',
    'paper_bgcolor': '#152336'
})

    fig4 = px.scatter(df, x="RainTmp", y="RainTmp2", animation_frame="Year", animation_group="State",
           size="Rain", color="Month", hover_name="State", facet_col="Month",
           size_max=0.99999, range_x=[0.00000,0.99999], range_y=[0.00000,0.99999])
    fig3.update_layout({
    'plot_bgcolor': '#152336',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})

    return fig_left, fig2, fig3, fig4

if __name__=='__main__':
    app.run_server(debug=True, port=8054)
