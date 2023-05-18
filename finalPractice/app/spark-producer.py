from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg
from app.schemas import Schemas

# Define Spark session
spark = SparkSession.builder.appName("Top station Streaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0") \
    .getOrCreate()

# Define schema
schemas = Schemas()
statusSchema = schemas.statusSchema

# Read parquet files
statusDf = spark.readStream.option("header", True) \
    .option("timestampFormat", "M/d/y H:m") \
    .schema(statusSchema) \
    .parquet("../parquetResources/status.parquet")

# Get most popular stations
popularDf = statusDf.groupBy("station_id") \
    .agg(count("*").alias("count"),
         avg("bikes_available").alias("avg_bikes"),
         avg("docks_available").alias("avg_docks")) \
    .withColumn("popularity",
                col("count") * col("avg_bikes") * col("avg_docks")) \
    .orderBy(col("popularity").desc())

#  Prepare the result DataFrame to send to Kafka
kafka_df = popularDf.selectExpr("to_json(struct(*)) AS value")

# Send the result to a Kafka topic
query = kafka_df.writeStream.format("kafka") \
    .outputMode("complete") \
    .option("kafka.bootstrap.servers", "localhost:29092") \
    .option("topic", "station_topic") \
    .option("checkpointLocation", "checkpoints") \
    .start()
query.awaitTermination()
