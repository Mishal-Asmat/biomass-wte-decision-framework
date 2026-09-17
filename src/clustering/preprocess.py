"""Feature scaling for distance-based clustering."""

from sklearn.preprocessing import StandardScaler


def scale_features(df):
    """
    Standardize clustering features to zero mean / unit variance so
    that variables measured in different units (e.g. MJ/kg vs. %)
    contribute to distance calculations without bias.

    Returns
    -------
    X_scaled : np.ndarray
        Standardized feature matrix.
    scaler : sklearn.preprocessing.StandardScaler
        Fitted scaler (retained for potential inverse-transform / reuse).
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)
    return X_scaled, scaler
