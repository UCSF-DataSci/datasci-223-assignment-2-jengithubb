import polars as pl
import os

def analyze_patient_cohorts(input_file: str) -> pl.DataFrame:
    """
    Analyze patient cohorts based on BMI ranges.
    
    Args:
        input_file: Path to the input CSV file
        
    Returns:
        DataFrame containing cohort analysis results with columns:
        - bmi_range: The BMI range (e.g., "Underweight", "Normal", "Overweight", "Obese")
        - avg_glucose: Mean glucose level by BMI range
        - patient_count: Number of patients by BMI range
        - avg_age: Mean age by BMI range
    """
    # Convert CSV to Parquet for efficient processing
    # BUG: No error handling if file no exist
    # FIX: Added error handling to check if the file exists
    # FIX: Imported os to make sure file exists in the directory
    if os.path.exists(input_file):
        pl.read_csv(input_file).write_parquet("patients_large.parquet")
    else:
        return None
    
    # Create a lazy query to analyze cohorts
    cohort_results = pl.scan_parquet("patients_large.parquet").pipe(
        lambda df: df.filter((pl.col("BMI") >= 10) & (pl.col("BMI") <= 60))
    ).pipe(
        lambda df: df.select(["BMI", "Glucose", "Age"])
    ).pipe(
        lambda df: df.with_columns(
            #BUG: misalignment, labels should be one more than the breaks
            #FIX: The syntax for this pl, we should only include the middle cuts,
            #  the first and last range is already specific earlier
            pl.col("BMI").cut(
                breaks=[18.5, 25, 30],
                labels=["Underweight", "Normal", "Overweight", "Obese"],
                left_closed=True
            ).alias("bmi_range")
        )
    ).pipe(
        # BUG: groupby missing a underscore
        # FIX: make groupby into group_by
        lambda df: df.group_by("bmi_range").agg([
            pl.col("Glucose").mean().alias("avg_glucose"),
            pl.count().alias("patient_count"),
            pl.col("Age").mean().alias("avg_age")
        ])
    ).collect(streaming=True)
    
    return cohort_results

def main():
    # Input file
    input_file = "patients_large.csv"
    
    # Run analysis
    results = analyze_patient_cohorts(input_file)
    if results is None:
        return 1
    # Print summary statistics
    print("\nCohort Analysis Results:")
    print(results)

if __name__ == "__main__":
    main() 