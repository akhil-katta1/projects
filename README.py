# Remove dollar signs from the 'col1' column
df['col1'] = df['col1'].replace({'\$': ''}, regex=True)
