"""
Categorization of variables and validation of dataset.

Divides the 79 columns of raw dataset into meaningful groups (identifiers, text, categorical, proximate/ultimate analysis,
HHV, ash-mineral composition) and exports the output file (``variable_categorization.json``) with no missing columns

"""

import json
import pandas as pd

identifier_vars = [
    "Sample_ID", "SSC_NAME16", "STE_NAME16",
    "Longitude", "Latitude"
]
text_vars = [
    "Short_Description", "Full_Description", "Notes",
    "Location_Notes", "Analysis_Note_1", "Source"
]
categorical_vars = [
    "Biomass_Type", "Class", "Subclass", "State"
]
proximate_analysis = [
    "Moist_ar", "Moist_ad",
    "Ash_ar", "Ash_ad", "Ash_db",
    "VM_ar", "VM_ad", "VM_db", "VM_daf",
    "FC_ar", "FC_ad", "FC_db", "FC_daf"
]
ultimate_analysis = [
    "C_ar", "C_ad", "C_db", "C_daf",
    "H_ar", "H_ad", "H_db", "H_daf",
    "N_ar", "N_ad", "N_db", "N_daf",
    "S_ar", "S_ad", "S_db", "S_daf",
    "O_ar", "O_ad", "O_db", "O_daf",
    "Cl_mg/kg_ar", "Cl_mg/kg_ad", "Cl_mg/kg_db", "Cl_mg/kg_daf"
]
HHV_vars = [
    "CV_MJ/kg_ar", "CV_MJ/kg_ad", "CV_MJ/kg_db", "CV_MJ/kg_daf",
    "CV_kcal/kg_ar", "CV_kcal/kg_ad", "CV_kcal/kg_db", "CV_kcal/kg_daf"
]
ash_mineral_vars = [
    "Na2O", "MgO", "Al2O3", "SiO2",
    "P2O5", "K2O3", "CaO", "TiO2",
    "Mn3O4", "Fe2O3", "Other"
]


def validate_and_categorize(df: pd.DataFrame, output_path: str) -> dict:
    """
    Categorization of dataset variables into groups and export
    a metadata report.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataset to validate.
    output_path : str
        Destination path for the JSON metadata report.

    Returns
    -------
    dict
        Metadata containing variable groupings, any missing columns
        per group, and overall dataset dimensions.
    """
    variable_map = {
        "identifiers": identifier_vars,
        "text": text_vars,
        "categorical": categorical_vars,
        "proximate_analysis": proximate_analysis,
        "ultimate_analysis": ultimate_analysis,
        "hhv_energy_content": HHV_vars,
        "mineral_ash_composition": ash_mineral_vars
    }

    missing_cols = {
        key: [c for c in cols if c not in df.columns]
        for key, cols in variable_map.items()
    }

    metadata = {
        "variable_groups": variable_map,
        "missing_columns": missing_cols,
        "n_samples": df.shape[0],
        "n_features": df.shape[1]
    }

    with open(output_path, "w") as f:
        json.dump(metadata, f, indent=4)

    return metadata
