import pandas as pd
import re

def process_salary_ranges(df):
    # Exit early if column doesn't exist
    if df is None or 'Salary Range' not in df.columns:
        return df

    # Step 1: Clean and standardize the 'Salary Range' text
    def extract_salary_range(value):
        if pd.isna(value):
            return value
        value_str = str(value)
        numbers = re.findall(r"([\d,]+\.\d+)", value_str)
        if len(numbers) >= 2:
            return f"{numbers[0]} - {numbers[1]}"
        elif len(numbers) == 1:
            return f"{numbers[0]}"
        else:
            return None

    df['Salary Range'] = df['Salary Range'].apply(extract_salary_range)

    # Step 2: Split the cleaned range into min and max
    split_range = df['Salary Range'].str.replace(',', '').str.split('-', expand=True)

    df['Min Salary'] = pd.to_numeric(split_range[0], errors='coerce')
    df['Max Salary'] = pd.to_numeric(split_range[1], errors='coerce')

    # Step 3: Calculate mean salary
    df['Mean Salary'] = df[['Min Salary', 'Max Salary']].mean(axis=1)

    return df
