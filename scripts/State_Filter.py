# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 22:09:45 2025

@author: Puneeth Velivela
"""

import os
print(os.getcwd())  # Get current working directory

os.chdir('D:\MS\GMU\COURSE\DAE-690\DATASETS')  # Change directory
print(os.getcwd())  # Confirm the change

import pandas as pd

# Import only one sheet from the state list Excel file
df_states = pd.read_excel('D:/MS/GMU/COURSE/DAE-690/DATASETS/state_province_list.xlsx', sheet_name='State and Province List')

# Display the first few rows
print(df_states.head())

df_original = pd.read_excel('D:/MS/GMU/COURSE/DAE-690/DATASETS/USGS_cwbData_variables.xlsx', sheet_name='cwbData')
print(df_original.head())

print(df_original['State'].unique())
# Count the number of records with NaN in the 'State' column
nan_state_count = df_original['State'].isna().sum()

# Display the result
print(f"Number of records with 'State' as NaN: {nan_state_count}")

df_missing_states = df_original[df_original['State'].isna()]
import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Initialize the geolocator with a custom user-agent
geolocator = Nominatim(user_agent="AtlanticFlywayProject")

# Function to get the state from latitude and longitude
def get_state(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True, timeout=10)
        if location:
            address = location.raw.get('address', {})
            return address.get('state', 'State Not Found')
    except GeocoderTimedOut:
        return "Timeout Error"  
    except Exception as e:
        return f"Error: {e}"


# Identify rows where 'State' is missing (NaN)
missing_state_rows = df_missing_states[df_missing_states['State'].isna()]

# Loop through missing state rows and update state using latitude & longitude
for index, row in missing_state_rows.iterrows():
    if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):  # Ensure coordinates exist
        state_name = get_state(row['Latitude'], row['Longitude'])
        if state_name:
            df_missing_states.at[index, 'State'] = state_name  # Update the dataset
    
    time.sleep(1)  # Pause to avoid hitting rate limits

print("Missing state values have been updated based on latitude and longitude.")

print(df_missing_states['State'].unique())

# Merge updated state values into the original dataset
df_original.update(df_missing_states)


df_states = df_states.dropna(subset=['ABB'])
df_states['ABB'] = df_states['ABB'].replace('PEI', 'PE')
df_original['State'] = df_original['State'].replace('Rhode Island','RI')
# Extract the list of valid state abbreviations
valid_states = df_states['ABB'].tolist()

# Filter the main dataset to include only rows where 'State' is in valid_states
df_filtered = df_original[df_original['State'].isin(valid_states)]
df_removed = df_original[~df_original['State'].isin(valid_states)]

# Save the cleaned dataset (optional)
df_filtered.to_excel('filtered_dataset.xlsx', index=False)
df_removed.to_excel('Removed_States.xlsx', index=False)
# Display the result
print(df_filtered.head())

initial_count = len(df_original)
final_count = len(df_filtered)
records_deleted = initial_count - final_count
# Display the result
print(f"Initial number of records: {initial_count}")
print(f"Final number of records: {final_count}")
print(f"Number of records deleted: {records_deleted}")


# Count duplicate records
duplicate_count = df_original.duplicated(keep=False).sum()
print(f"Total number of duplicate records: {duplicate_count}")