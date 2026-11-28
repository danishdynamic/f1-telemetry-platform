
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


spark = (
    SparkSession.builder
    .appName("F1-Silver-To-Gold")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Read the cleaned Silver lap dataset.
laps = spark.read.parquet("/data/silver/laps")

# Add optional sector columns if they are missing.
for column in [
    "duration_sector_1",
    "duration_sector_2",
    "duration_sector_3",
]:
    if column not in laps.columns:
        laps = laps.withColumn(
            column,
            F.lit(None).cast("double"),
        )

# Calculate race-session performance for each driver.
gold = (
    laps
    .groupBy(
        "year",
        "session_key",
        "driver_number",
    )
    .agg(
        F.min("lap_duration").alias("best_lap_seconds"),
        F.avg("lap_duration").alias("average_lap_seconds"),
        F.countDistinct("lap_number").alias("valid_lap_count"),
        F.min("duration_sector_1").alias("best_sector_1"),
        F.min("duration_sector_2").alias("best_sector_2"),
        F.min("duration_sector_3").alias("best_sector_3"),
    )
)

# Rank drivers by their best lap within each session.
from pyspark.sql.window import Window

rank_window = Window.partitionBy(
    "year",
    "session_key",
).orderBy("best_lap_seconds")

gold = gold.withColumn(
    "best_lap_rank",
    F.rank().over(rank_window),
)

# Save analytics as partitioned Parquet.
gold.write \
    .mode("overwrite") \
    .partitionBy("year", "session_key") \
    .parquet("/data/gold/driver_performance")

print("Silver to Gold processing completed.")
gold.orderBy(
    "year",
    "session_key",
    "best_lap_rank",
).show(20, truncate=False)

spark.stop()
