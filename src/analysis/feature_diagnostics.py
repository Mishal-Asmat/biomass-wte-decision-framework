"""
Diagnose why decision frameworks disagree by comparing the behavior of
decision-active features across groups (clusters, rule outcomes, or
final technology).

Interpretability analysis is restricted to decision-active indicators
directly involved in process suitability and conversion logic.
Secondary chemical constituents and metadata are excluded to avoid
redundancy and preserve causal interpretability: ultimate-analysis
elements (C, H, O, N, S) are already embedded in HHV / Energy Density /
Combustibility Index, and individual ash oxides (Na2O, CaO, MgO, ...)
are already embedded in Silica Ratio / Base-Acid Ratio / Alkali Index.
"""

import pandas as pd

key_features = [
    "Ash_db",                # direct constraint in pyrolysis and gasification
    "VM_db",                 # core driver for pyrolysis and gasification
    "FC_db",                 # combustion suitability
    "Moist_ar",               # pre-treatment + constraint level
    "Alkali_Index",           # slagging/fouling -> combustion rejection
    "Silica_Ratio",           # ash melting behavior
    "Base_Acid_Ratio",        # ash chemistry severity
    "Energy_Density_Index",   # overall fuel quality
    "Combustibility_Index"    # thermal stability and reactivity
]


def summarize_features_by_group(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """
    Compare mean / median / standard deviation of decision-active
    features across a grouping column (e.g. Cluster, Final_Tech_RuleOnly,
    or Final_Conversion_Technology).

    - mean: average/typical fuel condition for the group.
    - median: whether behavior is widespread or outlier-driven.
    - std: heterogeneity within the group (confidence in the assignment).
    """
    return (
        df.groupby(group_col)[key_features]
        .agg(["mean", "median", "std"])
        .round(3)
    )
