from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, col, count, countDistinct, sum, avg
from pyspark.sql.types import StructField, StructType, StringType, IntegerType, DoubleType
from delta.tables import *
from delta import *
from delta import configure_spark_with_delta_pip


builder = SparkSession \
        .builder \
        .appName('healthcare_Aggregations')\
        .master('local')\

spark = configure_spark_with_delta_pip(builder).getOrCreate()

silver_folder = "include/health_data/silver"
gold_folder = "include/health_data/gold"

source = spark.read \
                .format("delta").load(f"{silver_folder}/healthcare_trans")             

source.printSchema()

source.createOrReplaceTempView("health")


#Insurance Analysis
pop_insurance = spark.sql("SELECT PAYER_NAME, \
                          SUM(TOTAL_CLAIM_COST) AS TOTALCLAIMCOST,\
                          AVG(PAYER_COVERAGE) AS AVERAGEPAYERCOVERAGE,\
                          COUNT(ENCOUNTERCLASS) AS TOTAL_CLAIMS\
                          FROM health \
                          GROUP BY PAYER_NAME \
                          ORDER BY AVERAGEPAYERCOVERAGE DESC")

pop_insurance.show()


#Common Encounters
encount_cases = spark.sql("SELECT ENCOUNTERCLASS, \
                          COUNT(ENCOUNTERCLASS) AS OCCURENCES,\
                          SUM(BASE_ENCOUNTER_COST) AS TOTAL_BASE_ENCOUNTER_COST,\
                          SUM(BASE_COST) AS TOTAL_BASE_COST\
                          FROM health \
                          GROUP BY ENCOUNTERCLASS \
                          ORDER BY OCCURENCES DESC")

encount_cases.show()

try:
    pop_insurance.write.format("delta").mode("overwrite").save(f"{gold_folder}/pop_insurance")
    print("table created")
except Exception as e:
    print("Table creation failed")
    print (e)


try:
    encount_cases.write.format("delta").mode("overwrite").save(f"{gold_folder}/encount_cases")
    print("table created")
except Exception as e:
    print("Table creation failed")
    print (e)


spark.stop
