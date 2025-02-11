# RID190521_Desafio06



## Description
This repository contains the implementation of a data pipeline that ingests raw data from a CSV file on the local machine, processes it, and stores it in three distinct layers: bronze, silver, and gold. The pipeline is executed using Docker and Apache Airflow to manage the workflow and ensure smooth orchestration.

The primary purpose of this project is to demonstrate a structured approach to data processing and storage, utilizing Docker for environment management and Airflow to automate the execution of each step in the pipeline.



## Repository Structure
This project consists of three .py files located in /airflow/dags/app, which define the functions used in the DAG tasks, one .py file located in /airflow/dags, which defines the DAG, and two Jupyter Notebooks used to explore the data between each stage of the process.

  ### /airflow/dags/app/**extractor_loader.py**
   - Define the functions used to extract and load data, extracting data from *.csv* files and saving it in both *.csv* and *.parquet* formats.
  
  ### /airflow/dags/app/**transformer.py**
   - Define functions to transform the data according to the needs observed in the notebooks.

  ### /airflow/dags/app/**organizer.py**
   - Organizes functions for the main DAG, improving code cleanliness and maintenance.

  ### /airflow/dags/**orders_dag.py**
   - Define and configure the DAG, seting the tasks and the order run order.  

  ### bronze_data_analysis.ipynb 
  - This file analyzes the extracted data, checking for null values, input errors, and incorrect date formats. It also tests some solutions that are applied in the DAGs, in the files Transformer.py and Extractor_loader.py.
  
  ### silver_data_analysis.ipynb 
  - This file analyzes the cleaned data by creating new columns and exploring it through various grouping methods.

  ### Especificacoes_do_Projeto
  - Define the project specifications. The file is in Portuguese until the project is reviewed by DNC; after that, it will be translated into English.



## Project Structure
- **Raw Data**: .csv file provided by the challenge.
- **Bronze Layer**: Ingests raw data from CSV and stores it with the extraction date.
- **Silver Layer**: Cleans and transforms the data, preserving the extraction date.
- **Gold Layer**: Stores the final processed data in .parquet format, with key aggregations saved as .csv.

  

## Installation
To run this project, you need to have Python and Jupyter Notebook installed on your local machine. Follow the steps below to set up the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/tigureis/RID190521_Desafio06.git
   cd RID190521_Desafio06

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`

3. Install the required packages:
   ```bash
   pip install -r requirements.txt

4. Initialize and start Docker (if not already running):
Ensure Docker is installed and running on your machine. If needed, start Docker manually or use the command:
   ```bash
   docker info
   
If Docker is not running, you can start it manually:

 - On Windows/Mac:
Open the Docker Desktop application. It will start Docker and you should see a Docker icon in the system tray once it is running.

 - On Linux:
Use the following command to start Docker:
   ```bash
   sudo systemctl start docker

5. Set up and start Apache Airflow:

  a)Create the directories needed are not present in your project create then using de command below
  
  ```bash
  mkdir -p ./dags ./logs ./plugins ./config ./data
  echo -e "AIRFLOW_UID=$(id -u)" > .env
  ```
  
  b) Initialize Airflow:
   
   ```bash
   docker-compose up airflow-init
   ```

  c) Start Airflow services:
   ```bash
   docker-compose up -d
   ```



## Usage

- Access the Airflow web interface:
    
  - Access Airflow at: http://localhost:8080
  - Default login credentials (if required):
    
    - Username: airflow
    
    - Password: airflow
   
- Finde and run the dag Orders_Dag

- Use the Jupyter Notebooks on Main to analyze the data

- Modify the files .py on airflow/dag and airlfow/dag/app to fit your aplication needs
   
