# Set pandas to display all rows and columns
pd.set_option('display.max_rows', None)  # No limit to the number of rows
pd.set_option('display.max_columns', None)  # No limit to the number of columns
pd.set_option('display.width', None)  # To avoid line wrapping
pd.set_option('display.max_colwidth', None)  # Show full column content

# Find duplicate rows (including the first occurrence)
duplicates = df[df.duplicated(keep=False)]  # This will include all duplicates

# Print the entire table of duplicates
print(duplicates)
