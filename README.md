## Database Use
This database is being used to analyze songs, and how many times they are played.
This data is likely being used to find the most popular songs, and by extension, the most popular artists related to the songs played. 

## Database Design
This database schema was designed around the intent of analyzing a single Fact table to find the most relevant information possible. The supporting dimension tables can flesh out queries made against the central fact table. 

## ETL Process and Files
This ETL process is efficient at parsing the raw data into the appropriate tables. 

### The files in this package are as follows:

create_tables.py: This python file creates the database and drops it if it already exists. It also has the two functions for dropping and creating the tables necessary, it refers to the sql_queries.py file for the information necessary to create them.

sql_queries.py: This python file holds the information required to drop the tables and recreate them. It has the columns and datatypes for the tables. It also has the insert statements to insert data into those tables as well as a couple queries needed in the ETL process.

etl.ipynb: This jupyter notebook has a step by step ETL process for the data we are transforming, however this notebook only 'ETL's a few files as a proof of concept.

etl.py: This python file is built off of the jupyter notebook and is fully fleshed out to fully transform the data and log files necessary to fill out the tables in the database.

test.ipynb: This jupyter notebook is simply used as a test for the tables to see if the data had been correctly transformed and loaded into the database.