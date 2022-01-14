# Import required libraries
from ast import Return
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
sites = spacex_df['Launch Site'].unique()
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options = [
                                    {'label':'All sites','value':'ALL'},
                                    {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                    {'label':'	CCAFS SLC-40','value':'	CCAFS SLC-40'},
                                    {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                    {'label':'	VAFB SLC-4E','value':'	VAFB SLC-4E'}
                                ],                               
                                value = 'ALL',
                                placeholder = 'Place holder here',
                                searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=spacex_df['Payload Mass (kg)'].min(), 
                                max=10000, step=1000,
                                marks={0:'0',2000:'2000',7500:'7500',10000:'10000'},
                                value=[spacex_df['Payload Mass (kg)'].min(),spacex_df['Payload Mass (kg)'].max()]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# add callback decorator
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site== 'ALL':
        data = spacex_df.groupby('Launch Site')['class'].count().reset_index()
        fig = px.pie(data,values='class',
        names= 'Launch Site',
        title='Total success launches by sites')
        return fig
    else:
        data = spacex_df[spacex_df['Launch Site']==entered_site]
        df = data['class'].value_counts().reset_index()
        fig = px.pie(df,values='class',
        names= 'class',
        title='Total success launches for site %s'%(entered_site))
        return fig     

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id='payload-slider',component_property='value'))
def get_scatter(launch,slider):
    low, high = slider
    if launch == 'ALL':
        range = (spacex_df['Payload Mass (kg)']>low) & (spacex_df['Payload Mass (kg)']<high)
        df = spacex_df[range]
    else:
        data = spacex_df[spacex_df['Launch Site']==launch]
        range = (data['Payload Mass (kg)']>low) & (data['Payload Mass (kg)']<high)
        df = data[range]    
    fig = px.scatter(df, y='class',x='Payload Mass (kg)',color='Booster Version Category')
    return fig
 
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
