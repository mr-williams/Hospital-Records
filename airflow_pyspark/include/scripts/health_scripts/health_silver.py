from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, col, count, countDistinct, sum, avg, lit, to_timestamp, coalesce
from pyspark.sql.types import StructField, StructType, StringType, IntegerType, DoubleType
from delta.tables import *
from delta import *
from delta import configure_spark_with_delta_pip

builder = SparkSession \
        .builder \
        .appName('healthcare_transformation')\
        .master('local')\

spark = configure_spark_with_delta_pip(builder).getOrCreate()


bronze_folder = "include/health_data/bronze"
silver_folder = "include/health_data/silver"


patients = spark.read \
                .format("delta").load(f"{bronze_folder}/healthcare_delta/patients")

patients.printSchema()


encounters = spark.read \
                .format("delta").load(f"{bronze_folder}/healthcare_delta/encounters") \
                .withColumnRenamed("REASONCODE", "REASONCODE_EN") \
                .withColumnRenamed("REASONDESCRIPTION", "REASONDESCRIPTION_EN")

encounters.printSchema()


procedure = spark.read \
                .format("delta").load(f"{bronze_folder}/healthcare_delta/procedure")

procedure.printSchema()


payers = spark.read \
            .format("delta").load(f"{bronze_folder}/healthcare_delta/payers") \
            .withColumnRenamed("CITY", "PAYER_CITY") \
            .withColumnRenamed("payers_id", "PAYERS_ID")

payers.printSchema()


combined_pe = patients.join(encounters, patients.PATIENTS_ID == encounters.PATIENT_ID) \
                      .join(procedure, encounters.PATIENT_ID == procedure.PATIENT_ID) \
                      .join(payers, encounters.PAYER == payers.PAYERS_ID)
                      
combined_pe.printSchema()


final_df = combined_pe.select("PATIENTS_ID", "FIRST", "LAST","GENDER", "CITY","BIRTHDATE","DEATHDATE","ENCOUNTERCLASS","REASONCODE", "REASONDESCRIPTION",
                             "BASE_COST", "BASE_ENCOUNTER_COST", "TOTAL_CLAIM_COST", "PAYER", "PAYER_COVERAGE","PAYER_NAME" 
                   )\
                   .withColumn("INGESTION_DATE", current_timestamp())\
                   .withColumn("MODIFICATION_DATE", current_timestamp())\
                   .withColumn("SOURCE", lit("Kaggle"))

final_df.printSchema()

final_df_dropped = final_df.dropDuplicates()



try:
    final_df_dropped.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{silver_folder}/healthcare_trans")
    print("table created")
except Exception as e:
    print("Table creation failed")
    print (e)


spark.stop
