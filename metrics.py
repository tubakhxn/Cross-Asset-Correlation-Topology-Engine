"""
metrics.py
Computes network metrics for systemic risk analysis.
"""
import networkx as nx
from typing import Dict, Any

def compute_metrics(G: nx.Graph) -> Dict[str, Any]:
    """
    Compute key network metrics for a given graph:
    - Degree centrality
    - Eigenvector centrality
    - Clustering coefficient
    - Network density
    - Modularity (to be filled after clustering)
    Returns a dictionary of metrics.
    """
    metrics = {}
    metrics['degree_centrality'] = nx.degree_centrality(G)
    metrics['eigenvector_centrality'] = nx.eigenvector_centrality(G, max_iter=1000)
    metrics['clustering_coefficient'] = nx.clustering(G)
    metrics['network_density'] = nx.density(G)
    metrics['modularity'] = None  # To be computed after clustering
    return metrics
