"""Feature subset selection for unsupervised fuel-typology clustering."""

import pandas as pd

# Clustering features are limited to intrinsic energy behavior and
# first-order constraints of fuels that directly restricts usable energy.
# Ash oxides are excluded here as they donot describe fuel-type identity.
cluster_features = [
    "Sample_ID",              # metadata / reference key (not used as a feature)
    "CV_MJ/kg_db",            # energy density
    "VM_db",                  # ignition behavior
    "FC_db",                  # burnout behavior
    "Ash_db",                 # inert mass, first-order constraint on usable energy
    "Volatile_Fixed_Ratio",   # reactivity behavior
    "Moisture_Penalty"        # system-level efficiency loss
]


def build_clustering_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the dataset to use as input for unsupervised clustering.

    Restricts the engineered feature set to ``cluster_features`` and
    drops rows only where a clustering variable is missing.
    """
    cluster_df = df[cluster_features].dropna().copy()
    return cluster_df
