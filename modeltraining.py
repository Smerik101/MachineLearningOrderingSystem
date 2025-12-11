from joblib import dump
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from pathlib import Path
import json


def model_training(state):

    with open ("model_params.json", "r") as f:
        custom_params = json.load(f)
    
    # Load preprocessed data
    for filename in state.pp_data.iterdir():
        name = str(filename.name)[0:-4]
        data = np.load(filename)
        X = data['X']
        y = data['y']

        if name in custom_params.keys():
            params = custom_params[name]

        #Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False)
        
        
        # Initialize and train HistGradientBoostingRegressor. Tweak parameters for performance
        model = HistGradientBoostingRegressor(
            learning_rate=0.05,
            max_iter=100,
            max_leaf_nodes = 31,
            min_samples_leaf=30,
            l2_regularization=0.5,
            early_stopping=True,
            validation_fraction=0.2,
            random_state=42)

        if name in custom_params:
            model.set_params(**params)

        model.fit(X_train, y_train)

        # Make predictions
        y_valid = model.predict(X_train)
        y_pred = model.predict(X_test)

        """
        print(name)
        # Evaluate performance
        print("Validation")
        print("MSE:", mean_squared_error(y_test, y_pred))
        print("R²:", r2_score(y_test, y_pred))

        print("Training")
        print("MSE:", mean_squared_error(y_train, y_valid))
        print("R²:", r2_score(y_train, y_valid))

        print(f"Diff:{((mean_squared_error(y_train, y_valid))/mean_squared_error(y_test, y_pred))*100}%")

        print("\n")
        """

        # Save model
        dump(model, f"{state.model_path}/{name}.joblib")
  
