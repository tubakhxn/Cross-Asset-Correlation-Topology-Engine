"""
main.py
Entry point for Cross-Asset Correlation Topology Engine.
"""
import argparse
import pandas as pd
import networkx as nx
from data import load_csv, download_yfinance, compute_log_returns, compute_rolling_correlation
from network_builder import build_dynamic_network
from metrics import compute_metrics
from clustering import louvain_clustering, spectral_clustering, detect_regime_shifts
from visualization import plot_3d_network, plot_correlation_heatmap, plot_metric_timeseries


def main():
    parser = argparse.ArgumentParser(description="Cross-Asset Correlation Topology Engine")
    parser.add_argument('--csv', type=str, help='Path to CSV file with historical prices')
    parser.add_argument('--tickers', nargs='+', help='List of asset tickers for yfinance download')
    parser.add_argument('--start', type=str, help='Start date for yfinance (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, help='End date for yfinance (YYYY-MM-DD)')
    parser.add_argument('--window', type=int, default=60, help='Rolling window size')
    parser.add_argument('--threshold', type=float, default=0.3, help='Correlation threshold for edges')
    parser.add_argument('--clustering', choices=['louvain', 'spectral'], default='louvain', help='Community detection method')
    args = parser.parse_args()

    # Data ingestion
    if args.csv:
        prices = load_csv(args.csv)
    elif args.tickers and args.start and args.end:
        prices = download_yfinance(args.tickers, args.start, args.end)
    else:
        print("Error: Provide either --csv or --tickers, --start, --end.")
        return

    # Preprocessing
    log_returns = compute_log_returns(prices)
    rolling_corrs = compute_rolling_correlation(log_returns, window=args.window)

    # Network construction
    graphs = build_dynamic_network(rolling_corrs, threshold=args.threshold)

    # Analysis over time
    metric_series = []
    clusters_list = []
    for G in graphs:
        metrics = compute_metrics(G)
        if args.clustering == 'louvain':
            communities = louvain_clustering(G)
            clusters = {node: idx for idx, comm in enumerate(communities) for node in comm}
        else:
            labels = spectral_clustering(G, n_clusters=2)
            clusters = {node: label for node, label in zip(G.nodes(), labels)}
        metrics['modularity'] = nx.algorithms.community.modularity(G, [list(comm) for comm in communities] if args.clustering == 'louvain' else [list(G.nodes())])
        metric_series.append(metrics)
        clusters_list.append(clusters)

    # Regime shift detection
    regime_shifts = detect_regime_shifts(metric_series, clusters_list)
    print(f"Regime shifts detected at windows: {regime_shifts}")

    # Visualization (first window as example)
    plot_3d_network(graphs[0], clusters_list[0], metric_series[0]['degree_centrality'])
    plot_correlation_heatmap(rolling_corrs[0])
    plot_metric_timeseries(metric_series, 'network_density')

if __name__ == "__main__":
    main()
