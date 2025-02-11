import pandas as pd
from datetime import datetime, date

#Drop lines with null values
def drop_nulls(df):
    df = df.dropna()
    return(df)

#Fix the column data types 
def fix_format(df):
    df[['date_of_birth', 'signup_date']] = df[['date_of_birth','signup_date']].apply(pd.to_datetime)
    df['subscription_status'] = df['subscription_status'] == 'active'
    return(df)

#Add "@" to the emails that are missing it
def fix_email(df):
    df['email'] = df['email'].apply(lambda x: x.replace('example.', '@example.') if '@' not in x else x)
    return df


#Calculate age based on the given birthdate
def calculate_age(df):
    today = pd.to_datetime('today')
    df['age'] = today.year - df['date_of_birth'].dt.year
    df['age'] -= ((today.month < df['date_of_birth'].dt.month) | 
              ((today.month == df['date_of_birth'].dt.month) & (today.day < df['date_of_birth'].dt.day))).astype(int)
    return (df)


#Calculate subscription time in years based on the given signup date, set 0 for unsigneds
def calculate_sub_time(df):
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    today = pd.to_datetime(datetime.today().strftime('%Y-%m-%d'))
    df['subscription_time'] = 0
    df.loc[df['subscription_status'] == True, 'subscription_time'] = ((today - df['signup_date']).dt.days / 365.25)
    return df


#Create a column with the age_group
def separate_age_group(df):
    df["age_group"] = df["age"].apply(lambda age: f"{(age // 10) * 10}-{(age // 10) * 10 + 9}")
    return df


#Agg the data by age_group
def agg_by_age(df):
    df = df.groupby(df['age_group']).agg(
        total_users=('id', 'count'),
        active_users=('subscription_status', lambda x: (x == True).sum()),
        inactive_users=('subscription_status', lambda x: (x == False).sum()),
        avg_sub_time_for_active_users=('subscription_time', lambda x: x[df.loc[x.index, 'subscription_status'] == True].mean())
    ).reset_index()
    return df


#Agg the data by subscription status
def agg_by_status(df):
    df = df.groupby(df['subscription_status']).agg(
        total_users=('id', 'count'),
        avg_age=('age','mean'),
        avg_subscription_time=('subscription_time', 'mean')
    ).reset_index()
    return df