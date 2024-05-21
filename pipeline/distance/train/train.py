import joblib
import numpy
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.model_selection import GridSearchCV

dataset = pd.read_csv('../generatedataset/distance_dataset.csv')

x = dataset.drop('move_by', axis=1)
y = dataset['move_by']

# chose classifier instead of regressor because it shouldn't forecast value, but classify as class
random_forest = RandomForestClassifier()
# regulate model with grid search method

grid_param = [
    {'n_estimators': [3, 10, 30], 'max_features': [2, 4, 6, 8]},
    {'bootstrap': [False], 'n_estimators': [3, 10], 'max_features': [2, 3, 4]}
]

grid_search = GridSearchCV(
    random_forest, grid_param, cv=10, scoring='neg_mean_squared_error', return_train_score=True
)

grid_search.fit(x.values, y)
print('best params')
print(grid_search.best_params_)
print('best estimators')
print(grid_search.best_estimator_)

cv_results = grid_search.cv_results_
for mean_test_score, params in zip(cv_results['mean_test_score'], cv_results['params']):
    print(numpy.sqrt(-mean_test_score), params)

predictions = grid_search.predict(x)
grid_mse = mean_squared_error(y, predictions)
grid_rmse = numpy.sqrt(grid_mse)
print('mean squared error:')
print(grid_rmse)

accuracy = accuracy_score(y, predictions)
print(f'Accuracy: {accuracy:.2f}')

filename = '../../../model/distance_random_forest_model.pickle'
joblib.dump(grid_search, filename)
