"""
visualization.py
Handles all visualizations using Plotly and NetworkX.
"""
import plotly.graph_objs as go
import networkx as nx
import numpy as np
import pandas as pd
from typing import List, Dict, Any

def plot_3d_network(G: nx.Graph, clusters: Dict[str, int], centrality: Dict[str, float], title: str = "3D Correlation Network"):
    """
    Plot a 3D interactive network graph using Plotly and NetworkX.
    - Node size: centrality
    - Edge thickness: correlation strength
    - Node color: cluster assignment
    - Dark theme aesthetic
    """
    pos = nx.spring_layout(G, dim=3, seed=42)
    edge_x, edge_y, edge_z, edge_width = [], [], [], []
    for u, v, d in G.edges(data=True):
        x0, y0, z0 = pos[u]
        x1, y1, z1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        edge_z += [z0, z1, None]
        edge_width.append(abs(d['weight']) * 5)
    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        line=dict(width=2, color='#888'),
        hoverinfo='none', mode='lines')
    node_x, node_y, node_z, node_size, node_color = [], [], [], [], []
    for node in G.nodes():
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        node_size.append(centrality[node] * 30 + 10)
        node_color.append(clusters.get(node, 0))
    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        marker=dict(
            size=node_size,
            color=node_color,
            colorscale='Viridis',
            line=dict(width=2, color='DarkSlateGrey'),
            opacity=0.85
        ),
        text=list(G.nodes()),
        hoverinfo='text')
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=title,
                        showlegend=False,
                        margin=dict(l=0, r=0, b=0, t=40),
                        paper_bgcolor='rgb(20,20,30)',
                        plot_bgcolor='rgb(20,20,30)',
                        scene=dict(
                            xaxis=dict(showbackground=False),
                            yaxis=dict(showbackground=False),
                            zaxis=dict(showbackground=False)
                        )
                    ))
    fig.show()

def animate_network_evolution(graphs: List[nx.Graph], clusters_list: List[Dict[str, int]], centrality_list: List[Dict[str, float]]):
    """
    Animate network evolution over time using Plotly animation frames.
    (To be implemented for full time-series animation.)
    """
    pass

def plot_correlation_heatmap(corr_matrix: pd.DataFrame, title: str = "Rolling Correlation Heatmap"):
    """
    Plot a heatmap of rolling correlations using Plotly.
    - Dark theme aesthetic
    """
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='Viridis'))
    fig.update_layout(title=title, paper_bgcolor='rgb(20,20,30)', plot_bgcolor='rgb(20,20,30)')
    fig.show()

def plot_metric_timeseries(metric_series: List[Dict[str, Any]], metric_name: str, title: str = "Network Metric Time Series"):
    """
    Plot time series of a network metric using Plotly.
    - Shows evolution of metrics (e.g., density, centrality) over time.
    - Dark theme aesthetic
    """
    values = [metrics[metric_name] if isinstance(metrics[metric_name], float) else np.mean(list(metrics[metric_name].values())) for metrics in metric_series]
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=values, mode='lines', line=dict(color='cyan')))
    fig.update_layout(title=title, paper_bgcolor='rgb(20,20,30)', plot_bgcolor='rgb(20,20,30)')
    fig.show()
