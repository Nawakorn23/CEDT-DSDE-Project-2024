import pandas as pd
import glob

# Load all files
file_paths = glob.glob("D:\\CEDT-2_01\\Data_project\\CEDT-DSDE-Project-2024\\data_per\\*_per.csv")

# Read each CSV file into a dictionary with year as key
dataframes = {}
for year, file_path in zip(range(2018, 2025), file_paths):
    dataframes[year] = pd.read_csv(file_path)

# Merge all the dataframes into one using 'Country', 'Subject Area', and 'Percentage' columns
merged_df = pd.DataFrame()

for year, df in dataframes.items():
    # Rename 'Percentage' to the respective year for clarity
    df = df.rename(columns={'Percentage': f"Year{year}"})
    
    if merged_df.empty:
        # Start with the first dataframe
        merged_df = df[['Country', 'Subject Area', f"Year{year}"]]
    else:
        # Merge subsequent dataframes based on 'Country' and 'Subject Area'
        merged_df = pd.merge(merged_df, df[['Country', 'Subject Area', f"Year{year}"]], on=['Country', 'Subject Area'], how='outer')


merged_df.to_csv("sum_per_data.csv")