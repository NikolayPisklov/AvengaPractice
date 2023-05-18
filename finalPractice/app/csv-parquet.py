from pyspark.sql import SparkSession
from app.schemas import Schemas

# Define Spark session
spark = SparkSession.builder.master('local').appName("Csv to parquet convert").getOrCreate()
spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")
# Define CSV schema
schemas = Schemas()
statusSchema = schemas.statusSchema
stationSchema = schemas.stationSchema
# Read CSV file
statusDf = spark.read.format("csv") \
             .option("header", True) \
             .option("timestampFormat", "M/d/y H:m") \
             .schema(statusSchema) \
             .load("../resources/status.csv")
stationDf = spark.read.format("csv") \
             .option("header", True) \
             .option("timestampFormat", "M/d/y H:m") \
             .schema(stationSchema) \
             .load("../resources/station.csv")

# Save result as parquet file
statusDf.repartition(1).write.parquet("../parquetResources/status.parquet")
stationDf.repartition(1).write.parquet("../parquetResources/station.parquet")