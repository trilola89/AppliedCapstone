import pandas as pd
import dash
from dash import html
from dash import dcc
from plotly import express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output


url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv'
df = pd.read_csv(url)



app = dash.Dash(__name__)

#TODO: TASK 1: Add a Launch Site Drop-down Input Component  
#TODO: TASK 2: Add a callback function to render 'success-pie-chart' based on selected site dropdown
"""launch site is a categorical variable, so we can use a dropdown menu to select a launch site. which will alter the pie chart."""


#TODO: TASK 3: Add a Range Slider to Select Payload
#TODO: TASK 4: Add a callback function to render `success-payload-scatter-chart` based on selected site and payload range
"""Payload is a continuous variable, so we can use a range slider to select a payload range. which will alter the scatter chart."""




app.layout = html.Div(children=
                      [
                        html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 35}),

                        html.Div(children=
                                 [
                            dcc.Dropdown(id='site-dropdown',
                                        options=[
                                            {'label': label, 'value': label} for label in df['Launch Site'].unique()
                                                 ] + [{'label': 'All Sites', 'value': 'All Sites'}],
                                                 value='All Sites',
                                                 placeholder='Select a Launch Site here', searchable=True)
                                 ]),


                        #output pie chart
                        html.Div(id='success-pie-chart'),



                        html.Br(),
                        html.Br(),

                        #next input component
                        html.P("Payload range (Kg):", style={'font-weight': 'bold'}),
                        html.Div(children=[

                            dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[df['Payload Mass (kg)'].min(), df['Payload Mass (kg)'].max()],
                                            marks={i: str(i) for i in range(0, 10001, 2000)})
                                            

                        ]),

                                        
                        #output scatter chart
                        html.Div(id='success-payload-scatter-chart')
                                 
    ])



@app.callback(
    Output(component_id='success-pie-chart', component_property='children'),
    Input(component_id='site-dropdown', component_property='value')
)

def pie_chart(site_dropdown):

    allData = df
    if site_dropdown == 'All Sites':
        allData = allData.groupby(['Launch Site'])['class'].mean().reset_index()
        fig = px.pie(allData, values='class', names='Launch Site', title='Success Rate for All Sites')

    else:

        allData = allData[allData['Launch Site'] == site_dropdown]
        allData = allData['class'].value_counts().reset_index()


        fig = px.pie(allData, values='count', names='class', title='Success Rate for ' + site_dropdown)

    return dcc.Graph(figure=fig)

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='children'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')]
)

def scatter_chart(site_dropdown, payload_slider):

    if site_dropdown == 'All Sites':
        allData = df
        allData = allData[(allData['Payload Mass (kg)'] >= payload_slider[0]) & (allData['Payload Mass (kg)'] <= payload_slider[1])]
        fig = px.scatter(allData, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for All Sites')
    else:
        allData = df[df['Launch Site'] == site_dropdown]
        allData = allData[(allData['Payload Mass (kg)'] >= payload_slider[0]) & (allData['Payload Mass (kg)'] <= payload_slider[1])]
        fig = px.scatter(allData, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for ' + site_dropdown)

    return dcc.Graph(figure=fig)




if __name__ == '__main__':
    app.run_server(debug=True)