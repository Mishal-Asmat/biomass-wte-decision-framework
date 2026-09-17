"""Ash-chemistry-based operational risk indicators (slagging/fouling)."""

import pandas as pd


def add_ash_risk_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add ash-chemistry-based operational risk indicators.

    Adds
    ----
    Alkali_Index : Na2O + K2O3
        Slagging risk from alkali metals (low-melting eutectics).
    Silica_Ratio : SiO2 / (CaO + MgO)
        Fouling behavior; high values indicate sticky-silicate formation.
    Base_Acid_Ratio : (CaO + MgO + Fe2O3) / (SiO2 + Al2O3)
        Ash-melting tendency (basic vs. acidic oxide balance).
    """
    df = df.copy()

    df["Alkali_Index"] = df["Na2O"] + df["K2O3"]
    df["Silica_Ratio"] = df["SiO2"] / (df["CaO"] + df["MgO"])
    df["Base_Acid_Ratio"] = (
        (df["CaO"] + df["MgO"] + df["Fe2O3"]) /
        (df["SiO2"] + df["Al2O3"])
    )

    return df
