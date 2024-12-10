import pandas as pd

# Loading data from the uploaded file
df = pd.read_csv('D:\\CEDT-2_01\\Data_project\\CEDT-DSDE-Project-2024\\te_sql_summary_2024.csv')

# Calculating percentage for each country, year, and subject area
df['Total Documents'] = df.groupby(['Country', 'Year'])['Number of Documents'].transform('sum')
df['Percentage'] = (df['Number of Documents'] / df['Total Documents']) * 100

df.to_csv('D:\\CEDT-2_01\\Data_project\\CEDT-DSDE-Project-2024\\2024_per.csv', index=False)
