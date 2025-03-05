import dash
from dash import html
import dash_leaflet as dl
import pandas as pd

file2arr = [k.rstrip().split(';') for k in open("coord.txt").readlines()]
boobs = dict(
    iconUrl='./assets/female.png',
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

markers = [dl.Marker(icon=boobs, position=[row['lat'], row['lon']], children=dl.Tooltip(row['label'])) for index, row in df.iterrows()]

app.layout = html.Div([dl.Map(center=[55.751244, 37.618423],
                              zoom=4,
                              children=[dl.TileLayer(),  *markers],
                              style={'width' : '100%', 'height' : '50vh', 'margin' : 'auto', 'display' : 'block'})])


if __name__ == '__main__':
    app.run_server(debug=True, port=5000, host='0.0.0.0')

