# HEALTHCARE PROJECT:

This is my first data engineering project which shows the process of taking records of patients and various costs and using them for insights.
The process does have various parts which I would mention and explain:

`The DE model`: The data Engineering model showcases the diagram explaining the process from ingesting the raw data through to the finished aggregates used for data analysis

`Medallion_Architecture`: This folder contains a further 4 folders, Landing zone, Bronze, Silver, Gold. These represent the data at various levels of the process. Landing zone being where the raw data from the sources is stored without any adjustments made. Bronze being where the data is converted to a delta table format and cleaned. Silver having the necessary data joined and further cleaned for duplicates. Gold being the final stage for the aggregates.

`Health_ingest_bronze`: This file ingests the raw data performs the initial cleaning process and saves the data in the delta format.

`Health_trans_silver`: This file transforms the data performing various joins and further cleaning with duplicates. This is also saved in the delta format.

`Health_agg_gold`: This file contains the scripts that perform aggregations for various business requirements which would allow other data departments and stakeholders to perform further analysis such as Insurance costs, Types of Health occurences e.t.c.
