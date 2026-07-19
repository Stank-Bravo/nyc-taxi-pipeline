import os
os.environ["PYSPARK_PYTHON"] = "python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, dayofweek, when, round
from pyspark.sql.types import DoubleType

# ── 1. Start Spark Session ──────────────────────────────────────────
spark = SparkSession.builder \
    .master("local[2]") \
    .appName("NYC Taxi Pipeline") \
    .config("spark.sql.shuffle.partitions", "4") \
    .config("spark.shuffle.push.enabled", "false") \
    .config("spark.executor.extraJavaOptions", "-Dio.netty.tryReflectionSetAccessible=true") \
    .config("spark.driver.extraJavaOptions", "-Dio.netty.tryReflectionSetAccessible=true") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
print("✅ Spark session started")

# ── 2. Ingest ───────────────────────────────────────────────────────
df = spark.read.parquet("data/yellow_tripdata_2024-01.parquet")
print(f"✅ Loaded {df.count():,} rows")
df.printSchema()

# ── 3. Clean ────────────────────────────────────────────────────────
df_clean = df \
    .dropna(subset=["tpep_pickup_datetime", "tpep_dropoff_datetime",
                    "trip_distance", "fare_amount", "passenger_count"]) \
    .filter(col("trip_distance") > 0) \
    .filter(col("fare_amount") > 0) \
    .filter(col("passenger_count") > 0) \
    .filter(col("passenger_count") <= 6)

print(f"✅ After cleaning: {df_clean.count():,} rows")

# ── 4. Transform ─────────────────────────────────────────────────────
df_transformed = df_clean \
    .withColumn("pickup_hour", hour("tpep_pickup_datetime")) \
    .withColumn("pickup_day", dayofweek("tpep_pickup_datetime")) \
    .withColumn("trip_duration_mins",
        round((col("tpep_dropoff_datetime").cast("long") -
               col("tpep_pickup_datetime").cast("long")) / 60, 2)) \
    .withColumn("day_type",
        when(col("pickup_day").isin([1, 7]), "Weekend").otherwise("Weekday")) \
    .filter(col("trip_duration_mins") > 0) \
    .filter(col("trip_duration_mins") < 120)

# ── 5. Aggregate ─────────────────────────────────────────────────────
hourly_demand = df_transformed \
    .groupBy("pickup_hour") \
    .count() \
    .withColumnRenamed("count", "trip_count") \
    .orderBy("pickup_hour")

avg_fare_by_day = df_transformed \
    .groupBy("day_type") \
    .agg({"fare_amount": "avg", "trip_duration_mins": "avg"})

# ── 6. Save ───────────────────────────────────────────────────────────
df_transformed.write.mode("overwrite").parquet("data/cleaned")
hourly_demand.write.mode("overwrite").parquet("data/hourly_demand")
avg_fare_by_day.write.mode("overwrite").parquet("data/avg_fare_by_day")

print("✅ Pipeline complete. Files saved to data/")
spark.stop()