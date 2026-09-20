"""Fit the KMeans fuel-typology clustering model."""

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
    Remapping of random KMeans integer labels into a fixed, physically
    meaningful ordering.

    the cluster indices (0, 1, 2, ...) assigned via KMeans is based on internal centre point which
    could not provide stable outcomes across runs, streamlit verisons or minor changes in input 
    feature matrix (e.g inclusion of identifier column). Downstream rule-based modules 
    (``cluster_only_rules.py``, ``wte_conversion_rules.py``) use particular technology decisions for 
    each cluster, with fixed ordering (Cluster 0 = lowest ash / most stable, Cluster 2 = highest ash / 
    most constrained). It ensures the explicit ordering by re-labelling clusters according to increasing
    mean of ``sort_series`` (Ash_db).

    Parameters
    ----------
    labels : array-like
        Raw KMeans integer labels.
    sort_series : pd.Series
        The variable to rank cluster means by (indexed identically to
        ``labels``); ``Ash_db`` throughout this project.

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
