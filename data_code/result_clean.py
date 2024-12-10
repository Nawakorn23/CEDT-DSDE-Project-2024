import pandas as pd

# Load the predicted data from result.csv
data = pd.read_csv('D:\\CEDT-2_01\\Data_project\\CEDT-DSDE-Project-2024\\result_per.csv')

# Group by 'Country' and find the subject area with the highest percentage for each country
data_cleaned = data.loc[data.groupby('Country')['Predicted_Percentage'].idxmax()]

# Save the cleaned data to a new CSV file
data_cleaned.to_csv('D:\\CEDT-2_01\\Data_project\\CEDT-DSDE-Project-2024\\cleaned_result.csv', index=False)

print("Cleaned data with highest percentage subject area per country has been saved to cleaned_result.csv")
