"""
Central reference for column groupings used throughout the pipeline.

This module is documentation-as-code: it does not transform data, it
simply names which raw / engineered columns belong to which conceptual
group so that feature selection choices in the notebooks are explicit
and reusable rather than re-typed in every phase.
"""

# --- Raw measured variables (dry basis, "_db") ---------------------------
proximate_db = ["Ash_db", "VM_db", "FC_db"]          # Proximate analysis
moisture_ar = ["Moist_ar"]                           # As-received moisture (system-level only)
ultimate_db = ["C_db", "H_db", "N_db", "S_db", "O_db"]  # Ultimate analysis
hhv_db = ["CV_MJ/kg_db"]                             # Higher heating value

# Ash-forming oxides, split by process relevance
primary_ash_oxides = [                               # Process-critical (slagging/fouling/ash fusion)
    "Na2O", "K2O3", "CaO", "MgO",
    "SiO2", "Al2O3", "Fe2O3"
]
secondary_ash_oxides = [                             # Chemically relevant but not process-dominant
    "P2O5", "TiO2", "Mn3O4", "Other"
]

# --- Engineered variables --------------------------------------------------
energy_indices = [
    "Effective_HHV",
    "Energy_Density_Index"
]
ash_indices = [
    "Alkali_Index",
    "Base_Acid_Ratio",
    "Silica_Ratio",
]
process_modifiers = [
    "Moisture_Penalty",
    "Volatile_Fixed_Ratio"
]

# --- Model input groups -----------------------------------------------------
# Used for unsupervised clustering / downstream ML.
model_features = (
    proximate_db
    + hhv_db
    + energy_indices
    + ash_indices
    + process_modifiers
)
