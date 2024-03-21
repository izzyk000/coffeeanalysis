import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report
from joblib import dump
import os
from data_processing import load_data, preprocess_data

# Load and preprocess the data
coffee_products_df, customers_data_df, sales_data_df = load_data()
average_monthly_sales_with_share = preprocess_data(coffee_products_df, sales_data_df)

# Merge processed data back with coffee_products_df to ensure all necessary data is present
final_df = pd.merge(average_monthly_sales_with_share, coffee_products_df, on='ProductID', how='left')

# Create Target Encoded features
origin_means = final_df.groupby('Origin')['CompositeMetric'].mean().to_dict()
roastlevel_means = final_df.groupby('RoastLevel')['CompositeMetric'].mean().to_dict()

final_df['Origin_TargetEncoded'] = final_df['Origin'].map(origin_means)
final_df['RoastLevel_TargetEncoded'] = final_df['RoastLevel'].map(roastlevel_means)

# Define thresholds for categorization based on quantiles of CompositeMetric
low_threshold, high_threshold = final_df['CompositeMetric'].quantile([0.33, 0.66]).tolist()

# Categorize products based on CompositeMetric
def categorize_performance(metric):
    if metric <= low_threshold:
        return 'Low'
    elif metric <= high_threshold:
        return 'Medium'
    else:
        return 'High'

final_df['PerformanceCategory'] = final_df['CompositeMetric'].apply(categorize_performance)

# Prepare features and target for model training
features = final_df[['Origin_TargetEncoded', 'RoastLevel_TargetEncoded', 'Price']]
target = final_df['PerformanceCategory']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(features, target, random_state=42)

# Model training
model = make_pipeline(StandardScaler(), RandomForestClassifier(random_state=42))
param_grid = {
    'randomforestclassifier__n_estimators': [10, 50, 100, 200],
    'randomforestclassifier__max_depth': [None, 10, 20, 30],
}
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

# Save the trained model and feature importance
models_dir = 'models'
os.makedirs(models_dir, exist_ok=True)
dump(best_model, os.path.join(models_dir, 'your_model.joblib'))

feature_importance = best_model.named_steps['randomforestclassifier'].feature_importances_
features_list = ['Origin_TargetEncoded', 'RoastLevel_TargetEncoded', 'Price']
feature_importance_data = dict(zip(features_list, feature_importance))
dump(feature_importance_data, os.path.join(models_dir, 'feature_importance.joblib'))

# Evaluation and reporting
print("Best parameters:", grid_search.best_params_)
print("Best cross-validation score: {:.2f}".format(grid_search.best_score_))
y_pred_best = best_model.predict(X_test)
print(classification_report(y_test, y_pred_best))

# Save encoding dictionaries for future predictions
dump(origin_means, os.path.join(models_dir, 'origin_means.joblib'))
dump(roastlevel_means, os.path.join(models_dir, 'roastlevel_means.joblib'))
