# network_viz.py
import networkx as nx
from pyvis.network import Network
import streamlit as st
from config import node_colors
import pandas as pd

def detect_type(value, row):
    if pd.notna(row.get('Gene_symbol', None)) and value == row['Gene_symbol']:
        return "Target"
    elif pd.notna(row.get('Disease_name', None)) and value == row['Disease_name']:
        return "Disease"
    elif pd.notna(row.get('Metabolite_name', None)) and value == row['Metabolite_name']:
        return "Metabolite"
    elif pd.notna(row.get('Food_name', None)) and value == row['Food_name']:
        return "Food"
    else:
        return "Microbe"

def build_network(df, center_colors):
    G = nx.Graph()
    for _, row in df.iterrows():
        prev = row['source']
        if prev not in G:
            G.add_node(prev, label=prev, color=center_colors.get(prev, "#81c784"))
        for col in list(row)[1:]:
            if pd.isna(col):
                continue
            if col not in G:
                nodetype = detect_type(col, row)
                G.add_node(col, label=col, color=node_colors.get(nodetype, "#ccc"))
            G.add_edge(prev, col)
            prev = col
    net = Network(height="550px", width="100%", notebook=False)
    net.from_nx(G)
    net.set_options('''{
      "nodes": {"shape": "dot", "size": 20, "font": {"size": 16, "color": "#343434"}, "borderWidth": 2},
      "edges": {"width": 2, "smooth": true, "arrows": {"to": {"enabled": false}, "from": {"enabled": false}}},
      "physics": {"forceAtlas2Based": {"gravitationalConstant": -50, "centralGravity": 0.01, "springLength": 100, "springConstant": 0.08},
                  "solver": "forceAtlas2Based", "timestep": 0.35, "stabilization": {"iterations": 150}}
    }''')
    net.save_graph("graph.html")
    with open("graph.html", "r", encoding="utf-8") as f:
        html = f.read()
    st.components.v1.html(html, height=600)
    st.download_button("下载查询网络图 HTML", data=html, file_name="network_graph.html", mime="text/html")