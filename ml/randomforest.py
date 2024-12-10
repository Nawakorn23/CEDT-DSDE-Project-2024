import pandas as pd
import glob
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import os

file_paths = glob.glob("D:\\CEDT-2_01\\Data_project\\CEDT-DSDE-Project-2024\\data_per\\*_per.csv")
data_frames = []


for file_path in file_paths:
    df = pd.read_csv(file_path)
    year = os.path.basename(file_path).split('_')[0]
    df['Year'] = int(year)
    data_frames.append(df)

combined_df = pd.concat(data_frames)

# Filter out countries with Total Documents less than 5 
filtered_df = combined_df[combined_df['Total Documents'] >= 5]

pivot_df = filtered_df.pivot_table(index=['Country', 'Year'], 
                                   columns='Subject Area', 
                                   values='Percentage', 
                                   aggfunc='sum')

# training data (2018-2023) and test data (2024)
train_df = pivot_df.loc[pivot_df.index.get_level_values('Year').isin(range(2018, 2024))]
test_df = pivot_df.loc[pivot_df.index.get_level_values('Year') == 2024]

X_train = train_df.reset_index().drop(columns=['Country', 'Year'])
y_train = train_df.reset_index()['Country']
X_test = test_df.reset_index().drop(columns=['Country', 'Year'])

# Fill NaN values with 0
X_train = X_train.fillna(0)
X_test = X_test.fillna(0)

train_labels = train_df.idxmax(axis=1).values

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, train_labels)

predictions_2025_rf = rf_model.predict(X_test)

test_results_2025_rf = test_df.reset_index()[['Country']]
test_results_2025_rf['Predicted Highest Subject Area (2025)'] = predictions_2025_rf

test_results_2025_rf.to_csv('result.csv', index=False)

true_labels_2024 = test_df.idxmax(axis=1).values
all_labels = list(train_labels) + list(true_labels_2024)
label_encoder = LabelEncoder()
label_encoder.fit(all_labels)
true_labels_2024_encoded = label_encoder.transform(true_labels_2024)

predictions_2024_encoded = label_encoder.transform(rf_model.predict(X_test))

# error
accuracy_2024 = accuracy_score(true_labels_2024_encoded, predictions_2024_encoded)
error_2024 = 1 - accuracy_2024

print(f"Error rate for 2024 predictions: {error_2024}")
