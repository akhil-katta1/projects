def convert_object_to_string(df):
    """
    Converts all columns with 'object' data type to string type in a pandas DataFrame.
    
    Args:
    df (pandas.DataFrame): The input DataFrame.
    
    Returns:
    pandas.DataFrame: DataFrame with 'object' columns converted to string.
    """
    # Convert columns with 'object' data type to string
    for column in df.select_dtypes(include=['object']).columns:
        df[column] = df[column].astype(str)
    
    return df
