"""Select the number of clusters (k) via inertia (elbow) and silhouette score."""

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def evaluate_k_range(X, k_range=range(2, 8)):
    """
    Fit KMeans across a range of ``k`` values and record inertia
    (within-cluster compactness) and silhouette score (between-cluster
    separation quality) for each, to support elbow-point selection.

    Parameters
    ----------
    X : array-like
        Scaled feature matrix (unsupervised: no labels required).
    k_range : iterable of int
        Candidate cluster counts to evaluate.

    Returns
    -------
    list[dict]
        One record per k: ``{"k", "inertia", "silhouette"}``.
    """
    results = []

    for k in k_range:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(X)

        results.append({
            "k": k,
            "inertia": model.inertia_,
            "silhouette": silhouette_score(X, labels)
        })

    return results
