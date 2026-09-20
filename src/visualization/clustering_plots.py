"""KMeans clustering analysis and visualization of results."""

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def plot_elbow(X, k_range, save_path):
    """Plot inertia vs. number of clusters (elbow method for k selection)."""
    inertia = []

    for k in k_range:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(X)
        inertia.append(model.inertia_)

    plt.figure(figsize=(7, 5))
    plt.plot(list(k_range), inertia, marker="o")
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Inertia")
    plt.title("Elbow Method for K Selection")
    plt.grid(True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_silhouette_scores(X, k_range, save_path):
    """Plot silhouette score vs. number of clusters."""
    scores = []

    for k in k_range:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(X)
        scores.append(silhouette_score(X, labels))

    plt.figure(figsize=(7, 5))
    plt.plot(list(k_range), scores, marker="o")
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Silhouette Score")
    plt.title("Silhouette Score vs Number of Clusters")
    plt.grid(True)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_pca_clusters(X, labels, save_path):
    """Project scaled features to 2D via PCA and color by cluster label."""
    pca = PCA(n_components=2)
    components = pca.fit_transform(X)

    pca_df = pd.DataFrame(components, columns=["PC1", "PC2"])
    pca_df["Cluster"] = labels

    plt.figure(figsize=(7, 6))
    scatter = plt.scatter(
        pca_df["PC1"], pca_df["PC2"], c=pca_df["Cluster"], alpha=0.7
    )
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("PCA Projection of Biomass Clusters")
    plt.colorbar(scatter, label="Cluster")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
