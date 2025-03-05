import dash
from dash import html
import dash_leaflet as dl
import pandas as pd

data = {
    'lat': [],
    'lon': [],
    'label': []
}



app = dash.Dash(__name__)
