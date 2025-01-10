README

HEALTHCARE PROJECT:
This is my first data engineering project which shows the process of taking records of patients and various costs and using them for insights.
The process does have various parts which i would mention and explain:

1. The DE model: The data Engineering model showcases the diagram explaining the process from ingesting the raw data through to the 
		finished aggregates used for data anlysis

2. Medallion_Architecture: This folder contains a further 4 folders, Landing_zone, Bronze, Silver, Gold. These represent the data at 
			   various levels of the process. Landing_zone being where the raw data is from the sources. Bronze being the data 
			   converted to a delta table format and cleaned. Silver having the data joined and further cleaned for duplicates,
			   Gold being the final stage for the aggregates.

3. Med_configs: This contains the links or paths to the various folders in the medallion architecture which are run at the start of each 
		process allowing quicker access to the data at each level.

4. Health_ingest_bronze: This file ingest the raw data performs the initial cleaning process and saves the data in the delta format.

5. Health_ingest_silver: This file transforms the data performing various joins and further cleaning with duplicats. 
		 	  This is also saved in the delta format.