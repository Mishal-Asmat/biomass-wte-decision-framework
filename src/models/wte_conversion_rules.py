"""
Phase 4C - Cluster-informed hybrid WtE conversion decision framework.

Combines cluster identity (Phase 4), process suitability (Phase 4A),
and constraint level into a final conversion-technology recommendation. 
This decision layer is compared against the cluster-only and rule-only 
baselines in Phase 5.
"""

import pandas as pd


def assign_conversion_technology(df: pd.DataFrame) -> pd.DataFrame:
    """
    Final WtE decision layer combining cluster identity, primary
    process suitability, and physical constraints.

    Adds
    ----
    Final_Conversion_Technology : str
    """
    df = df.copy()

    def decision_logic(row):
        cluster = row["Cluster"]              # fuel family
        primary = row["Primary_Process"]      # best process chemically
        constraint = row["Constraint_Level"]  # feasibility level

        # Cluster 0: low-ash / woody / thermodynamically stable biomass
        if cluster == 0:
            if primary == "Gasification":
                return "Gasification"
            return "Combustion"

        # Cluster 1: highly reactive / high-volatiles / waste-like / energy-dense
        elif cluster == 1:
            if primary == "Pyrolysis":
                return "Pyrolysis"
            return "Combustion"

        # Cluster 2: high-ash / wet / biologically active / degraded feedstock
        elif cluster == 2:
            if constraint == "High":
                return "Gasification"
            return "Pyrolysis"

        return "Further Assessment Needed"

    df["Final_Conversion_Technology"] = df.apply(decision_logic, axis=1)
    return df
