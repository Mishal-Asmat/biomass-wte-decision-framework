"""
Harmoniation of analytical basis.

The raw dataset contains proximate/ultimate/HHV variables with 4 different bases (as-received "ar", air-dried "ad", dry "db", and
dry-ash-free "daf"). To avoid issues of multicollinearity and moisture distortion, a single canonical dry-basis ("db") is selected
which best represents the intrinsic properties of fuel. 

"""

import json
import pandas as pd

# Canonical basis: intrinsic, basis-independent fuel/biomass properties
canonical_columns = [
    "Sample_ID", "Biomass_Type", "Class", "Subclass",   # Metadata
    "Ash_db", "VM_db", "FC_db",                         # Proximate (dry basis)
    "C_db", "H_db", "N_db", "S_db", "O_db",             # Ultimate (dry basis)
    "CV_MJ/kg_db",                                      # Energy
    "Na2O", "MgO", "Al2O3", "SiO2",                     # Ash chemistry
    "P2O5", "K2O3", "CaO", "TiO2",
    "Mn3O4", "Fe2O3", "Other",
    "State", "Longitude", "Latitude"                    # Metadata
]


def harmonize_to_db_basis(df: pd.DataFrame, output_csv: str, meta_path: str) -> pd.DataFrame:
    """
    Reduce the validated dataset to dry-basis canonical variables and
    keep both the harmonized dataset and the modeling-decision
    metadata.

    Parameters
    ----------
    df : pd.DataFrame
        Validated dataset (output of ``validate_and_categorize``).
    output_csv : str
        Destination path for the harmonized dry-basis CSV.
    meta_path : str
        Destination path for the JSON basis-selection metadata.

    Returns
    -------
    pd.DataFrame
        Dataset restricted to ``canonical_columns``.
    """
    missing = [c for c in canonical_columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    harmonized_df = df[canonical_columns].copy()

    metadata = {
        "selected_basis": "dry_basis (db)",
        "rationale": "Minimizes moisture distortion and multicollinearity",
        "retained_features": canonical_columns,
        "dropped_bases": ["ar", "ad", "daf"]
    }

    harmonized_df.to_csv(output_csv, index=False)

    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=4)

    return harmonized_df
