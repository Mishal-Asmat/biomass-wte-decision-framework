"""
Unit tests for ``src.data.validate_data``.

It covers correction of variable grouping, detection of missing-column, and
correction in reporting dataset-shape (exported metadata).
"""

import json

import pandas as pd
import pytest

from src.data.validate_data import validate_and_categorize


@pytest.fixture
def complete_df():
    """A minimal dataframe containing every column validate_data expects."""
    columns = [
        "Sample_ID", "SSC_NAME16", "STE_NAME16", "Longitude", "Latitude",
        "Short_Description", "Full_Description", "Notes",
        "Location_Notes", "Analysis_Note_1", "Source",
        "Biomass_Type", "Class", "Subclass", "State",
        "Moist_ar", "Moist_ad", "Ash_ar", "Ash_ad", "Ash_db",
        "VM_ar", "VM_ad", "VM_db", "VM_daf",
        "FC_ar", "FC_ad", "FC_db", "FC_daf",
        "C_ar", "C_ad", "C_db", "C_daf",
        "H_ar", "H_ad", "H_db", "H_daf",
        "N_ar", "N_ad", "N_db", "N_daf",
        "S_ar", "S_ad", "S_db", "S_daf",
        "O_ar", "O_ad", "O_db", "O_daf",
        "Cl_mg/kg_ar", "Cl_mg/kg_ad", "Cl_mg/kg_db", "Cl_mg/kg_daf",
        "CV_MJ/kg_ar", "CV_MJ/kg_ad", "CV_MJ/kg_db", "CV_MJ/kg_daf",
        "CV_kcal/kg_ar", "CV_kcal/kg_ad", "CV_kcal/kg_db", "CV_kcal/kg_daf",
        "Na2O", "MgO", "Al2O3", "SiO2", "P2O5", "K2O3", "CaO",
        "TiO2", "Mn3O4", "Fe2O3", "Other",
    ]
    data = {c: [1, 2] for c in columns}
    return pd.DataFrame(data)


def test_no_missing_columns_when_schema_complete(complete_df, tmp_path):
    output_path = tmp_path / "variable_categorization.json"

    metadata = validate_and_categorize(complete_df, str(output_path))

    for group, missing in metadata["missing_columns"].items():
        assert missing == [], f"Unexpected missing columns in group '{group}': {missing}"


def test_detects_missing_columns(complete_df, tmp_path):
    df = complete_df.drop(columns=["Ash_db", "State"])
    output_path = tmp_path / "variable_categorization.json"

    metadata = validate_and_categorize(df, str(output_path))

    assert "Ash_db" in metadata["missing_columns"]["proximate_analysis"]
    assert "State" in metadata["missing_columns"]["categorical"]


def test_reports_correct_shape(complete_df, tmp_path):
    output_path = tmp_path / "variable_categorization.json"

    metadata = validate_and_categorize(complete_df, str(output_path))

    assert metadata["n_samples"] == complete_df.shape[0]
    assert metadata["n_features"] == complete_df.shape[1]


def test_writes_valid_json_file(complete_df, tmp_path):
    output_path = tmp_path / "variable_categorization.json"

    validate_and_categorize(complete_df, str(output_path))

    assert output_path.exists()
    with open(output_path) as f:
        written = json.load(f)
    assert "variable_groups" in written
    assert "missing_columns" in written


def test_variable_groups_are_disjoint_where_expected(complete_df, tmp_path):
    output_path = tmp_path / "variable_categorization.json"

    metadata = validate_and_categorize(complete_df, str(output_path))
    groups = metadata["variable_groups"]

    # to avoid overlapping of identifiers and categorical variables
    assert set(groups["identifiers"]).isdisjoint(set(groups["categorical"]))
