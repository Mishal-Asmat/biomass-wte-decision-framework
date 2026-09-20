"""
Rule-only technology decision baseline.

Which specific technology is suitable based on Primary_Process and Constraint_Level 
outputs (phase 4A) only avoiding cluster infromtion? Avoid Secondary_Process and give
single best technology. It is done to avoid collapse of hybrid framework. 

"""

import pandas as pd


def assign_rule_only_conversion(df: pd.DataFrame) -> pd.DataFrame:
    """Assign a technology depedning only on process-suitability rules."""
    df = df.copy()

    def decision_logic(row):
        primary = row["Primary_Process"]

        if primary == "Pre-treatment Required":
            return "Further Assessment Needed"

        return primary

    df["Final_Tech_RuleOnly"] = df.apply(decision_logic, axis=1)
    return df
