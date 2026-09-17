"""
Phase 4A - Process/technology suitability rules.

Assigns graded (primary / secondary / constraint-level) thermochemical
process recommendations from engineered physicochemical features using
literature-aligned thresholds, independent of any ML predictions.
"""

import pandas as pd

from src.config.process_thresholds import thresholds


def assign_processes(row: pd.Series) -> pd.Series:
    """
    Assign Primary_Process, Secondary_Process, and Constraint_Level
    for a single sample based on graded fuel characteristics.
    """
    possible_processes = []

    # Pyrolysis: sufficiently high volatile matter, ash not excessive
    if (
        row["VM_db"] >= thresholds["pyrolysis"]["VM_min"] and
        row["Ash_db"] <= thresholds["pyrolysis"]["Ash_max"]
    ):
        possible_processes.append("Pyrolysis")

    # Gasification: VM in the moderate-high operating window, ash within limits
    if (
        thresholds["gasification"]["VM_min"] <= row["VM_db"] <= thresholds["gasification"]["VM_max"] and
        row["Ash_db"] <= thresholds["gasification"]["Ash_max"]
    ):
        possible_processes.append("Gasification")

    # Combustion: adequate fixed carbon, ash chemistry safe, moisture within limits
    if (
        row["FC_db"] >= thresholds["combustion"]["FC_min"] and
        row["Alkali_Index"] <= thresholds["combustion"]["Alkali_max"] and
        row["Moist_ar"] <= thresholds["combustion"]["Moisture_max"]
    ):
        possible_processes.append("Combustion")

    # Pre-treatment flag: hard constraint indicator, independent of process fit
    requires_pretreatment = (
        row["Ash_db"] >= thresholds["pretreatment"]["Ash_max"] or
        row["Moist_ar"] >= thresholds["pretreatment"]["Moisture_max"]
    )

    if not possible_processes:
        primary = "Pre-treatment Required"
        secondary = None
    else:
        primary = possible_processes[0]
        secondary = possible_processes[1] if len(possible_processes) > 1 else None

    constraint_level = (
        "High" if requires_pretreatment else
        "Moderate" if len(possible_processes) == 1 else
        "Low"
    )

    return pd.Series({
        "Primary_Process": primary,
        "Secondary_Process": secondary,
        "Constraint_Level": constraint_level
    })


def apply_process_rules(df: pd.DataFrame) -> pd.DataFrame:
    """Apply process suitability logic to every row of the engineered dataframe."""
    process_df = df.apply(assign_processes, axis=1)
    return pd.concat([df, process_df], axis=1)
