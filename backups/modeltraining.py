import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load data
data = np.load('preprocessed_data.npz')
X = data['X']
y = data['y']

# split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.06, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("MSE:", mean_squared_error(y_test, y_pred))
print("R²:", r2_score(y_test, y_pred))

print(X_train.shape)  # Should show (n_samples, 12)
print(X.shape)

with open("linear_model.pkl", "wb") as f:
    pickle.dump(model, f)