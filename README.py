from pyspark.sql.types import StructType, StructField, StringType, FloatType

schema = StructType([
    StructField("Job Code", StringType(), True),
    StructField("Job Title", StringType(), True),
    StructField("Pay Scale Group", StringType(), True),
    StructField("Pay Scale Type", StringType(), True),
    StructField("Bargaining Unit", StringType(), True),
    StructField("Min Salary", FloatType(), True),
    StructField("Max Salary", FloatType(), True),
    StructField("Mean Salary", FloatType(), True)
])
