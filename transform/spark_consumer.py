from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType,TimestampType

schema = StructType([
    StructField("transaction_id", StringType()),
    StructField("account_id", StringType()),
    StructField("amount", DoubleType()),
    StructField("currency", StringType()),
    StructField("merchant_category",StringType()),
    StructField("country", StringType()),
    StructField("timestamp", TimestampType()),
])

spark = (
    SparkSession.builder
    .appName("TransactionIngestion")
    # .config("spark.jars.packages",
    #         "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.7.3")
    .getOrCreate()
)

raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "transactions")
    .option("startingOffsets", "earliest")
    .load()
)

parsed = (
    raw.select(from_json(col("value").cast("string"), schema).alias("data"))
    .select("data.*")
    .filter(col("amount") > 0)  # basic data-quality gate — reject non-positive amounts
    .dropDuplicates(["transaction_id"])
)


def write_batch(batch_df, batch_id):
    (
        batch_df.write
        .format("jdbc")
        .option("url", "jdbc:postgresql://localhost:5432/transactions")
        .option("dbtable", "transactions_raw")
        .option("user", "txuser")
        .option("password", "txpass")
        .option("driver", "org.postgresql.Driver")
        .mode("append")
        .save()
    )


query = (
    parsed.writeStream
    .foreachBatch(write_batch)
    .outputMode("update")
    .start()
)

query.awaitTermination()