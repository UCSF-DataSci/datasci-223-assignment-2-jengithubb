#!/usr/bin/env python3
"""
Patient Data Cleaner

This script standardizes and filters patient records according to specific rules:

Data Cleaning Rules:
1. Names: Capitalize each word (e.g., "john smith" -> "John Smith")
2. Ages: Convert to integers, set invalid ages to 0
3. Filter: Remove patients under 18 years old
4. Remove any duplicate records

Input JSON format:
    [
        {
            "name": "john smith",
            "age": "32",
            "gender": "male",
            "diagnosis": "hypertension"
        },
        ...
    ]

Output:
- Cleaned list of patient dictionaries
- Each patient should have:
  * Properly capitalized name
  * Integer age (≥ 18)
  * Original gender and diagnosis preserved
- No duplicate records
- Prints cleaned records to console

Example:
    Input: {"name": "john smith", "age": "32", "gender": "male", "diagnosis": "flu"}
    Output: {"name": "John Smith", "age": 32, "gender": "male", "diagnosis": "flu"}

Usage:
    python patient_data_cleaner.py
"""

import json
import os
import pandas as pd

def load_patient_data(filepath):
    """
    Load patient data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        list: List of patient dictionaries
    """
    # BUG: No error handling for file not found
    # FIX: Added try-except block to handle FileNotFoundError and return None
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
       print(f"Error: File not found: {filepath}.")
       return None

def clean_patient_data(patients):
    """
    Clean patient data by:
    - Capitalizing names
    - Converting ages to integers
    - Filtering out patients under 18
    - Removing duplicates
    
    Args:
        patients (list): List of patient dictionaries
        
    Returns:
        list: Cleaned list of patient dictionaries
    """
    cleaned_patients = []
    # Transform the dictionary into a dataframe
    df = pd.DataFrame(patients)
    
    # BUG: Typo in key 'nage' instead of 'name'
    # FIX: Changed nage to name
    df['name1'] = df['name1'].str.title()

    # BUG: Wrong method name (fill_na vs fillna)
    # FIX: Changed fill_na to fillna
    df['age'] = df['age'].fillna(0).astype(int)

    # BUG: Wrong method name (drop_duplcates vs drop_duplicates)
    # FIX: Changed duplcates to duplicates
    df = df.drop_duplicates()

    # BUG: Wrong comparison operator (= vs ==)
    # FIX: Used >= instead of == since we want to keep all the patients under 18
    df_over_18 = df[df['age'].astype(int) >= 18]
    # BUG: Logic error - keeps patients under 18 instead of filtering them out
    cleaned_data = df_over_18.to_dict(orient='records')

    # BUG: Missing return statement for empty list
    # FIX: If cleaned_data is empty, return None, else return the dictionary
    if not cleaned_data:
        return None
    
    return cleaned_data

def main():
    """Main function to run the script."""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the data file
    data_path = os.path.join(script_dir, 'data', 'raw', 'patients.json')

    # BUG: No error handling for load_patient_data failure
    # FIX: If patient data load failed, return none
    patients = load_patient_data(data_path)
    if patients is None:
        return None
    
    # Clean the patient data
    cleaned_patients = clean_patient_data(patients)
    
    # BUG: No check if cleaned_patients is None
    # FIX: If cleaned_patients is none, then return
    if cleaned_patients is None:
        return None
    
    # Print the cleaned patient data
    print("Cleaned Patient Data:")
    for patient in cleaned_patients:
        # BUG: Using 'name' key but we changed it to 'nage'
        # FIX: The above typo has been fixed
        print(f"Name: {patient['name1']}, Age: {patient['age']}, Diagnosis: {patient['diagnosis']}")
    
    # Return the cleaned data (useful for testing)
    return cleaned_patients

if __name__ == "__main__":
    main()