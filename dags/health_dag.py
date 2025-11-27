import os
from airflow.decorators import dag
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

@dag(
    schedule=None,
    catchup=False,
    start_date=datetime(2025, 1, 1)
)

def health_pipeline():
    bronze_ingest = SparkSubmitOperator(
        task_id = "bronze_ingest",
        application = "./include/scripts/health_scripts/health_bronze.py",
        conn_id = "local_spark",
        verbose = True,
        packages = "io.delta:delta-core_2.12:2.4.0",
        conf={
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.driver.extraJavaOptions": "--add-opens java.base/sun.nio.ch=ALL-UNNAMED",
            "spark.executor.extraJavaOptions": "--add-opens java.base/sun.nio.ch=ALL-UNNAMED"
        },
        application_args = [],
    )

    silver_trans = SparkSubmitOperator(
        task_id = "silver_trans",
        application = "./include/scripts/health_scripts/health_silver.py",
        conn_id = "local_spark",
        verbose = True,
        packages = "io.delta:delta-core_2.12:2.4.0",
        conf={
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.driver.extraJavaOptions": "--add-opens java.base/sun.nio.ch=ALL-UNNAMED",
            "spark.executor.extraJavaOptions": "--add-opens java.base/sun.nio.ch=ALL-UNNAMED"
        },
        application_args = [],
    )

    gold_aggs = SparkSubmitOperator(
        task_id = "gold_aggregations",
        application = "./include/scripts/health_scripts/health_gold.py",
        conn_id = "local_spark",
        verbose = True,
        packages = "io.delta:delta-core_2.12:2.4.0",
        conf={
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.driver.extraJavaOptions": "--add-opens java.base/sun.nio.ch=ALL-UNNAMED",
            "spark.executor.extraJavaOptions": "--add-opens java.base/sun.nio.ch=ALL-UNNAMED"
        },
        application_args = [],
    )


    bronze_ingest >> silver_trans >> gold_aggs


health_data_pipeline = health_pipeline()
