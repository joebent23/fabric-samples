# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# # Notebook 1
#
# This starter notebook is intentionally simple so the repository can be used
# as an initial Fabric Git integration target.

# CELL ********************

message = "Hello from the starter Fabric notebook."
print(message)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import Row

df = spark.createDataFrame([Row(step="fabric-git-setup", status="ready")])
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
