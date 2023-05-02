from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType, IntegerType

class Schemas:
    def __init__(self):
        self.statusSchema = StructType([
            StructField("station_id", IntegerType(), True),
            StructField("bikes_available", IntegerType(), True),
            StructField("docks_available", IntegerType(), True),
            StructField("time", TimestampType(), True)
        ])
        self.stationSchema = StructType([
            StructField("id", IntegerType(), True),
            StructField("name", StringType(), True),
            StructField("lat", FloatType(), True),
            StructField("long", FloatType(), True),
            StructField("dock_count", IntegerType(), True),
            StructField("city", StringType(), True),
            StructField("installation_date", TimestampType(), True)
        ])
        self.popularitySchema = StructType([
            StructField("station_id", IntegerType(), True),
            StructField("count", IntegerType(), True),
            StructField("avg_bikes", StringType(), True),
            StructField("avg_docks", FloatType(), True),
            StructField("popularity", FloatType(), True)
        ])
