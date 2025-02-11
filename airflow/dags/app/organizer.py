from datetime import datetime
import sys
import os

# Add the parent directory of "app" to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.extractor_loader import extractor, csv_loader, parquet_loader
from app.transformer import drop_nulls, fix_format, fix_email, calculate_age, calculate_sub_time, separate_age_group, agg_by_age, agg_by_status

"""This file organizes functions for the main DAG, improving code cleanliness and maintenance."""


def bronze_protocol():
    phase_name = 'bronze'
    file_path = "/opt/airflow/data/raw/raw_data.csv"
    file_name = "raw_data.csv"
    bronze_dir = "/opt/airflow/data/bronze"

    print(f"Loading raw data") 
    df = extractor(file_path=file_path, file_name=file_name)
    
    print(f"Loading data to the {phase_name} layer")   
    csv_loader(df=df, target_dir=bronze_dir, phase_name=phase_name)


def silver_protocol():
    phase_name = 'silver'
    bronze_dir = "/opt/airflow/data/bronze"
    today_date = datetime.today().strftime('%Y-%m-%d')
    file_name = f"bronze_{today_date}.csv"
    bronze_file_path = os.path.join(bronze_dir, file_name)
    silver_dir = "/opt/airflow/data/silver"

    print("extracting data from bronze layer")    
    df = extractor(file_path=bronze_file_path, file_name=file_name)

    print("Droping nulls")
    df = drop_nulls(df)

    print("Fixing columns format")
    df = fix_format(df)

    print("fixing mistyped emails")
    df = fix_email(df)

    print("Calculating age")
    df = calculate_age(df)

    print(f"Loading data to the {phase_name} layer") 
    csv_loader(df=df,target_dir=silver_dir,phase_name=phase_name)


def gold_protocol():
    phase_name = 'gold'
    silver_dir = "/opt/airflow/data/silver"
    today_date = datetime.today().strftime('%Y-%m-%d')
    file_name = f"silver_{today_date}.csv"
    silver_file_path = os.path.join(silver_dir, file_name)
    gold_dir = "/opt/airflow/data/gold"

    print("extracting data from silver layer")    
    df = extractor(file_path=silver_file_path, file_name=file_name)

    print("Calculating subscription time for active members")    
    df = calculate_sub_time(df)

    print("Creating age groups columns on the df")    
    age_df = separate_age_group(df)
    
    column_name = 'age_group'
    print(f"Saving Parquets grouped by {column_name}") 
    parquet_loader(df=age_df, target_dir=gold_dir, column_name=column_name, phase_name=f'{phase_name}_{column_name}')

    column_name = 'subscription_status'
    print(f"Saving Parquets grouped by {column_name}") 
    parquet_loader(df=df, target_dir=gold_dir, column_name=column_name, phase_name=f'{phase_name}_{column_name}')

    print("Aggregating data by age group for easy analysis")    
    age_df = agg_by_age(age_df)

    print(f"Saving age group analysis on a csv") 
    csv_loader(df=age_df, target_dir=os.path.join(gold_dir,'analysis','by_age'), phase_name=f'{phase_name}_age_analysis')


    print("Aggregating data by subscription status for easy analysis")    
    age_df = agg_by_status(df)

    print(f"Saving subscription status analysis on a csv") 
    csv_loader(df=age_df, target_dir=os.path.join(gold_dir,'analysis','by_status'), phase_name=f'{phase_name}_age_status')