"""Identify disagreement cases between the three decision frameworks."""

import pandas as pd


def label_disagreement_cases(df: pd.DataFrame) -> pd.DataFrame:
    """
    Label rows where the cluster-only, rule-only, and hybrid decision
    frameworks disagree with one another.

    Adds
    ----
    Cluster_vs_Rule_Disagree : bool
    Rule_vs_Hybrid_Disagree : bool
    Cluster_vs_Hybrid_Disagree : bool
    """
    df = df.copy()

    df["Cluster_vs_Rule_Disagree"] = (
        df["Final_Tech_ClusterOnly"] != df["Final_Tech_RuleOnly"]
    )
    df["Rule_vs_Hybrid_Disagree"] = (
        df["Final_Tech_RuleOnly"] != df["Final_Conversion_Technology"]
    )
    df["Cluster_vs_Hybrid_Disagree"] = (
        df["Final_Tech_ClusterOnly"] != df["Final_Conversion_Technology"]
    )

    return df
