"""
Cluster-only technology decision baseline.

Answers: if only the fuel-typology cluster is known (ignoring chemistry
and process-suitability rules entirely), which conversion technology
would be selected? Used as a comparison baseline against the rule-only
and hybrid decision frameworks (Phase 5).
"""

import pandas as pd


def assign_cluster_only_decision(df: pd.DataFrame) -> pd.DataFrame:
    """Assign a technology purely from cluster identity (Phase 4 typology)."""
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
