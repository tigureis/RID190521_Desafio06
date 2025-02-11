import pandas as pd
import os
from datetime import datetime


#Read data from a csv file and save it on a pandas df
def extractor(file_path, file_name):
    
    # Check if raw file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_name} data file not found.")
        
    # Load the data
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise RuntimeError(f"Error reading {file_name}: {e}")
        
    # Check if the file is empty
    if df.empty:
        raise ValueError(f"{file_name} file is empty.")
    
    return df


#Save data from a pandas df on a .CSV file
def csv_loader(df,target_dir,phase_name):
        
        # Ensure path directory exists or raise an error
    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to create {phase_name} directory: {e}")

    # Generate filename with today's date
    today_date = datetime.today().strftime('%Y-%m-%d')
    target_file = os.path.join(target_dir, f"{phase_name}_{today_date}.csv")
        
    # Save to target_directory
    try:
        df.to_csv(target_file, index=False)
    except Exception as e:
        raise RuntimeError(f"Failed to save {phase_name} file: {e}")
        
    print(f"Data saved to {target_file}")



#Save data from a pandas df on a .parquet file
def parquet_loader(df, target_dir, column_name, phase_name):

    #create a the target directory name, joining the imput with today's date
    today_date = datetime.today().strftime('%Y-%m-%d')
    output_dir = os.path.join(target_dir,column_name, today_date)
    
    # Ensure path directory exists or raise an error
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        raise RuntimeError(f"Failed to create {phase_name} directory {output_dir}: {e}")
    
    #create a parquet file for each group on the imputed column
    for group, data in df.groupby(column_name):
        file_path = os.path.join(output_dir, f"{column_name}_{group}_{today_date}.parquet")
        try:
            data.to_parquet(file_path, index=False)
            print(f"Saved {file_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to save Parquet file {file_path}: {e}")