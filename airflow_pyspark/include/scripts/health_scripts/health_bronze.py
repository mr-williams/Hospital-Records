from pyspark.sql.functions import current_timestamp, col
from pyspark.sql.types import StructField, StructType, StringType, IntegerType, DoubleType
from pyspark.sql import SparkSession
from delta.tables import *
from delta import *
from delta import configure_spark_with_delta_pip



builder = SparkSession \
        .builder \
        .appName('healthcare_ingest')\
        .master('local')
        
spark = configure_spark_with_delta_pip(builder).getOrCreate()


landing_folder = "include/health_data/landing_zone"
bronze_folder = "include/health_data/bronze"

patients = spark.read \
            .option("inferschema", "True") \
            .option("header", "True") \
            .csv(f"{landing_folder}/health_records/patients.csv")
patients.printSchema()

patients_renamed = patients.withColumnRenamed("Id", "PATIENTS_ID")


procedure = spark.read \
            .option("inferschema", "True") \
            .option("header", "True") \
            .csv(f"{landing_folder}/health_records/procedures.csv")

procedure.printSchema()


procedure_renamed = procedure.withColumnRenamed("PATIENT", "PATIENT_ID") \
                             .withColumnRenamed("ENCOUNTER", "ENCOUNTER_ID")


encounters = spark.read \
            .option("inferschema", "True") \
            .option("header", "True") \
            .csv(f"{landing_folder}/health_records/encounters.csv")

encounters.printSchema()

encounters_renamed = encounters.withColumnRenamed("Id", "encounters_id") \
                               .withColumnRenamed("PATIENT", "PATIENT_ID")


payers = spark.read \
            .option("inferschema", "True") \
            .option("header", "True") \
            .csv(f"{landing_folder}/health_records/payers.csv")

payers.printSchema()

payers_renamed = payers.withColumnRenamed("Id", "payers_id") \
                       .withColumnRenamed("NAME", "PAYER_NAME")


organizations = spark.read \
            .option("inferschema", "True") \
            .option("header", "True") \
            .csv(f"{landing_folder}/health_records/organizations.csv")

organizations.printSchema()

organizations_renamed = organizations.withColumnRenamed("Id", "organizations_id")


description = spark.read \
            .option("inferschema", "True") \
            .option("header", "True") \
            .csv(f"{landing_folder}/health_records/data_dictionary.csv")

description.printSchema()


try:
    patients_renamed.write.format("delta").mode("overwrite").save(f"{bronze_folder}/healthcare_delta/patients")
    print("table created")
except Exception as e:
    print("Table creation failed")
    print (e)


procedure_renamed.write.format("delta").mode("overwrite").save(f"{bronze_folder}/healthcare_delta/procedure")

encounters_renamed.write.format("delta").mode("overwrite").save(f"{bronze_folder}/healthcare_delta/encounters")

payers_renamed.write.format("delta").mode("overwrite").save(f"{bronze_folder}/healthcare_delta/payers")

organizations_renamed.write.format("delta").mode("overwrite").save(f"{bronze_folder}/healthcare_delta/organizations")

description.write.format("delta").mode("overwrite").save(f"{bronze_folder}/healthcare_delta/description")


spark.stop