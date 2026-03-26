# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse_name": "Bronze_LH",
# META       "default_lakehouse_workspace_id": "",
# META       "known_lakehouses": []
# META     }
# META   }
# META }

# MARKDOWN ********************

# # 01 — Ingest Insolvency Data to Bronze
# 
# This notebook reads raw Companies House insolvency data from the
# `insolvency_1` shortcut (OneLake → CoHouseMedallion) and loads it
# as a Delta table in the Bronze Lakehouse.
# 
# **Data source:** Companies House bulk data product — Insolvency cases
# **Pattern:** Read raw files → minimal schema enforcement → Delta table

# CELL ********************

from pyspark.sql import functions as F
from pyspark.sql.types import *

# Read raw insolvency data from the shortcut (CSV files)
raw_path = "Files/insolvency_1"

# Try reading as CSV first (Companies House data is typically CSV)
try:
    df_raw = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .option("multiLine", "true")
        .csv(raw_path)
    )
    print(f"Successfully read {df_raw.count()} rows from insolvency shortcut")
    display(df_raw.limit(10))
except Exception as e:
    # If CSV fails, try reading as Parquet or JSON
    print(f"CSV read failed: {e}")
    try:
        df_raw = spark.read.parquet(raw_path)
        print(f"Read {df_raw.count()} rows as Parquet")
        display(df_raw.limit(10))
    except:
        df_raw = spark.read.json(raw_path)
        print(f"Read {df_raw.count()} rows as JSON")
        display(df_raw.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Add bronze audit columns
df_bronze = (
    df_raw
    .withColumn("_bronze_load_timestamp", F.current_timestamp())
    .withColumn("_bronze_source_file", F.input_file_name())
    .withColumn("_bronze_load_date", F.current_date())
)

print(f"Bronze DataFrame schema:")
df_bronze.printSchema()
print(f"Total rows: {df_bronze.count()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Write to Bronze Delta table (overwrite for full refresh)
(
    df_bronze
    .write
    .mode("overwrite")
    .format("delta")
    .saveAsTable("bronze_insolvency")
)

print("✅ Bronze insolvency table created successfully")

# Verify
display(spark.sql("SELECT COUNT(*) as row_count FROM bronze_insolvency"))
display(spark.sql("SELECT * FROM bronze_insolvency LIMIT 5"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
