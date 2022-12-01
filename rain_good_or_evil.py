from dash import Dash, dcc, Output, Input,html 
import dash_bootstrap_components as dbc   
import plotly.express as px
import pandas as pd      
import plotly.graph_objects as go
      

df = pd.read_csv("data_rain_csv.csv")
df_car = df.groupby(['State', 'value','Month', 'state_code'])[['car']].mean()
df_rain= df.groupby(['State', 'value','Month', 'state_code'])[['Rain']].mean()
df_economic= df.groupby(['State', 'value','Month', 'state_code'])[['economic']].mean()
df_airline = df.groupby(['State', 'value','Month', 'state_code'])[['Airline']].mean()
df_all = df.groupby(['State', 'value','Month', 'state_code', 'car', 'economic', 'Airline'])[['Rain']].mean()
df_car.reset_index(inplace=True)
df_rain.reset_index(inplace=True)
df_economic.reset_index(inplace=True)
df_airline.reset_index(inplace=True)
df_all.reset_index(inplace=True)

# print(df[:5])

df_bubble = px.data.gapminder().query("year==2007")



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])




mytitle = dcc.Markdown(children='Rain: Good or Evil? A Geospatial Implementation With Customisable Glyphs')
graph_left = dcc.Graph(figure={})
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
                     {"label": "Car Accidents", "value": 1},
                     {"label": "Economic Impact", "value": 2},
                     {"label": "Flight Cancellations", "value": 3},
                     ],
                 multi=False,
                 value=3,
                 style={'width': "40%"})

dropdown_scatter = dcc.Dropdown(
                 options=[
                     {'label': i, 'value': i} for i in df_all.State.unique()
                ],
                 multi=True,                 
                 searchable=True,
                 clearable= True,
                 placeholder="Select a state",
                 value='Florida',
                 style={'width': "40%"})

distplot = dcc.Graph(figure={})

sunburst = dcc.Graph(figure={})

scatter = dcc.Graph(figure={})


card_high_rain=  dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Highest Rainfall", className="card-title"),
                    html.H5(
                        ["State",
                        dbc.Alert(id="rainfall_high"),
                        "Value",
                        dbc.Alert(id="rainfall_high_value")
                        ],
                        className="card-text",
                    ),
                    
                ]
            ),
            className="w-50",
        )

card_low_rain=  dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Lowest Rainfall", className="card-title"),
                    html.H5(
                        ["State",
                        dbc.Alert(id="rainfall_low"),
                        "Value",
                        dbc.Alert(id="rainfall_low_value")
                        ],
                        className="card-text",
                        
                    ),
                  
                ]
            ),
            className="w-50",
        )

card_low_fill=  dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Lowest Instances", className="card-title"),
                    html.H5(
                        ["State",
                        dbc.Alert(id="fill_low"),
                        "Value",
                        dbc.Alert(id="fill_low_value")
                        ],
                        className="card-text",
                        
                    ),
                ]
            ),
            className="w-50",
        )
card_high_fill=  dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Highest Instances", className="card-title"),
                    html.H5(
                        ["State",
                        dbc.Alert(id="fill_high"),
                        "Value",
                        dbc.Alert(id="fill_high_value")
                        ],
                        className="card-text",
                        
                    ),
                ]
            ),
            className="w-50",
        )




app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle])
    ], className='text-center text-primary mb-2'),
    dbc.Row([
        dbc.Col([graph_left]),
        dbc.Col([graph_right]),
    ]),
    dbc.Row([
        dbc.Col([dropdown_left], width=6),
        dbc.Col([dropdown_right], width=6)
    ], justify='center'),
      dbc.Row([
        dbc.Col([card_high_rain]),
        dbc.Col([card_low_rain]),
        dbc.Col([card_high_fill]),
        dbc.Col([card_low_fill]),
    ]),
    dbc.Row([
        dbc.Col([distplot]),
    ]),
    dbc.Row([
        dbc.Col([sunburst]),
    ], justify='center'),
    dbc.Row([
        dbc.Col([dropdown_scatter], width=12),
    ], justify='center'),
    dbc.Row([
        dbc.Col([scatter]),
    ], justify='center')  
], fluid=True)


@app.callback(
    Output(graph_right, 'figure'),
    Output('fill_low', 'children'),
    Output('fill_low_value', 'children'),
    Output('fill_high', 'children'),
    Output('fill_high_value', 'children'),
    Input(dropdown_right, 'value')
)
def update_graph_right(option_slcted_right):
    print(option_slcted_right)
    print(type(option_slcted_right))
    if(option_slcted_right == 1):
        dff = df_car.copy()              
        print(dff[:5])
        #dff = dff[dff["value"] == option_slcted_right]
        max_value =dff.max().values
        min_value = dff.min().values
        print(max_value)
        print(min_value)
        fig_right = px.choropleth(
            data_frame=dff,
            locationmode='USA-states',
            locations='state_code',
            scope="usa",
            color='car',
            hover_data=['State'],
            color_continuous_scale=px.colors.sequential.YlOrRd,
            labels={'Car Accidentts': 'Car Accidents'},
            template='plotly_dark',
            animation_frame='Month'
            )
    elif(option_slcted_right == 2):
      dff = df_economic.copy()
      #dff = dff[dff["value"] == option_slcted_right]
      max_value =dff.max().values
      min_value = dff.min().values
      print(max_value)
      print(min_value)
      fig_right = px.choropleth(
           data_frame=dff,
           locationmode='USA-states',
           locations='state_code',
           scope="usa",
           color='economic',
           hover_data=['State'],
           color_continuous_scale=px.colors.sequential.YlOrRd,
           labels={'car': 'Amount of rainfall'},
           template='plotly_dark',
           animation_frame='Month'
    )

    elif(option_slcted_right == 3):
      dff = df_airline.copy()
      print(dff[:5])
      #dff = dff[dff["value"] == option_slcted_right]
      max_value =dff.max().values
      min_value = dff.min().values
      print(max_value)
      print(min_value)
      fig_right = px.choropleth(
           data_frame=dff,
           locationmode='USA-states',
           locations='state_code',
           scope="usa",
           color='Airline',
           hover_data=['State'],
           color_continuous_scale=px.colors.sequential.YlOrRd,
           labels={'car': 'Amount of rainfall'},
           template='plotly_dark',
           animation_frame='Month'
    )



    return fig_right,min_value[0], min_value[4], max_value[0], max_value[4]



@app.callback(
    Output(graph_left, 'figure'),
    Output('rainfall_high', 'children'),
    Output('rainfall_high_value', 'children'),
    Output('rainfall_low', 'children'),
    Output('rainfall_low_value', 'children'),
    Output(distplot, "figure"), 
    Output(sunburst, 'figure'),
    Output(scatter, 'figure'), 
    Input(dropdown_scatter, 'value')
    #Input(dropdown_left, 'value')
)
def update_graph_left(option_slctd_left):

    #print(option_slctd_left)
    #print(type(option_slctd_left))
    dff = df_rain.copy()
    #dff = dff[dff["value"] == option_slctd_left]
    # Plotly Express
    max_value =dff.max().values
    min_value = dff.min().values
    fig_left = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Rain',
        hover_data=['State'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Rain': 'Amount of rainfall'},
        template='plotly_dark',
        animation_frame='Month'
    )

    fig_left.update_layout(geo=dict(bgcolor= '#152236'))   # Left Map Colours
    fig_left.update_layout({
    'paper_bgcolor': '#152336'})



    fig2 = px.histogram(
        df, x="State", y="Rain", color="Month",
        hover_data=df.columns)
    fig2.update_layout(
        font=dict(
            family="Lucida Sans",
            size=12,
            color="white"
        ),
    )
    fig2.update_layout({
    'paper_bgcolor': '#152336',
    'plot_bgcolor':'#152336'
    })
    fig2.update_layout(
        font=dict(
            family="Lucida Sans",
            size=12,
            color="white"
        ),
    )

    
    fig3 = px.sunburst(df_all, path=['State', 'Month'], values='Rain', color='State') 

    dff = df_all.copy()
    dff = df_all[df_all.State.str.contains('|'.join(option_slctd_left))]
    fig4 = px.scatter(
        dff, x="car", y="economic", animation_group="State",
           size="Rain", color="Month", hover_name="State", facet_col="Month",
           size_max=50, range_x=[-300000, 300000], range_y=[-1000000, 4000000])


    return fig_left, max_value[0], max_value[4] ,min_value[0], min_value[4],fig2, fig3, fig4


if __name__=='__main__':
    app.run_server(debug=True, port=8000)
