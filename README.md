## Creator/Dev: tubakhxn
<img width="2414" height="1587" alt="cross" src="https://github.com/user-attachments/assets/84884af5-b086-42a2-893f-d572b390976f" />

# Cross-Asset Correlation Topology Engine

## What is this project about?
This project models financial markets as a dynamic correlation network and detects systemic risk using graph theory and AI. It analyzes historical asset prices, builds rolling correlation networks, applies community detection, and visualizes network evolution to identify regime shifts and systemic risk.

## Main Features
- Data ingestion from CSV or Yahoo Finance (yfinance)
- Log return and rolling correlation computation
- Network construction (assets as nodes, correlations as weighted edges)
- Network metrics: degree/eigenvector centrality, clustering coefficient, density, modularity
- AI clustering: Louvain and Spectral clustering
- Regime shift detection
- Interactive 3D network graph (Plotly + NetworkX)
- Animated network evolution, heatmaps, and metric time series

## Project Files
- data.py: Data ingestion and preprocessing
- network_builder.py: Build correlation networks
- metrics.py: Compute network metrics
- clustering.py: Community detection and regime shift analysis
- visualization.py: All visualizations
- main.py: Entry point and pipeline orchestration

## How to Fork and Run
1. Fork this repository to your own GitHub account.
2. Clone your fork locally:
   ```
   git clone https://github.com/<your-username>/Cross-Asset-Correlation-Topology-Engine.git
   ```
3. Install Python 3.8+ and create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   Or manually:
   ```
   pip install numpy pandas yfinance networkx scikit-learn plotly
   ```
5. Run the project:
   ```
   python main.py --csv sample_prices.csv --window 60 --threshold 0.3 --clustering louvain
   ```
   Or use your own data or yfinance options.

---
For questions or contributions, contact tubakhxn.

