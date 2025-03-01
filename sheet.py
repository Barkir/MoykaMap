import dash
from dash import dcc
from dash import html

import requests
from googleapiclient.discovery import build
from google.cloud import language



YANDEX_API_KEY = "23ba9181-ab9f-4c7e-a209-346f4ef7c4a9"

GOOGLE_API_KEY = "AIzaSyCP0qTkrjpSNwfYV9nzyNfxGTj2-LOoizM"
SPREADSHEET_ID = "1__of0_NMbxIDXlKTkcEbV1stP4p7qEKUIDluGWXDEZc"

def sheets_auth(api_key):
    return build('sheets', 'v4', developerKey=api_key).spreadsheets()






# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Graph(
        id='map',
        figure={
            'data': [
                {
                    'type': 'scattermapbox',  # Type of map
                    'lat': [37.7749, 34.0522, 40.7128],  # Latitude coordinates
                    'lon': [-122.4194, -118.2437, -74.0060],  # Longitude coordinates
                    'mode': 'markers',  # Display markers
                    'marker': {'size': 10, 'color': 'red'},  # Marker style
                    'text': ['San Francisco', 'Los Angeles', 'New York'],  # Hover text
                }
            ],
            'layout': {
                'mapbox': {
                    'style': 'open-street-map',  # Map style (can also use Mapbox styles)
                    'center': {'lat': 37.7749, 'lon': -122.4194},  # Center of the map
                    'zoom': 2,  # Zoom level
                },
                'title': 'US Cities Map',  # Title of the map
                'margin': {'l': 0, 'r': 0, 't': 40, 'b': 0},  # Margins
            }
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)