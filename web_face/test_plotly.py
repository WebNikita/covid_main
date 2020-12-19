import plotly

import pandas as pd
import numpy as np
import json

import plotly.express as px
import plotly.io as pi



def create_map(file):
    print(file)
    fig = px.scatter_mapbox(file,lat="Долгота", lon="Широта", hover_name="Город", size="Размер",color='Цвет',hover_data=["Кол-во заболевших"], zoom=6, height=700)
    print(fig)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def create_graph(list_y, text):
    df = px.data.stocks(indexed=True)-1
    fig = dict({
    "data": [{"type": "bar",
              "x": df.index,
              "y": list_y}],
    "layout": {"title": {"text": text}}
    })
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
    
    # print(df.index)
    # fig = px.bar(df, x=df.index, y=["GOOG"])


