# HEALTHCARE PROJECT:

This is my first data engineering project which shows the process of taking records of patients, the various costs, how much their insrance covers (if they have insurance)  and using them for insights.
The process does have various parts which I would mention and explain:

`The DE model`: The data Engineering model showcases the diagram explaining the process from ingesting the raw data through to the finished aggregates used for data analysis.

![image](https://github.com/user-attachments/assets/286d326f-9b42-48a2-b0d5-3568191dec42)


`Medallion_Architecture`: This folder contains a further 4 folders, Landing zone, Bronze, Silver, Gold. These represent the data at various levels of the process. Landing zone being where the raw data from the sources is stored without any adjustments made. Bronze being where the data is converted to a delta table format and cleaned. Silver having the necessary data joined and further cleaned for duplicates. Gold being the final stage for the aggregates.

`Health_ingest_bronze`: This file ingests the raw data performs the initial cleaning process and saves the data in the delta format.

`Health_trans_silver`: This file transforms the data performing various joins and further cleaning with duplicates. This is also saved in the delta format.

`Health_agg_gold`: This file contains the scripts that perform aggregations for various business requirements which would allow other data departments and stakeholders to perform further analysis such as Insurance costs, Types of Health occurences e.t.c.

The depencies required to run this project include:
- Python 3.11.0
- Pyspark 3.5.4
- Delta-spark 3.3.0
- Java 11(jdk 11)
- Scala 2.12.8
- Apache Airflow

Apart from Java 11 and Apache Airflow, all these dependencies can be installed using (pip install) in the cmd or terminal.

The orchestration which is done by Apache Airflow can be run in a Docker container. Which requires its own set of adjustments and dependencies to create a suitable working environment for the project.
