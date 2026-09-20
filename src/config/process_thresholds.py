"""
Thresholds (process bases andliterature aligned) are used to filter biomass fuels
for thermochemical conversion suitability

These are kept as single and editable dictionary to create threshold assumptions which are trapsrant,
version controlled and easy to defend without chnaging decision logic

"""

thresholds = {
    "pyrolysis": {
        "VM_min": 60,     # high volatile matter required for devolatilization dominant conversion
        "Ash_max": 25      # excessive ash limits the usable fraction of feedstock
    },
    "gasification": {
        "VM_min": 30,      # moderate volatile matter window
        "VM_max": 60,
        "Ash_max": 30
    },
    "combustion": {
        "FC_min": 15,          # sufficient fixed carbon for stable flame/char burnout
        "Alkali_max": 10,      # limits slagging/fouling risk (Na2O + K2O3)
        "Moisture_max": 20     # 'as-received' moisture ceiling for direct combustion
    },
    "pretreatment": {
        "Ash_max": 35,
        "Moisture_max": 30
    }
}
