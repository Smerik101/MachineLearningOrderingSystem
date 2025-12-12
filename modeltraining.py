from joblib import dump
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def model_training(state):
    error_total = []
    
    # Load preprocessed data
    for filename in state.pp_data.iterdir():
        name = str(filename.name)[0:-4]
        data = np.load(filename)
        X = data['X']
        y = data['y']

        #Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False) 
        
        # Initialize and train HistGradientBoostingRegressor. Tweak parameters for performance
        model = Pipeline([
            ("scaler", StandardScaler()),
            ("ridge", Ridge(alpha=1.0))
        ])

        model.fit(X_train, y_train)

        # Make predictions
        y_valid = model.predict(X_train)
        y_pred = model.predict(X_test)

        # Evaluate performance
        print(name)
        print("Validation")
        print("MSE:", mean_squared_error(y_test, y_pred))
        print("R²:", r2_score(y_test, y_pred))
        print("Training")
        print("MSE:", mean_squared_error(y_train, y_valid))
        print("R²:", r2_score(y_train, y_valid))
        print(f"Diff:{((mean_squared_error(y_train, y_valid))/mean_squared_error(y_test, y_pred))*100}%")
        print("\n")

        error_total.append(mean_squared_error(y_train, y_valid))

        # Save model
        dump(model, f"{state.model_path}/{name}.joblib")
    
    print(error_total)
    print(float(sum(error_total)) / len(error_total))  
  
