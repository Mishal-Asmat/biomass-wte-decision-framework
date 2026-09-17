"""Raw dataset loading utilities"""

import pandas as pd


def load_raw_data(path: str) -> pd.DataFrame:
    """
    Load the raw biomass/waste fuel database.

    Parameters
    ----------
    path : str
        Path to the raw CSV file (e.g. ``data/raw/biomass_waste_dataset.csv``).

    Returns
    -------
    pd.DataFrame
        Unmodified raw dataset.
    """
    return pd.read_csv(path)
