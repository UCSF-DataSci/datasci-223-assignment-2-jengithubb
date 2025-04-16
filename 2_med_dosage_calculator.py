#!/usr/bin/env python3
"""
Emergency Room Medication Calculator


This script calculates medication dosages for emergency room patients based on
standard emergency protocols. It follows weight-based dosing guidelines for common
emergency medications.


Dosing Formula:
   Base Dosage (mg) = Patient Weight (kg) × Medication Factor (mg/kg)
   Loading Dose (mg) = Base Dosage × 2 (for first dose only)


When to use Loading Doses:
   - Only for first doses of certain medications (e.g., antibiotics, anti-seizure meds)
   - Determined by 'is_first_dose' flag in the input
   - Some medications always use loading doses for first administration


Example:
   Patient: 70kg, Medication: epinephrine, Is First Dose: No
   Base Dosage = 70 kg × 0.01 mg/kg = 0.7 mg
   Final Dosage = 0.7 mg


   Patient: 70kg, Medication: amiodarone, Is First Dose: Yes
   Base Dosage = 70 kg × 5 mg/kg = 350 mg
   Loading Dose = 350 mg × 2 = 700 mg
   Final Dosage = 700 mg


Input Format:
   {
       "name": "John Smith",
       "weight": 70.0,
       "medication": "epinephrine",
       "condition": "anaphylaxis",
       "is_first_dose": false,
       "allergies": ["penicillin"]
   }


Output:
   {
       "name": "John Smith",
       "weight": 70.0,
       "medication": "epinephrine",
       "base_dosage": 0.7,
       "is_first_dose": false,
       "loading_dose_applied": false,
       "final_dosage": 0.7,
       "warnings": ["Monitor for arrhythmias"]
   }


Medication Factors (mg/kg):
   epinephrine:  0.01  (Anaphylaxis)
   amiodarone:   5.00  (Cardiac arrest)
   lorazepam:    0.05  (Seizures)
   fentanyl:     0.001 (Pain)
   ...
"""


import json
import os


# Dosage factors for different medications (mg per kg of body weight)
# These are standard dosing factors based on medical guidelines
DOSAGE_FACTORS = {
   "epinephrine": 0.01,  # Anaphylaxis
   "amiodarone": 5.00,   # Cardiac arrest
   "lorazepam": 0.05,    # Seizures
   "fentanyl": 0.001,    # Pain
   "lisinopril": 0.5,    # ACE inhibitor for blood pressure
   "metformin": 10.0,    # Diabetes medication
   "oseltamivir": 2.5,   # Antiviral for influenza
   "sumatriptan": 1.0,   # Migraine medication
   "albuterol": 0.1,     # Asthma medication
   "ibuprofen": 5.0,     # Pain/inflammation
   "sertraline": 1.5,    # Antidepressant
   "levothyroxine": 0.02 # Thyroid medication
}


# Medications that use loading doses for first administration
# BUG: Missing commas between list items
# FIX: Added commas to properly separate items in the list
LOADING_DOSE_MEDICATIONS = [
   "amiodarone",
   "lorazepam",
   "fentanyl",
]


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
  


def calculate_dosage(patient):
   """
   Calculate medication dosage for a patient.
  
   Args:
       patient (dict): Patient dictionary with 'weight', 'medication', and 'is_first_dose' keys
      
   Returns:
       dict: Patient dictionary with added dosage information
   """
   # Create a copy of the patient data to avoid modifying the original
   patient_with_dosage = patient.copy()
  
   # Extract patient information
   # BUG: No check if 'weight' key exists
   # FIX: If weight key exists in patient, proceed, if not, return with error code
   if patient.get("weight")is not None:
       weight = patient['weight']
   else:
       # add something here
       return None
   # BUG: No check if 'medication' key exists
   # FIX: If medication key exists, proceed, if not, return with error code
   if patient.get('medication') is not None:
       medication = patient['medication'] # This bug is diabolical
   else:
       # return somethinbg here
       return None
  
   # Get the medication factor
   # BUG: Adding 's' to medication name, which doesn't match DOSAGE_FACTORS keys
   # FIX: Deleting the extra s adding to the original string
   factor = DOSAGE_FACTORS.get(medication)
  
   # Calculate base dosage
   # BUG: Using addition instead of multiplication
   base_dosage = weight * factor
  
   # Determine if loading dose should be applied
   # BUG: No check if 'is_first_dose' key exists
   # FIX: If is_first_dose exist, then proceed, if not return to notify main
   if patient.get('is_first_dose') is not None:
       is_first_dose = patient.get('is_first_dose', False)
       loading_dose_applied = False
       final_dosage = base_dosage
   else:
       # return false incomplete here
       return None
  
   # Apply loading dose if it's the first dose and the medication uses loading doses
   # BUG: Incorrect condition - should check if medication is in LOADING_DOSE_MEDICATIONS
   # FIX: Only check if medication instead of checking both medication and is_first_dose in LOADING_DOSE_MEDICATIONS:
   if medication in LOADING_DOSE_MEDICATIONS:
       loading_dose_applied = True
       # BUG: Using addition instead of multiplication for loading dose
       # FIX: Used multiplication instead of addition
       final_dosage = base_dosage * base_dosage
  
   # Add dosage information to the patient record
   patient_with_dosage['base_dosage'] = base_dosage
   patient_with_dosage['loading_dose_applied'] = loading_dose_applied
   patient_with_dosage['final_dosage'] = final_dosage
  
   # Add warnings based on medication
   warnings = []
   # BUG: Typos in medication names
   # FIX: added e to epinephrin, fix the spelling of fentanyl
   if medication == "epinephrine":
       warnings.append("Monitor for arrhythmias")
   elif medication == "amiodarone":
       warnings.append("Monitor for hypotension")
   elif medication == "fentanyl":
       warnings.append("Monitor for respiratory depression")
  
   patient_with_dosage['warnings'] = warnings
  
   return patient_with_dosage


def calculate_all_dosages(patients):
   """
   Calculate dosages for all patients and sum the total.
  
   Args:
       patients (list): List of patient dictionaries
      
   Returns:
       tuple: (list of patient dicts with dosages, total medication needed)
   """
   total_medication = 0
   patients_with_dosages = []
  
   # Process all patients
   for patient in patients:
       # Calculate dosage for this patient
       patient_with_dosage = calculate_dosage(patient)
      
       # Add to our list
       patients_with_dosages.append(patient_with_dosage)
      
       # Add to total medication
       # BUG: No check if 'final_dosage' key exists
       # FIX: If final_dosage exists, then proceed, if not, return with error code
       if patient_with_dosage.get('final_dosage') is not None:
           total_medication += patient_with_dosage['final_dosage']
       else:
           return None
  
   return patients_with_dosages, total_medication


def main():
   """Main function to run the script."""
   # Get the directory of the current script
   script_dir = os.path.dirname(os.path.abspath(__file__))
  
   # Construct the path to the data file
   data_path = os.path.join(script_dir, 'data','raw', 'meds.json')
  
   # BUG: No error handling for load_patient_data failure
   patients = load_patient_data(data_path)
   if patients == None:
       return 1
  
   # Calculate dosages for all patients
   patients_with_dosages, total_medication = calculate_all_dosages(patients)
   if patients_with_dosages is None or total_medication is None:
       return 1
   
   # Print the dosage information
   print("Medication Dosages:")
   for patient in patients_with_dosages:
       # BUG: No check if required keys exist
       # FIX: Add if statement to check if the keys exist. if not, return with error
       if patient.get('name') is None or patient.get('name') is None or patient.get('name') is None or patient.get('name') is None:
           return 1


       print(f"Name: {patient['name']}, Medication: {patient['medication']}, "
             f"Base Dosage: {patient['base_dosage']:.2f} mg, "
             f"Final Dosage: {patient['final_dosage']:.2f} mg")
       if patient['loading_dose_applied']:
           print(f"  * Loading dose applied")
       if patient['warnings']:
           print(f"  * Warnings: {', '.join(patient['warnings'])}")
  
   print(f"\nTotal medication needed: {total_medication:.2f} mg")
  
   # Return the results (useful for testing)
   return patients_with_dosages, total_medication


if __name__ == "__main__":
   main()