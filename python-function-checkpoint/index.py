def calculator():
    # Get user input for the first number and convert it to a float.
    first_num = float(input("Enter first number: "))
    # Get user input for the second number and convert it to a float.
    second_num = float(input("Enter second number: "))
    # Get user input for the desired arithmetic operator.
    operator = input("Select an operator (+, -, *, /): ")

    # A dictionary that maps operator symbols to lambda functions performing the calculation.
    operations = {
        "+": lambda: first_num + second_num,
        "-": lambda: first_num - second_num,
        "*": lambda: first_num * second_num,
        # The lambda for division includes a check to prevent division by zero.
        "/": lambda: first_num / second_num if second_num != 0 else None
    }

    # Validate if the entered operator is a valid key in the 'operations' dictionary.
    if operator not in operations:
        print("Error: Invalid operator.")
        return

    # A specific check for division by zero to provide a clear error message to the user.
    if operator == "/" and second_num == 0:
        print("Error: Cannot divide by zero.")
        return

    # Retrieve the appropriate lambda function from the dictionary and call it to get the result.
    calculation_result = operations[operator]()

    # The result from the operation is cast to an integer, truncating any fractional part.
    result = int(calculation_result)

    # Display the final result in a user-friendly format.
    print(f"The result of {int(first_num)} {operator} {int(second_num)} is {result}")


# This standard Python construct ensures that the calculator() function is called
# only when the script is executed directly.
if __name__ == "__main__":
    calculator()