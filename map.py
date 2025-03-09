import dash
from dash import html, dcc
import dash_leaflet as dl
import pandas as pd
from dash.dependencies import Input, Output
import os

file2arr = [k.rstrip().split(';') for k in open("coord.txt").readlines()]
car_wash = dict(
    iconUrl='./assets/car-wash.png',
    iconSize=[50, 50],
    iconAnchor=[15, 15],
    popupAnchor=[0, -15],
)

data = {
    'label': [k[0] for k in file2arr],
    'lat': [k[1] for k in file2arr],
    'lon': [k[2] for k in file2arr],
    'type': [k[3] for k in file2arr],
    'tel': [k[4] for k in file2arr],
    'url': [k[5] for k in file2arr]
}

df = pd.DataFrame(data)


app = dash.Dash(__name__)

markers = [dl.Marker(
                    id=f'marker-{index}',
                    icon=car_wash,
                     position=[row['lat'], row['lon']],
                     children=[
                         dl.Popup(
                             [html.Div(
                                 [html.H4(row['tel'], style={'color': '#2c3e50', 'margin': '0'}),
                            html.P(row['type'], style={'color': '#7f8c8d', 'margin': '5px 0'}),]
                             )]
                         )
                     ]) for index, row in df.iterrows()]

app.layout = html.Div(
[
    dl.Map([
        dl.TileLayer(
                        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
                        attribution='Tiles © Esri'),

    dl.FullScreenControl(), *markers],
    center=[55.751244, 37.618423],
    zoom=13,
    minZoom=12,
    maxZoom=20,
    style={'height' : '100vh'}),
    dcc.Location(id='url', refresh=False),
    html.Div(id='marker-click-output')
])

@app.callback(
    Output('marker-click-output', 'children'),  # Изменяем URL
    [Input(f"marker-{i}", "n_clicks") for i in range(len(markers))]
)
def marker_click(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    else:
        marker_id = ctx.triggered[0]['prop_id'].split('.')[0]
        marker_index = int(marker_id.split('-')[-1])

        url = df.iloc[marker_index]['url']

        return dcc.Location(id='dummy-location', href=url, refresh=True)


if __name__ == '__main__':
    app.run_server(debug=True, port=5000, host='0.0.0.0')

