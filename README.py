df['col1'] = df['col1'].apply(lambda x: x * 2080 if x < 1000 else x)
df['col2'] = df['col2'].apply(lambda x: x * 2080 if x < 1000 else x)
