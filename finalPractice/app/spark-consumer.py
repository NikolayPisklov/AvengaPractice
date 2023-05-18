from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from app.schemas import Schemas

# Define Spark session
spark = SparkSession.builder.appName("Top stations from Kafka") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,"
                                   "com.datastax.spark:spark-cassandra-connector_2.12:3.2.0") \
    .config("spark.cassandra.connection.host", "localhost") \
    .getOrCreate()

# Define schemas
schemas = Schemas()
popularitySchema = schemas.popularitySchema
stationSchema = schemas.stationSchema

# Read input data from Kafka and parquet
kafkaDf = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:29092") \
    .option("subscribe", "station_topic") \
    .option("startingOffsets", "earliest") \
    .load()

stationDf = spark.read.parquet("../parquetResources/station.parquet")

cleanDf = kafkaDf.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", popularitySchema).alias("data")) \
    .select("data.*")

# Join data frames
joinedDf = cleanDf.join(stationDf, cleanDf.station_id == stationDf.id) \
    .select(cleanDf.station_id, stationDf.name, stationDf.city, cleanDf.popularity)

# Write to cassandra
query = joinedDf.writeStream \
    .format("org.apache.spark.sql.cassandra") \
    .option("checkpointLocation", "checkpoints") \
    .option("keyspace", "popularity") \
    .option("table", "popularstations") \
    .start()

query.awaitTermination()
