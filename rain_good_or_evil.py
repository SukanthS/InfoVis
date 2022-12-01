from dash import Dash, dcc, Output, Input,html 
import dash_bootstrap_components as dbc   
import plotly.express as px
import pandas as pd      
import plotly.graph_objects as go
      
# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Page 1", href="#")),
#         dbc.DropdownMenu(
#             children=[
#                 dbc.DropdownMenuItem("More pages", header=True),
#                 dbc.DropdownMenuItem("Page 2", href="#"),
#                 dbc.DropdownMenuItem("Page 3", href="#"),

# ALL ABOUT THE DATA
df = pd.read_csv("data_rain_csv.csv")
df_car = df.groupby(['State', 'value','Month', 'state_code'])[['car']].mean()
df_rain= df.groupby(['State', 'value','Month', 'state_code'])[['Rain']].mean()
df_economic= df.groupby(['State', 'value','Month', 'state_code'])[['economic']].mean()
df_all = df.groupby(['State', 'value','Month', 'state_code', 'car', 'economic'])[['Rain']].mean()
df_car.reset_index(inplace=True)
df_rain.reset_index(inplace=True)
df_economic.reset_index(inplace=True)
df_all.reset_index(inplace=True)
print(df[:5])

df_bubble = px.data.gapminder().query("year==2007")



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])




mytitle = dcc.Markdown(children='Rain: Good or Evil? A Geospatial Implementation With Customisable Glyphs')

# THE TWO MAPS
graph_left = dcc.Graph(figure={})
graph_right = dcc.Graph(figure={})

# DROPDOWN TEXT
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
                 style={'width': "100%"})
dropdown_right = dcc.Dropdown(
                 options=[
                     {"label": "Car", "value": 1},
                     {"label": "economic", "value": 2},
                     ],
                 multi=False,
                 value=1,
                 style={'width': "100%"})

            
# THE GRAPHS
distplot = dcc.Graph(figure={})

sunburst = dcc.Graph(figure={})

scatter = dcc.Graph(figure={})

# CARDS
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



# GRID LAYOUT
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle])
    ], className='heading'),
    dbc.Row([
        dbc.Col([graph_left]),
        dbc.Col([graph_right]),
    ]),
    dbc.Row([
        dbc.Col([dropdown_left],className='mapdrop', width=6),
        dbc.Col([dropdown_right], className='mapdrop2',width=6)
    ], justify='center'),
      dbc.Row([
        dbc.Col([card_high_rain], className='cardStyle'),
        dbc.Col([card_low_rain], className='cardStyle'),
        dbc.Col([card_high_fill], className='cardStyle'),
        dbc.Col([card_low_fill], className='cardStyle'),
    ], className='cardRow'),

    dbc.Row([
        dbc.Col([distplot]),
    ], className='bar'),
    dbc.Row([
        dbc.Col([sunburst]),
    ], className='sun', justify='center'),
    dbc.Row([
        dbc.Col([scatter]),
    ], className='scatter', justify='center')  
], fluid=True)


# CALLBACKS FOR RIGHT MAP
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
            color_continuous_scale=px.colors.sequential.Burgyl,
            labels={'Rain': 'Amount of Rainfall'},
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
      fig_right = px.choropleth(        #Choropleth Details
           data_frame=dff,
           locationmode='USA-states',
           locations='state_code',
           scope="usa",
           color='economic',
           hover_data=['State'],
           color_continuous_scale=px.colors.sequential.Purpor,
           labels={'car': 'Amount of Rainfall'},
           template='plotly_dark',
           animation_frame='Month'
    )
    fig_right.update_layout(geo=dict(bgcolor= '#152236'))   # Right Map Colours
    fig_right.update_layout({
    'paper_bgcolor': '#152336'})

    return fig_right,min_value[0], min_value[4], max_value[0], max_value[4]


# OUTPUT CALLBACK
@app.callback(
    Output(graph_left, 'figure'),
    Output('rainfall_high', 'children'),
    Output('rainfall_high_value', 'children'),
    Output('rainfall_low', 'children'),
    Output('rainfall_low_value', 'children'),
    Output(distplot, "figure"), 
    Output(sunburst, 'figure'),
    Output(scatter, 'figure'), 
    Input(dropdown_left, 'value')
)

# MAP ON LEFT
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
        labels={'Rain': 'Amount of Rainfall'},
        template='plotly_dark',
        animation_frame='Month'
    )

    fig_left.update_layout(
        font=dict(
            family="Lucida Sans",
            color="white"
        ),
    )


# HISTOGRAM DETAILS
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


# SUNBURST DETAILS
    fig3 = px.sunburst(df_all, path=['State', 'Month'], values='Rain', color='State') 
    fig3.update_layout({
    'paper_bgcolor': '#152336',
    'plot_bgcolor':'#152336'
    })
    fig3.update_layout(
        font=dict(
            family="Lucida Sans",
            size=12,
            color="white"
        ),
    )

# SCATTERPLOT DETAILS
    fig4 = px.scatter(
        df_all, x="car", y="economic", animation_group="State",
           size="Rain", color="Month", hover_name="State", facet_col="Month",
           size_max=0.99999, range_x=[0.00000,0.99999], range_y=[0.00,5000.00])
    fig4.update_layout({
    'paper_bgcolor': '#152336',
    'plot_bgcolor':'#152336'
    })
    fig4.update_layout(
        font=dict(
            family="Lucida Sans",
            size=12,
            color="white"
        ),
    )


    return fig_left, max_value[0], max_value[4] ,min_value[0], min_value[4],fig2, fig3, fig4


if __name__=='__main__':
    app.run_server(debug=True, port=8000)
