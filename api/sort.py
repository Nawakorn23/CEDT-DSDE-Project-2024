import pandas as pd

# Load the dataset
data = pd.read_csv("all_with_y5.csv")  # Replace with your actual file name

# Sort the data by 'Country', 'Year', and 'Subject Area'
data_sorted = data.sort_values(by=['Country', 'Subject Area', 'Year'])

# Save the sorted data to a new CSV file
data_sorted.to_csv("sorted_data_y5.csv", index=False)

# Display the sorted data
print(data_sorted)
