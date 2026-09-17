"""Fit the final KMeans fuel-typology clustering model."""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def run_kmeans(X, n_clusters=3):
    """
    Fit a KMeans model with a fixed number of clusters, selected
    upstream via inertia (elbow) and silhouette-score analysis
    (see ``src.clustering.evaluation``).

    Parameters
    ----------
    X : array-like
        Scaled feature matrix.
    n_clusters : int, default 3
        Number of fuel-typology clusters to fit.

    Returns
    -------
    model : sklearn.cluster.KMeans
        Fitted clustering model.
    labels : np.ndarray
        Cluster label assigned to each sample.
    """
    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,   # reproducibility
        n_init=10          # multiple centroid seedings for stability
    )
    labels = model.fit_predict(X)
    return model, labels


def canonicalize_cluster_labels(labels, sort_series: pd.Series) -> np.ndarray:
    """
    Remap arbitrary KMeans integer labels to a fixed, physically
    meaningful ordering.

    KMeans assigns cluster indices (0, 1, 2, ...) based on internal
    centroid-discovery order, which is **not** guaranteed to be stable
    across runs, scikit-learn versions, or even minor changes to the
    input feature matrix (e.g., whether a spurious identifier column is
    accidentally included). Downstream rule-based modules in this
    project (``cluster_only_rules.py``, ``wte_conversion_rules.py``)
    hardcode technology decisions per literal cluster index, assuming a
    fixed semantic ordering (Cluster 0 = lowest ash / most stable,
    Cluster 2 = highest ash / most constrained). This function enforces
    that ordering explicitly and deterministically, by relabeling
    clusters according to ascending mean of ``sort_series`` (Ash_db).

    Parameters
    ----------
    labels : array-like
        Raw KMeans integer labels.
    sort_series : pd.Series
        The variable to rank cluster means by (indexed identically to
        ``labels``); ``Ash_db`` is used throughout this project.

    Returns
    -------
    np.ndarray
        Relabeled cluster assignments, 0 = lowest mean, increasing.
    """
    labels = np.asarray(labels)
    tmp = pd.DataFrame({"raw_label": labels, "sort_var": sort_series.values})
    ranked = (
        tmp.groupby("raw_label")["sort_var"]
        .mean()
        .sort_values()
        .reset_index()
    )
    remap = {row.raw_label: new_idx for new_idx, row in ranked.iterrows()}
    return np.array([remap[l] for l in labels])
