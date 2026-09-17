"""
Phase 4B - Cluster explainability via feature statistics + Random Forest
feature importance.

Clusters are fuel typologies, not technologies. This module answers:
which biomass properties make Cluster 0 different from Cluster 1 and
Cluster 2? It (1) quantifies per-cluster feature differences, (2) ranks
which features best explain the separation via a Random Forest
classifier trained to predict cluster membership from explainable
indicators, and (3) renders per-feature boxplots by cluster.
.
"""

import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier

# Explainable features used for cluster separation analysis.
# Combustibility_Index is intentionally excluded: it is derived from
# features already present here (FC_db, CV_MJ/kg_db, Ash_db) and would
# be redundant for feature-importance ranking.
EXPLAIN_FEATURES = [
    "Moisture_Penalty",       # operational limitation
    "Alkali_Index",           # slagging / fouling risk
    "Silica_Ratio",           # ash chemistry
    "Base_Acid_Ratio",        # ash behavior
    "Volatile_Fixed_Ratio",   # thermal reactivity
    "Effective_HHV",          # usable energy
    "Energy_Density_Index"    # logistics + performance
]


def compute_cluster_feature_statistics(df: pd.DataFrame, tables_dir: str,
                                        features: list = None) -> tuple:
    """
    Compute per-cluster mean and standard deviation of explainable
    features and persist them as CSV tables.

    Returns
    -------
    (cluster_means, cluster_std) : tuple[pd.DataFrame, pd.DataFrame]
    """
    features = features or EXPLAIN_FEATURES
    os.makedirs(tables_dir, exist_ok=True)

    cluster_means = df.groupby("Cluster")[features].mean()
    cluster_means.to_csv(os.path.join(tables_dir, "cluster_feature_means.csv"))

    cluster_std = df.groupby("Cluster")[features].std()
    cluster_std.to_csv(os.path.join(tables_dir, "cluster_feature_std.csv"))

    return cluster_means, cluster_std


def plot_cluster_feature_boxplots(df: pd.DataFrame, figures_dir: str,
                                   features: list = None) -> None:
    """save one boxplot per explainable feature, grouped by cluster."""
    features = features or EXPLAIN_FEATURES
    os.makedirs(figures_dir, exist_ok=True)

    for feature in features:
        plt.figure(figsize=(14, 6))
        sns.boxplot(data=df, x="Cluster", y=feature)
        plt.title(f"{feature.replace('_', ' ')} Distribution by Cluster")
        plt.tight_layout()
        plt.savefig(
            os.path.join(figures_dir, f"feature_{feature.lower()}_boxplots.png"),
            dpi=300
        )
        plt.close()


def compute_feature_importance(df: pd.DataFrame, tables_dir: str, figures_dir: str,
                                features: list = None) -> pd.DataFrame:
    """
    Rank explainable features by their importance in predicting cluster
    membership using a Random Forest classifier, and save a table + bar plot.

    Returns
    -------
    pd.DataFrame
        Feature importance table, sorted descending.
    """
    features = features or EXPLAIN_FEATURES
    os.makedirs(tables_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    X = df[features]
    y = df["Cluster"]

    model = RandomForestClassifier(n_estimators=500, random_state=42)
    model.fit(X, y)

    feature_importance = pd.DataFrame({
        "Feature": features,
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    feature_importance.to_csv(
        os.path.join(tables_dir, "cluster_feature_importance_rf.csv"), index=False
    )

    plt.figure(figsize=(8, 5))
    sns.barplot(data=feature_importance, x="Importance", y="Feature")
    plt.title("Feature Importance Explaining Clusters")
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "rf_feature_importance.png"), dpi=300)
    plt.close()

    return feature_importance


def run_cluster_explainability(df: pd.DataFrame, tables_dir: str, figures_dir: str,
                                features: list = None) -> dict:
    """
    Run the full Phase 4B explainability workflow: per-cluster
    statistics, boxplots, and Random Forest feature importance.

    Parameters
    ----------
    df : pd.DataFrame
        Engineered feature dataframe with a ``Cluster`` column
        (rows without a cluster label are dropped).
    tables_dir : str
        Output directory for CSV summary tables.
    figures_dir : str
        Output directory for PNG figures.

    Returns
    -------
    dict
        ``{"cluster_means", "cluster_std", "feature_importance"}``
    """
    features = features or EXPLAIN_FEATURES

    df = df.dropna(subset=["Cluster"]).copy()
    df["Cluster"] = df["Cluster"].astype(int)

    cluster_means, cluster_std = compute_cluster_feature_statistics(df, tables_dir, features)
    plot_cluster_feature_boxplots(df, figures_dir, features)
    feature_importance = compute_feature_importance(df, tables_dir, figures_dir, features)

    return {
        "cluster_means": cluster_means,
        "cluster_std": cluster_std,
        "feature_importance": feature_importance
    }
