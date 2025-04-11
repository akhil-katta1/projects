# Get unique job codes and convert all to strings
job_codes = dup['Job Code'].dropna().unique().tolist()
job_codes = [str(code) for code in job_codes]

# Print as comma-separated string
print(", ".join(job_codes))
