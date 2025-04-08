import re

def reverse_month_format(value):
    # Match pattern like '12-Oct' or '9-Oct' and convert to 'Oct 12'
    if isinstance(value, str) and re.match(r'^\d{1,2}-[A-Za-z]{3}$', value):
        day, month = value.split('-')
        return f"{month} {int(day)}"
    return value

df['PAY GRADE'] = df['PAY GRADE'].apply(reverse_month_format)

# Step 3: Confirm changes
print(df['PAY GRADE'].head(10))
