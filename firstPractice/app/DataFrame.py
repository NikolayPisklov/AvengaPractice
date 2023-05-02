import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType, IntegerType

spark = SparkSession.builder.appName('Avenga').getOrCreate()
spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")

statusSchema = StructType([
    StructField("station_id", IntegerType(), True),
    StructField("bikes_available", IntegerType(), True),
    StructField("docks_available", IntegerType(), True),
    StructField("time", TimestampType(), True)
])
stationSchema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("lat", FloatType(), True),
    StructField("long", FloatType(), True),
    StructField("dock_count", IntegerType(), True),
    StructField("city", StringType(), True),
    StructField("installation_date", TimestampType(), True)
])

statusDf = spark.read.format("csv") \
    .option("header", True) \
    .option("timestampFormat", "M/d/y H:m") \
    .schema(statusSchema) \
    .load("resources/status.csv")
stationDf = spark.read.format("csv") \
    .option("header", True) \
    .option("timestampFormat", "M/d/y H:m") \
    .schema(stationSchema) \
    .load("resources/station.csv")

# most popular stations
popularDf = statusDf.groupBy("station_id") \
     .agg(count("*").alias("count"),
          avg("bikes_available").alias("avg_bikes"),
          avg("docks_available").alias("avg_docks")) \
     .withColumn("popularity",
                 col("count") * col("avg_bikes") * col("avg_docks")) \
     .orderBy(col("popularity").desc())

# joining df to get name and city of stations
joinedDf = popularDf.join(stationDf, stationDf.id == popularDf.station_id) \
     .select(stationDf.id, stationDf.name, stationDf.city, popularDf.popularity)

joinedDf.show()


