# Load your dataset
michigan_ingest_df = pd.read_csv('/mnt/data/file-CXxZhv6kZWmcz4Tp8JPmTP')  # Replace with the actual file path

# Find duplicate rows
michigan_dup = michigan_ingest_df[michigan_ingest_df.duplicated(keep=False)]  # This includes all duplicates

# Set the index to the row with the maximum value of a specific column (e.g., the first column or based on another logic)
max_row_index = michigan_dup.idxmax()  # Find the index of the maximum value across the DataFrame
michigan_dup.set_index(michigan_dup.index[max_row_index[0]], inplace=True)  # Set the max value row as the index

# Print the duplicate rows
print(michigan_dup)
