# HW 2 analysis.md

# Explain your analysis approach
### 1. Reading the file and error handling for if the file exists
### 2. parquet
Transformed from CSV file to Parquet file, because Parquet is faster, smaller, and better for large structured data.
### 3. Error handling
Before using the data coming from the Parquet file, I created a new function that contains a set  
of error handling stuffs to make sure the data coming in is valid.
### 4. Pipe
Used pipe to connect functions together instead of doing function calls by function calls, because pipe lets me write cleaner, chainable code.
### 5. Filter, Select, Group_by data
Used these three different features to process the data, and only get the data that we want.
### 6. Lazy evaluation instead of eager evaluation
Lazy evaluation allows for more efficient memory management. Instead of loading the data into  
the memory upstraight, we only load the data when it needs to, thus saving the memory.

# Discuss any patterns or insights found
### I found out that Polar is faster because it utilizes binary data.
### Memory management is important when dealing with large files. Using lazy evaluation can reserve some memory.
### Pipe is sometimes used to enhance readability.
### Error handling is one of the most crucial parts. It ensures the system doesn't halt when unexpected input is coming in by validating all things that can be thought of.

# Describe how you used polars' features for efficiency
### In the line filtering out the data with BMI larger than 10 and smaller than 60, Polar uses bit mask manipulation, which can be way faster than normal comparison.
### There are two types of reading files we can do in Polar. One is the eager evaluation, one is the lazy evaluation. They serve different purposes, and in this case, we used lazy evaluation because it best suits large data.
