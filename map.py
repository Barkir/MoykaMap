import dash
from dash import html
import dash_leaflet as dl
import pandas as pd
import os

os.system("python sheet.py")

file2arr = [k.rstrip().split(';') for k in open("coord.txt").readlines()]
boobs = dict(
    iconUrl='./assets/car-wash.png',
    iconSize=[50, 50],
    iconAnchor=[15, 15],
    popupAnchor=[0, -15],
)

data = {
    'label': [k[0] for k in file2arr],
    'lat': [k[1] for k in file2arr],
    'lon': [k[2] for k in file2arr],
}

df = pd.DataFrame(data)


app = dash.Dash(__name__)

markers = [dl.Marker(icon=boobs,
                     position=[row['lat'], row['lon']],
                     children=[
                         dl.Tooltip(row['label']),
                         dl.Popup(
                             [html.Div(
                                 [html.H4("Москва", style={'color': '#2c3e50', 'margin': '0'}),
                            html.P("Столица России", style={'color': '#7f8c8d', 'margin': '5px 0'}),]
                             )]
                         )
                     ]) for index, row in df.iterrows()]

app.layout = html.Div([dl.Map([dl.TileLayer(
    url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    attribution='Tiles © Esri'

), dl.FullScreenControl(), *markers],
                              center=[55.751244, 37.618423],
                              zoom=13,
                              minZoom=12,
                              maxZoom=20,
                              style={'height' : '100vh'})])


if __name__ == '__main__':
    app.run_server(debug=True, port=5000, host='0.0.0.0')

