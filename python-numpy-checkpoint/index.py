# Import the numpy library, a fundamental package for scientific computing in Python.
import numpy as np

# Load data from the CSV file "Loan_prediction_dataset.csv".
data = np.genfromtxt(
    "Loan_prediction_dataset.csv",
    delimiter=",",  # The values in the file are separated by commas.
    dtype=str,      # Read all columns as strings to handle potential missing values.
    skip_header=1   # Skip the first row, which is the header.
)

# Extract the 9th column (index 8), which contains the loan amounts.
# The ':' selects all rows.
loan_amount = data[:, 8]

# Filter out empty strings from the loan_amount array and convert the remaining values to float.
# This handles missing loan amount values, which are represented as empty strings.
filtered_loan_amount = loan_amount[loan_amount != ""].astype(float)


# Calculate the mean of the loan amounts and round it down to the nearest integer.
loan_amount_mean = np.floor(np.mean(filtered_loan_amount))

# Calculate the median of the loan amounts and round it down to the nearest integer.
loan_amount_median = np.floor(np.median(filtered_loan_amount))

# Calculate the standard deviation of the loan amounts and round it down to the nearest integer.
loan_amount_standard_deviation = np.floor(np.std(filtered_loan_amount))

# Print the calculated statistics.
print(f"The mean of the loan amount is: {loan_amount_mean}")
print(f"The median of the loan amount is: {loan_amount_median}")
print(f"The standard deviation of the loan amount is: {loan_amount_standard_deviation}")
