import joblib
import pandas as pd
from LinearRegression import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

dataset = pd.read_csv('../generatedataset/width_angle_dataset.csv')

x = dataset.drop('angle', axis=1)
y = dataset['angle']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

regressor = LinearRegression()
regressor.fit(x_train.values, y_train.values)

predictions = regressor.predict(x_test.values)
score = r2_score(y_test.values, predictions)
print(predictions)
print("On test data model has a coefficient R^2 of ", score)

filename = '../../../model/angle_regressor_model.sav'
joblib.dump(regressor, filename)
