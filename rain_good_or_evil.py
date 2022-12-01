from dash import Dash, dcc, Output, Input,html 
import dash_bootstrap_components as dbc   
import plotly.express as px
import pandas as pd      
import plotly.graph_objects as go


df = pd.read_csv("data_rain_csv.csv")
df_car = df.groupby(['State', 'value','Month', 'state_code'])[['car']].mean()
df_rain= df.groupby(['State', 'value','Month', 'state_code'])[['Rain']].mean()
df_car.reset_index(inplace=True)
df_rain.reset_index(inplace=True)
print(df[:5])

df_bubble = px.data.gapminder().query("year==2007")



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
                     {"label": "Rain", "value": 1},
                     {"label": "Car", "value": 2},
                     ],
                 multi=False,
                 value=1,
                 style={'width': "40%"})

distplot = dcc.Graph(figure={})


card_high_rain=  dbc.Card(
            dbc.CardBody(
                [
                    html.H5("50% width card", className="card-title"),
                    html.P(
                        [
                            "This card uses the ",
                            html.Code("w-50"),
                            " class to set the width to 50%",
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
                    html.H5("50% width card", className="card-title"),
                    html.P(
                        [
                            "This card uses the ",
                            html.Code("w-50"),
                            " class to set the width to 50%",
                        ],
                        className="card-text",
                    ),
                    dbc.Alert(id="upload-alert")
                ]
            ),
            className="w-50",
        )

card_high_fill=  dbc.Card(
            dbc.CardBody(
                [
                    html.H5("50% width card", className="card-title"),
                    html.P(
                        [
                            "This card uses the ",
                            html.Code("w-50"),
                            " class to set the width to 50%",
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
                    html.H5("50% width card", className="card-title"),
                    html.P(
                        [
                            "This card uses the ",
                            html.Code("w-50"),
                            " class to set the width to 50%",
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
        dbc.Col([card_high_rain]),
        dbc.Col([card_low_rain]),
        dbc.Col([card_high_fill]),
        dbc.Col([card_low_fill]),
    ]),
    dbc.Row([
        dbc.Col([distplot])
    ], className='bar')
], fluid=True)


@app.callback(
    Output(graph_right, 'figure'),
    Output('upload-alert', 'children'),
    Input(dropdown_right, 'value')
)
def update_graph_right(option_slcted_right):
    print(option_slcted_right)
    print(type(option_slcted_right))
    if(option_slcted_right == 1):
        dff = df_rain.copy()
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
            color='Rain',
            hover_data=['State'],
            color_continuous_scale=px.colors.sequential.YlOrRd,
            labels={'Rain': 'Amount of rainfall'},
            template='plotly_dark',
            animation_frame='Month'
            )
    elif(option_slcted_right == 2):
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
           color_continuous_scale=px.colors.sequential.YlOrRd,
           labels={'car': 'Amount of rainfall'},
           template='plotly_dark',
           animation_frame='Month'   
    )

    return fig_right, max_value[4]
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

    #print(option_slctd_left)
    #print(type(option_slctd_left))

    dff = df_rain.copy()
    #dff = dff[dff["value"] == option_slctd_left]
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
    app.run_server(debug=True, port=8000)
