# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "6e6f8ff2-5de9-45e6-aac7-1320f485a63c",
# META       "default_lakehouse_name": "Bronze_LH",
# META       "default_lakehouse_workspace_id": "be777eda-10e7-4b4a-90da-dfd1663a53eb",
# META       "known_lakehouses": [
# META         {
# META           "id": "6e6f8ff2-5de9-45e6-aac7-1320f485a63c"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
df = spark.read.json('Files/copy_to_insolvency', multiLine=True, recursiveFileLookup=True)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
