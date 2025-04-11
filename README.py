# Get unique, non-null job codes as a list
job_codes = dup['Job Code'].dropna().unique().tolist()

# Print them as a clean, comma-separated string
print(", ".join(job_codes))
