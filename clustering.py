"""
clustering.py
Applies community detection and regime shift analysis.
"""
import networkx as nx
import numpy as np
from typing import Dict, Any, List
from networkx.algorithms.community import louvain_communities
from sklearn.cluster import SpectralClustering

def louvain_clustering(G: nx.Graph) -> List[List[str]]:
    """
    Detect communities using the Louvain method for modularity optimization.
    Returns a list of communities (each is a list of asset nodes).
    """
    return louvain_communities(G, seed=42)

def spectral_clustering(G: nx.Graph, n_clusters: int = 2) -> List[int]:
    """
    Detect communities using spectral clustering on the adjacency matrix.
    Returns a list of cluster labels for each node.
    """
    adj_matrix = nx.to_numpy_array(G)
    sc = SpectralClustering(n_clusters=n_clusters, affinity='precomputed', assign_labels='kmeans', random_state=42)
    labels = sc.fit_predict(adj_matrix)
    return labels

def detect_regime_shifts(metric_series: List[Dict[str, Any]], cluster_assignments: List[Any]) -> List[int]:
    """
    Detect regime shifts by tracking changes in network density and cluster assignments.
    Returns indices (time windows) where regime shifts are detected.
    """
    shifts = []
    prev_density = None
    prev_clusters = None
    for i, metrics in enumerate(metric_series):
        density = metrics['network_density']
        clusters = cluster_assignments[i]
        if prev_density is not None and abs(density - prev_density) > 0.1:
            shifts.append(i)
        if prev_clusters is not None and clusters != prev_clusters:
            shifts.append(i)
        prev_density = density
        prev_clusters = clusters
    return sorted(set(shifts))
