"""
Unit tests for ``src.features.feature_engineering`` and
``src.features.risk_indicators``.

Verification of engineered formulas of fuel-quality against the calculated
expected values, and checking of moisture penalty behavior (should decrease as moisture increases).
"""

import numpy as np
import pandas as pd
import pytest

from src.features.feature_engineering import (
    add_energy_reactivity_features,
    add_moisture_penalty,
)
from src.features.risk_indicators import add_ash_risk_indicators
from src.clustering.kmeans import canonicalize_cluster_labels


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "CV_MJ/kg_db": [20.0, 15.0],
        "FC_db": [10.0, 5.0],
        "VM_db": [80.0, 60.0],
        "Ash_db": [2.0, 4.0],
    })


@pytest.fixture
def sample_validated_df():
    return pd.DataFrame({"Moist_ar": [0.10, 0.30]})


def test_energy_density_index_formula(sample_df):
    result = add_energy_reactivity_features(sample_df)
    expected = sample_df["CV_MJ/kg_db"] * sample_df["FC_db"]
    pd.testing.assert_series_equal(
        result["Energy_Density_Index"], expected, check_names=False
    )


def test_volatile_fixed_ratio_formula(sample_df):
    result = add_energy_reactivity_features(sample_df)
    expected = sample_df["VM_db"] / sample_df["FC_db"]
    pd.testing.assert_series_equal(
        result["Volatile_Fixed_Ratio"], expected, check_names=False
    )


def test_combustibility_index_formula(sample_df):
    result = add_energy_reactivity_features(sample_df)
    expected = (sample_df["FC_db"] * sample_df["CV_MJ/kg_db"]) / sample_df["Ash_db"]
    pd.testing.assert_series_equal(
        result["Combustibility_Index"], expected, check_names=False
    )


def test_feature_engineering_does_not_mutate_input(sample_df):
    original = sample_df.copy()
    add_energy_reactivity_features(sample_df)
    pd.testing.assert_frame_equal(sample_df, original)


def test_moisture_penalty_decreases_as_moisture_increases(sample_df, sample_validated_df):
    engineered = add_energy_reactivity_features(sample_df)
    result = add_moisture_penalty(engineered, sample_validated_df)

    # Higher moisture (row 1, 0.30) must yield a lower penalty than
    # lower moisture (row 0, 0.10).
    assert result["Moisture_Penalty"].iloc[1] < result["Moisture_Penalty"].iloc[0]


def test_moisture_penalty_formula(sample_df, sample_validated_df):
    engineered = add_energy_reactivity_features(sample_df)
    result = add_moisture_penalty(engineered, sample_validated_df)

    expected = 1 / (1 + sample_validated_df["Moist_ar"])
    np.testing.assert_allclose(result["Moisture_Penalty"].values, expected.values)


def test_effective_hhv_formula(sample_df, sample_validated_df):
    engineered = add_energy_reactivity_features(sample_df)
    result = add_moisture_penalty(engineered, sample_validated_df)

    expected = sample_df["CV_MJ/kg_db"] * (1 - sample_validated_df["Moist_ar"])
    np.testing.assert_allclose(result["Effective_HHV"].values, expected.values)


@pytest.fixture
def ash_df():
    return pd.DataFrame({
        "Na2O": [1.0, 0.5],
        "K2O3": [2.0, 1.0],
        "SiO2": [10.0, 20.0],
        "CaO": [4.0, 2.0],
        "MgO": [1.0, 1.0],
        "Al2O3": [5.0, 5.0],
        "Fe2O3": [2.0, 1.0],
    })


def test_alkali_index_formula(ash_df):
    result = add_ash_risk_indicators(ash_df)
    expected = ash_df["Na2O"] + ash_df["K2O3"]
    pd.testing.assert_series_equal(result["Alkali_Index"], expected, check_names=False)


def test_silica_ratio_formula(ash_df):
    result = add_ash_risk_indicators(ash_df)
    expected = ash_df["SiO2"] / (ash_df["CaO"] + ash_df["MgO"])
    pd.testing.assert_series_equal(result["Silica_Ratio"], expected, check_names=False)


def test_base_acid_ratio_formula(ash_df):
    result = add_ash_risk_indicators(ash_df)
    expected = (
        (ash_df["CaO"] + ash_df["MgO"] + ash_df["Fe2O3"]) /
        (ash_df["SiO2"] + ash_df["Al2O3"])
    )
    pd.testing.assert_series_equal(result["Base_Acid_Ratio"], expected, check_names=False)


# --- Canonicalization of cluster label -----------------------------------------
# Becausse it is found that KMeans assigned clusters random numbers, but decision rules have
# fixed meaning of those numbers. So, this test guards the particular step of forcing the 
# numbering to always mean the same  

def test_canonicalize_cluster_labels_orders_by_ascending_mean():
    raw_labels = [0, 0, 1, 1, 2, 2]
    ash_db = pd.Series([30.0, 32.0, 15.0, 17.0, 2.0, 3.0])

    result = canonicalize_cluster_labels(raw_labels, ash_db)

    assert list(result[:2]) == [2, 2]
    assert list(result[2:4]) == [1, 1]
    assert list(result[4:6]) == [0, 0]


def test_canonicalize_cluster_labels_is_a_relabeling_not_a_reordering():
    raw_labels = [0, 1, 2, 0, 1, 2]
    ash_db = pd.Series([1.0, 10.0, 30.0, 1.5, 11.0, 29.0])

    result = canonicalize_cluster_labels(raw_labels, ash_db)

    # All 3 groups are same only the label identities may change.
    assert len(result) == len(raw_labels)
    assert len(set(result)) == 3
