"""
Cluster-only technology decision baseline.

Which conversion technology would be selected if only fuel-typology cluster is known?
Also used as comparison baseline against rule only and hybrid decision frameworks.

"""

import pandas as pd


def assign_cluster_only_decision(df: pd.DataFrame) -> pd.DataFrame:
    """Assign a technology depending entirely on cluster identity"""
    df = df.copy()

    def decision_logic(cluster):
        if cluster == 0:
            # Woody / low-ash / thermodynamically stable
            return "Combustion"
        elif cluster == 1:
            # High-volatiles / reactive / waste-like
            return "Pyrolysis"
        elif cluster == 2:
            # High-ash / wet / degraded feedstock
            return "Further Assessment Needed"
        return "Further Assessment Needed"

    df["Final_Tech_ClusterOnly"] = df["Cluster"].apply(decision_logic)
    return df
