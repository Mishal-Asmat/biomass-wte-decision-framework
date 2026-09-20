"""Feature scaling for distance-based clustering."""

from sklearn.preprocessing import StandardScaler


def scale_features(df):
    """
    Clustering features are standardized to zero mean/unit variance to avoid
    distance calculation bias when variables with different units (e.g. MJ/kg 
    vs. %) are used for measurement. 

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
