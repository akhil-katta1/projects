import pandas as pd

# Load your dataset
df = pd.read_csv('your_dataset.csv')  # Replace with your dataset file

# Set the index to the row with the maximum value of a specific column (for example, 'column_name')
# If you want to use the index as the max row in general, you can use the max of the DataFrame itself.
max_row_index = df.idxmax()  # Finds the index of the maximum value across the DataFrame
df.set_index(df.index[max_row_index[0]], inplace=True)  # Set the max value row as the index

# Find duplicate rows
duplicates = df[df.duplicated(keep=False)]  # This will include all duplicates

# Print the duplicate rows
print(duplicates)
