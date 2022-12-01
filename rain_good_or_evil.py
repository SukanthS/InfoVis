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
df_water = df.groupby(['State', 'value','Month', 'state_code'])[['Water']].mean()
df_air = df.groupby(['State', 'value','Month', 'state_code'])[['Air']].mean()
df_all = df.groupby(['State', 'value','Month', 'state_code', 'car', 'economic', 'Airline','Water','Air', 'vals'])[['Rain']].mean()
df_car.reset_index(inplace=True)
df_rain.reset_index(inplace=True)
df_economic.reset_index(inplace=True)
df_airline.reset_index(inplace=True)
df_water.reset_index(inplace=True)
df_air.reset_index(inplace=True)
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
                 style={'width': "75%"})
dropdown_right = dcc.Dropdown(
                 options=[
                     {"label": "Car Accidents", "value": 1},
                     {"label": "Economic Impact", "value": 2},
                     {"label": "Flight Cancellations", "value": 3},
                     {"label": "Groudwater Level", "value": 4},
                     {"label": "Air Quality Index", "value": 5},
                     ],
                 multi=False,
                 value=1,
                 style={'width': "75%"})

dropdown_scatter = dcc.Dropdown(
                 options=[
                     {'label': i, 'value': i} for i in df_all.State.unique()
                ],
                 multi=True,                 
                 searchable=True,
                 clearable= True,
                 placeholder="Select a state",
                 value='Florida',
                 style={'width': "100%"})

distplot = dcc.Graph(figure={})

#sunburst = dcc.Graph(figure={})

scatter = dcc.Graph(figure={})

#linegraph = dcc.Graph()
parplot = dcc.Graph()

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
            className="w-100",
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
            className="w-100",
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
            className="w-100",
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
            className="w-100",
        )

graph_desc = dcc.Markdown(className='desc')


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle], className="title")
    ], className='heading'),
    dbc.Row([
        dbc.Col([dropdown_left], className="mapdrop", width=6),
        dbc.Col([dropdown_right],className="mapdrop2", width=6)
    ]),
    dbc.Row([
        dbc.Col([graph_left]),
        dbc.Col([graph_right]),
    ]),
      dbc.Row([
        dbc.Col([card_high_rain], class_name="cardStyle"),
        dbc.Col([card_low_rain], class_name="cardStyle"),
        dbc.Col([card_high_fill], class_name="cardStyle"),
        dbc.Col([card_low_fill], class_name="cardStyle"),
    ], class_name="cardRow"),
    dbc.Row([
        dbc.Col([graph_desc], className="title")
    ], className='heading'),
    dbc.Row([
        dbc.Col([distplot]),
    ], class_name="bar"),
    dbc.Row([
        dbc.Col([dropdown_scatter], className="scatterDrop"),
    ]),
    dbc.Row([
        dbc.Col([parplot], class_name="par"),
        dbc.Col([scatter], class_name="scatter"),
    ], className="compare"),
    
    # dbc.Row([
    #     dbc.Col([scatter]),
    # ], class_name="scatter", justify='center')  
], fluid=True)


@app.callback(
    Output(graph_right, 'figure'),
    Output('fill_low', 'children'),
    Output('fill_low_value', 'children'),
    Output('fill_high', 'children'),
    Output('fill_high_value', 'children'),
    Output(distplot, "figure"), 
    Input(dropdown_right, 'value')
)

def update_graph_right(option_slcted_right):
    print(option_slcted_right)
    print(type(option_slcted_right))
    if(option_slcted_right == 1):
        dff = df_car.copy()  
        flag = "car"            
        print(dff[:5])
        #dff = dff[dff["value"] == option_slcted_right]
        # max_value =dff.max().values
        # min_value = dff.min().values
        max_value_state = 'South Carolina'
        max_value_value = '3874'
        min_value_state = 'Massachusetts'
        min_value_value = '129'
        fig_right = px.choropleth(
            data_frame=dff,
            locationmode='USA-states',
            locations='state_code',
            scope="usa",
            color='car',
            hover_data=['State'],
            color_continuous_scale=px.colors.sequential.Sunsetdark,
            labels={'car': 'Car Accidents'},
            template='plotly_dark',
            animation_frame='Month'
            )
    elif(option_slcted_right == 2):
      dff = df_economic.copy()
      flag = "economic"
      #dff = dff[dff["value"] == option_slcted_right]
    #   max_value =dff.max().values
    #   min_value = dff.min().values
      max_value_state = 'California'
      max_value_value = '2942968.5'
      min_value_state = 'Vermont'
      min_value_value = '30094'
      fig_right = px.choropleth(
           data_frame=dff,
           locationmode='USA-states',
           locations='state_code',
           scope="usa",
           color='economic',
           hover_data=['State'],
           color_continuous_scale=px.colors.sequential.BuGn,
           labels={'economic': 'Economic impact'},
           template='plotly_dark',
           animation_frame='Month'
    )

    elif(option_slcted_right == 3):
      dff = df_airline.copy()
      flag = 'Airline'
      print(dff[:5])
      #dff = dff[dff["value"] == option_slcted_right]
    #   max_value =dff.max().values
    #   min_value = dff.min().values
      max_value_state = 'New York'
      max_value_value = '112'
      min_value_state = 'Hawaii'
      min_value_value = '9'
      fig_right = px.choropleth(
           data_frame=dff,
           locationmode='USA-states',
           locations='state_code',
           scope="usa",
           color='Airline',
           hover_data=['State'],
           color_continuous_scale=px.colors.sequential.Magenta,
           labels={'Airline': 'Cancellations'},
           template='plotly_dark',
           animation_frame='Month'
    )

    elif(option_slcted_right == 4):
      dff = df_water.copy()
      flag = 'Water'
    #   print(dff[:5])
      #dff = dff[dff["value"] == option_slcted_right]
    #   max_value =dff.max().values
    #   min_value = dff.min().values
      max_value_state = 'Alaska'
      max_value_value = '54'
      min_value_state = 'Iowa'
      min_value_value = '11'
      fig_right = px.choropleth(
           data_frame=dff,
           locationmode='USA-states',
           locations='state_code',
           scope="usa",
           color="Water",
           hover_data=['State'],
           color_continuous_scale=px.colors.sequential.Brwnyl,
           labels={'Water': 'Groundwater'},
           template='plotly_dark',
           animation_frame='Month'
    )

    elif(option_slcted_right == 5):
      dff = df_air.copy()
      flag = 'Air'
      print(dff[:5])
      #dff = dff[dff["value"] == option_slcted_right]
    #   max_value =dff.max().values
    #   min_value = dff.min().values
      max_value_state = 'Utah'
      max_value_value = '53.2'
      min_value_state = 'Hawaii'
      min_value_value = '20.5'
      fig_right = px.choropleth(
           data_frame=dff,
           locationmode='USA-states',
           locations='state_code',
           scope="usa",
           color='Air',
           hover_data=['State'],
           color_continuous_scale=px.colors.sequential.Purpor,
           labels={'Air': 'Quality Index'},
           template='plotly_dark',
           animation_frame='Month'
    )
    fig_right.update_layout(geo=dict(bgcolor= '#152236'))   # Left Map Colours
    fig_right.update_layout({
    'paper_bgcolor': '#152336'})


    fig2 = px.histogram(
        df, x="State", y=flag, color="Month",
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
   


    return fig_right,min_value_state, min_value_value, max_value_state, max_value_value, fig2


@app.callback(
    Output(graph_left, 'figure'),
    Output('rainfall_high', 'children'),
    Output('rainfall_high_value', 'children'),
    Output('rainfall_low', 'children'),
    Output('rainfall_low_value', 'children'),
    #Output(sunburst, 'figure'),
    Output(parplot, 'figure'), 
    Output(scatter, 'figure'), 
    Output(graph_desc,'children'),
    Input(dropdown_scatter, 'value'),
    Input(dropdown_right,'value')
    #Input(dropdown_left, 'value')
)
def update_graph_left(option_slctd_left,category):
    
    if(category == 1):
        value = 'car'
        desc = 'Statewise comparison of car accidents'
    elif(category == 2):
        value = 'economic'
        desc = 'Statewise comparison of economic impact'
    elif(category == 3):
        value = 'Airline'
        desc = 'Statewise comparison of flight cancellations'
    elif(category == 4):
        value = 'Water'
        desc = 'Statewise comparison of groundwater level'
    elif(category == 5):
        value = 'Air'
        desc = 'Statewise comparison of Air Quality Index'

    #print(option_slctd_left)
    #print(type(option_slctd_left))
    dff = df_rain.copy()
    #dff = dff[dff["value"] == option_slctd_left]
    # Plotly Express
    max_value_state = 'Louisiana'
    max_value_value = '0.96'
    min_value_state = 'Nevada'
    min_value_value = '0.06'
    fig_left = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Rain',
        hover_data=['State'],
        color_continuous_scale=px.colors.sequential.Burgyl,
        labels={'Rain': 'Amount of rainfall'},
        template='plotly_dark',
        animation_frame='Month'
    )

    fig_left.update_layout(geo=dict(bgcolor= '#152236'))   # Left Map Colours
    fig_left.update_layout({
    'paper_bgcolor': '#152336'})


    dff = df_all.copy()
    dff = df_all[df_all.State.str.contains('|'.join(option_slctd_left))]

    #fig3 = px.line(dff, x="Rain", y=value, color='State')
    #fig3.update_layout(
    #    font=dict(
    #        family="Lucida Sans",
    #        size=12,
    #        color="white"
    #    ),
    #)
    #fig3.update_layout({
    #'paper_bgcolor': '#152336',
    #'plot_bgcolor':'#152336'
    #})

    dfff = df_all.copy()
    dfff = df_all[df_all.State.str.contains('|'.join(option_slctd_left))]

    dfff = dfff[dfff.Month.str.contains('|'.join(['January']))]
    

    fig5 = px.parallel_coordinates(
        dfff, 
        color='vals', 
        dimensions= ["Rain", "car", "economic", "Airline", "Air" ])
    fig5.update_layout(
        font=dict(
            family="Lucida Sans",
            size=12,
            color="white"
        ),
    )
    fig5.update_layout({
    'paper_bgcolor': '#152336',
    'plot_bgcolor':'#152336'
    })


    fig4 = px.scatter(
        dff, x="car", y="economic", animation_group="State", 
           size="Rain", color="Month", hover_name="State", facet_col="Month", facet_col_wrap=3,
           size_max=17, range_x=[-100000, 100000], range_y=[-250000, 2000000])
    fig4.update_layout(
        font=dict(
            family="Lucida Sans",
            size=12,
            color="white"
        ),
    )
    fig4.update_layout({
    'paper_bgcolor': '#152336',
    'plot_bgcolor':'#152336'
    })


    return fig_left, max_value_state, max_value_value , min_value_state, min_value_value, fig5, fig4, desc


if __name__=='__main__':
    app.run_server(debug=True, port=8000)