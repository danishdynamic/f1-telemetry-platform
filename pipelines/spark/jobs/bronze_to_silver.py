
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


BRONZE_PATH = Path("/data/bronze")
SILVER_PATH = "/data/silver"


spark = (
    SparkSession.builder
    .appName("F1-Bronze-To-Silver")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


def read_json_files(pattern):
    # Find raw snapshots matching the requested dataset.
    files = list(BRONZE_PATH.glob(pattern))

    if not files:
        raise FileNotFoundError(
            f"No Bronze files found for pattern: {pattern}"
        )

    return (
        spark.read
        .option("multiLine", "true")
        .option("basePath", str(BRONZE_PATH))
        .json([str(file) for file in files])
    )


def keep_existing_columns(df, columns):
    # Avoid errors when an optional API field is absent.
    return df.select(
        *[column for column in columns if column in df.columns]
    )


# -------------------------
# Drivers
# -------------------------

drivers = read_json_files(
    "year=*/session_key=*/drivers_*.json"
)

drivers = drivers.withColumn(
    "driver_number",
    F.col("driver_number").cast("int"),
)

drivers = drivers.filter(
    F.col("driver_number").isNotNull()
)

drivers = drivers.dropDuplicates(
    ["year", "session_key", "driver_number"]
)

driver_columns = [
    "year",
    "session_key",
    "driver_number",
    "full_name",
    "name_acronym",
    "team_name",
    "team_colour",
    "country_code",
]

drivers = keep_existing_columns(
    drivers,
    driver_columns,
)

drivers.write \
    .mode("overwrite") \
    .partitionBy("year", "session_key") \
    .parquet(f"{SILVER_PATH}/drivers")


# -------------------------
# Laps
# -------------------------

laps = read_json_files(
    "year=*/session_key=*/laps_*.json"
)

laps = (
    laps
    .withColumn("driver_number", F.col("driver_number").cast("int"))
    .withColumn("lap_number", F.col("lap_number").cast("int"))
    .withColumn("lap_duration", F.col("lap_duration").cast("double"))
)

# Keep laps with valid positive durations.
laps = laps.filter(
    F.col("lap_duration").isNotNull()
    & (F.col("lap_duration") > 0)
)

# Exclude pit-out laps when the flag is available.
pit_flag = (
    "is_pit_out_lap"
    if "is_pit_out_lap" in laps.columns
    else "pit_out_lap"
    if "pit_out_lap" in laps.columns
    else None
)

if pit_flag:
    laps = laps.filter(
        ~F.coalesce(
            F.col(pit_flag),
            F.lit(False),
        )
    )

laps = laps.filter(
    F.col("driver_number").isNotNull()
    & F.col("lap_number").isNotNull()
)

# Remove duplicate laps across repeated raw snapshots.
laps = laps.dropDuplicates(
    ["year", "session_key", "driver_number", "lap_number"]
)

lap_columns = [
    "year",
    "session_key",
    "driver_number",
    "lap_number",
    "lap_duration",
    "duration_sector_1",
    "duration_sector_2",
    "duration_sector_3",
    "i1_speed",
    "i2_speed",
    "st_speed",
]

laps = keep_existing_columns(
    laps,
    lap_columns,
)

laps.write \
    .mode("overwrite") \
    .partitionBy("year", "session_key") \
    .parquet(f"{SILVER_PATH}/laps")


print("Bronze to Silver processing completed.")
print(f"Clean drivers: {drivers.count()}")
print(f"Clean laps: {laps.count()}")

spark.stop()
