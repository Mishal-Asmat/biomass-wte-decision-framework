"""
Engineered fuel-quality indicators.

Two categories of engineered features are produced:

1. Intrinsic, dry-basis fuel-chemistry indicators (energy density,
   reactivity, combustibility) that depend only on lab-measured data
   (proximate/ultimate/HHV).
2. A system-level moisture penalty that is reintroduced 'as-received
   moisture' without compromising the chemistry of dry-basis.
"""

import pandas as pd


def add_energy_reactivity_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add intrinsic fuel-quality indicators calculated on a dry basis.

    Adds
    ----
    Energy_Density_Index : CV_MJ/kg_db * FC_db
        Overall energy intensity.
    Volatile_Fixed_Ratio : VM_db / FC_db
        Reactivity / devolatilization behavior.
    Combustibility_Index : (FC_db * CV_MJ/kg_db) / Ash_db
        Combustion suitability, penalized by inert ash content.
    """
    df = df.copy()

    df["Energy_Density_Index"] = df["CV_MJ/kg_db"] * df["FC_db"]
    df["Volatile_Fixed_Ratio"] = df["VM_db"] / df["FC_db"]
    df["Combustibility_Index"] = (
        df["FC_db"] * df["CV_MJ/kg_db"]
    ) / df["Ash_db"]

    return df


def add_moisture_penalty(df_engineered: pd.DataFrame, df_validated: pd.DataFrame) -> pd.DataFrame:
    """
    Add a system-level moisture penalty and effective (moisture-adjusted)
    HHV which is sourced from validated (pre-harmonization) dataset to avoid
    contamination to dry basis chemistry anywhere else in pipeline.

    Adds
    ----
    Moist_ar : as-received moisture, carried over from validated data.
    Moisture_Penalty : 1 / (1 + Moist_ar)
        Decreases monotonically as moisture increases.
    Effective_HHV : CV_MJ/kg_db * (1 - Moist_ar)
        Practical, moisture-derated heating value.
    """
    df = df_engineered.copy()

    df["Moist_ar"] = df_validated["Moist_ar"].values
    df["Moisture_Penalty"] = 1 / (1 + df["Moist_ar"])
    df["Effective_HHV"] = df["CV_MJ/kg_db"] * (1 - df["Moist_ar"])

    return df
