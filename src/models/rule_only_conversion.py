"""
Rule-only technology decision baseline.

Answers: is this specific technology chemically/physically suitable or
not, using only the Phase 4A Primary_Process / Constraint_Level output
and ignoring cluster (fuel-typology) information entirely? Only the
single best-suited condition is used (no secondary/moderate fallback),
otherwise this would collapse into the hybrid framework.
"""

import pandas as pd


def assign_rule_only_conversion(df: pd.DataFrame) -> pd.DataFrame:
    """Assign a technology purely from process-suitability rules (Phase 4A)."""
    df = df.copy()

    def decision_logic(row):
        primary = row["Primary_Process"]

        if primary == "Pre-treatment Required":
            return "Further Assessment Needed"

        return primary

    df["Final_Tech_RuleOnly"] = df.apply(decision_logic, axis=1)
    return df
