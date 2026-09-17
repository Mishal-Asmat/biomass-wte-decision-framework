"""Select the feature subset used for unsupervised fuel-typology clustering."""

import pandas as pd

# Clustering features are restricted to intrinsic energy behavior and
# first-order constraints that directly limit usable energy. Ash oxides
# are deliberately excluded here: they describe *reactor-side* problems
# (slagging, fouling) and not the fundamental fuel-type identity.
cluster_features = [
    "Sample_ID",             # metadata / reference key (not used as a feature)
    "CV_MJ/kg_db",            # energy density
    "VM_db",                  # ignition / devolatilization behavior
    "FC_db",                  # char formation / burnout behavior
    "Ash_db",                 # inert mass, first-order constraint on usable energy
    "Volatile_Fixed_Ratio",   # reactivity behavior
    "Moisture_Penalty"        # system-level efficiency loss
]


def build_clustering_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build the dataset used as input to unsupervised clustering.

    Restricts the engineered feature set to ``cluster_features`` and
    drops rows only where a clustering variable is missing (so upstream
    columns unrelated to clustering never cause unnecessary row loss).
    """
    cluster_df = df[cluster_features].dropna().copy()
    return cluster_df
