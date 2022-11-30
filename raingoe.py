from dash import Dash, dcc, Output, Input  
import dash_bootstrap_components as dbc   
import plotly.express as px
import pandas as pd      
      
# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Page 1", href="#")),
#         dbc.DropdownMenu(
#             children=[
#                 dbc.DropdownMenuItem("More pages", header=True),
#                 dbc.DropdownMenuItem("Page 2", href="#"),
#                 dbc.DropdownMenuItem("Page 3", href="#"),


df = pd.read_csv("data_rain_tmp_csv.csv")

df = df.groupby(['State', 'Month','value','RainTmp','RainTmp2','Year', 'state_code'])[['Rain']].mean()
df.reset_index(inplace=True)
print(df[:5])




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

sunburst = dcc.Graph(figure={})

scatter = dcc.Graph(figure={})





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
        dbc.Col([distplot]),
    ]),
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
        template='plotly_dark',
        animation_frame='Year'
    )

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
    dff = dff[dff["value"] == option_slctd_left]

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
        animation_frame='Year'
    )

    fig2 = px.histogram(
        df, x="State", y="Rain", color="Month",
        hover_data=df.columns, animation_frame='Year')


    fig3 = px.sunburst(df, path=['State', 'Month', 'Year'], values='Rain', color='State') 

    fig4 = px.scatter(df, x="RainTmp", y="RainTmp2", animation_frame="Year", animation_group="State",
           size="Rain", color="Month", hover_name="State", facet_col="Month",
           size_max=0.99999, range_x=[0.00000,0.99999], range_y=[0.00000,0.99999])

    


    return fig_left, fig2, fig3, fig4

if __name__=='__main__':
    app.run_server(debug=True, port=8054)
