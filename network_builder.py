"""
network_builder.py
Constructs a dynamic correlation network from rolling correlation matrices.
"""
import networkx as nx
import numpy as np
import pandas as pd
from typing import List, Dict

def correlation_to_graph(corr_matrix: pd.DataFrame, threshold: float = 0.3) -> nx.Graph:
    """
    Convert a correlation matrix to a weighted undirected graph.
    Nodes represent assets, edges represent correlation strength.
    Edges below the threshold are removed.
    """
    G = nx.Graph()
    assets = corr_matrix.columns
    for i, asset_i in enumerate(assets):
        G.add_node(asset_i)
        for j, asset_j in enumerate(assets):
            if i < j:
                weight = corr_matrix.iloc[i, j]
                if abs(weight) >= threshold:
                    G.add_edge(asset_i, asset_j, weight=weight)
    return G

def build_dynamic_network(rolling_corrs: List[pd.DataFrame], threshold: float = 0.3) -> List[nx.Graph]:
    """
    Build a list of NetworkX graphs from rolling correlation matrices.
    Each graph models the market at a time window.
    """
    graphs = [correlation_to_graph(corr, threshold) for corr in rolling_corrs]
    return graphs
