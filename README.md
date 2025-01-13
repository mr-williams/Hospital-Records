# HEALTHCARE PROJECT:

This is my first data engineering project which shows the process of taking records of patients, the various costs, how much their insrance covers (if they have insurance)  and using them for insights.
The process does have various parts which I would mention and explain:

`The DE model`: The data Engineering model showcases the diagram explaining the process from ingesting the raw data through to the finished aggregates used for data analysis.

![image](https://github.com/user-attachments/assets/286d326f-9b42-48a2-b0d5-3568191dec42)


`Medallion_Architecture`: This folder contains a further 4 folders, Landing zone, Bronze, Silver, Gold. These represent the data at various levels of the process. Landing zone being where the raw data is from the sources. Bronze being the data converted to a delta table format and cleaned. Silver having the data joined and further cleaned for duplicates. Gold being the final stage for the aggregates.

 `Health_ingest_bronze`: This file ingests the raw data performs the initial cleaning process and saves the data in the delta format.

 `Health_ingest_silver`: This file transforms the data performing various joins and further cleaning with duplicates. This is also saved in the delta format.
