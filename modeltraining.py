import joblib
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


def model_training():
    
    # Load preprocessed data
    data = np.load('preprocessed_data.npz')
    X = data['X']
    y = data['y']

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.09, random_state=42)

    # Initialize and train HistGradientBoostingRegressor. Tweak parameters for performance
    model = HistGradientBoostingRegressor(
        learning_rate=0.07,
        max_iter=90,
        max_depth=9,
        min_samples_leaf=23,
        l2_regularization=0.4,
        random_state=42)

    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate performance
    print("MSE:", mean_squared_error(y_test, y_pred))
    print("R²:", r2_score(y_test, y_pred))

    # Print shapes
    print("Train shape:", X_train.shape)
    print("Full data shape:", X.shape)

    # Save model
    with open("linear_model.joblib", "wb") as f:
        joblib.dump(model, f)
