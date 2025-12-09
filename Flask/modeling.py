import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import GridSearchCV, learning_curve
import seaborn as sns
import pickle


def load_data(path):
    print(f"Loading data from {path}")
    data = pd.read_csv(path)
    print(data.head())
    return data

def train_model(df):
    target = df["value"]
    df.drop(columns=["value"], inplace=True)
    # split data for training and testing
    X_train, X_test, y_train, y_test = train_test_split(df, target, test_size=0.2, random_state=42)
    rf = RandomForestRegressor(random_state=42, n_estimators=100, max_depth=10, min_samples_split=5, max_features="sqrt", bootstrap=True)
    rf.fit(X_train, y_train)

    #Make predictions
    y_pred = rf.predict(X_test)

    #Evaluate the classifier
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mean_absolute_error, mean_squared_error, r2_score

    print(f"Regression Mean Absolute Error: {mae:.2f}")
    print(f"Regression Mean Squared Error: {mse:.2f}")
    print(f"Regression r2 Score: {r2:.2f}")

    parameters = {
    "max_depth": [None, 3, 5, 8, 10, 15, 20],
    "min_samples_split": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20],
    "max_features": ['sqrt', 'log2', None]
}

    grid_search = GridSearchCV(estimator=rf, param_grid=parameters, cv=5)

    grid_search.fit(X_train, y_train)

    #Evaluate the model
    y_pred = rf.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return rf, X_test, y_test, mae, mse, r2

def test_model(model, X_test, y_test):
    # Get the model score
    y_pred = model.predict(X_test)
    mae = model.mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Squared Error: {mse}")
    print(f"R2 Score: {r2}")

    return mae, mse, r2

def predict(model, X_test):
    return model.predict(X_test)

def save_model(model, path):

    # Save Model Using Pickle
    with open(path, "wb") as model_file:
        pickle.dump(model, model_file)

    return model

def load_model(path):
    with open(path, "rb") as model_file:
        model = pickle.load(model_file)
    return model

def main():
    df = load_data("scaledData/.csv")
    print(f"Data after loading: {df.head()}")
   # df = preprocess_data(df)
    model, X_test, y_test, mae, mse, r2 = train_model(df)
    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Squared Error: {mse}")
    print(f"R2 Score: {r2}")
    test_model(model, X_test, y_test)
    save_model(model, "models/model.pkl")
    return model

if __name__ == "__main__":
    main()