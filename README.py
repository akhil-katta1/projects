from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

# Define the schema
schema = StructType([
    StructField("Job Code", StringType(), True),
    StructField("Job Title", StringType(), True),
    StructField("Pay Scale Group", FloatType(), True),
    StructField("Pay Scale Type", StringType(), True),
    StructField("Bargaining Unit", StringType(), True),
    StructField("Salary Range", StringType(), True),
    StructField("Min Salary", FloatType(), True),
    StructField("Max Salary", FloatType(), True),
    StructField("Mean Salary", FloatType(), True)
])

# Now you can create a Spark DataFrame with the schema
df = spark.createDataFrame(df_pandas, schema=schema)
