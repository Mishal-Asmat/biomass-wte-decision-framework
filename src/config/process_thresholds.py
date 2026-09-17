"""
Engineering-informed, literature-aligned thresholds used to screen
biomass fuels for thermochemical conversion suitability.

These are intentionally kept as a single, editable dictionary so that
threshold assumptions are transparent, version-controlled, and easy to
cite / defend (e.g., in a methods section or to a reviewer) without
touching the decision logic in ``src.models.suitability_rules``.
"""

thresholds = {
    "pyrolysis": {
        "VM_min": 60,     # high volatile matter required for devolatilization-dominant conversion
        "Ash_max": 25      # excessive ash limits usable feedstock fraction
    },
    "gasification": {
        "VM_min": 30,      # moderate volatile matter window
        "VM_max": 60,
        "Ash_max": 30
    },
    "combustion": {
        "FC_min": 15,          # sufficient fixed carbon for stable flame/char burnout
        "Alkali_max": 10,      # limits slagging/fouling risk (Na2O + K2O3)
        "Moisture_max": 20     # as-received moisture ceiling for direct combustion
    },
    "pretreatment": {
        "Ash_max": 35,
        "Moisture_max": 30
    }
}
