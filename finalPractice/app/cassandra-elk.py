from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master('local') \
    .appName("Popularity of stations") \
    .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.2.0,"
                                   "org.elasticsearch:elasticsearch-spark-30_2.12:8.0.0") \
    .config("es.net.ssl.cert.allow.self.signed", "true") \
    .getOrCreate()

df = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", "popularity") \
    .option("table", "popularstations") \
    .load()

es_write_conf = {
    "es.nodes": "localhost",
    "es.port": "9200",
    "es.nodes.wan.only": "true",
}

df.write.format("es") \
    .mode("overwrite") \
    .options(**es_write_conf) \
    .save("popularity")
