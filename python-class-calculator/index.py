# Import the math module to access mathematical functions.
import math

class Calculator:
    """
    A class to represent a simple calculator that can be extended with new operations.
    """
    def __init__(self):
        """
        Initializes the Calculator with basic arithmetic operations.
        """
        self.operations = {
            "+": lambda x, y: x + y, # Addition
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y
        }

    def add_math_operation(self, symbol, function):
        """Add a new operation to the dictionary."""
        # Adds a new operation to the operations dictionary.
        # 'symbol' is the character representing the operation (e.g., '+').
        # 'function' is the lambda or function that performs the calculation.
        self.operations[symbol] = function

    def calculate_value(self, first_num, math_operator, second_num):
        """
        Performs a calculation based on the provided numbers and operator.

        Args:
            first_num (float): The first number in the calculation.
            math_operator (str): The symbol for the mathematical operation.
            second_num (float): The second number in the calculation.
        """
        # Check that both inputs are numbers
        if not isinstance(first_num, (int, float)):
            print("Error: The first value must be a number.")
            raise TypeError("First value must be a number.")

        if not isinstance(second_num, (int, float)):
            print("Error: The second value must be a number.")
            raise TypeError("Second value must be a number.")

        # Check whether the operation exists
        if math_operator not in self.operations:
            print(f"Error: '{math_operator}' is not a valid operation.")
            raise ValueError(f"Invalid operation: {math_operator}")

        # Handle division by zero
        if math_operator == "/" and second_num == 0:
            print("Error: Cannot divide by zero.")
            raise ZeroDivisionError("Cannot divide by zero.")

        # Perform the calculation
        return self.operations[math_operator](first_num, second_num)


# Advanced mathematical functions

def exponentiation(x, y):
    """
    Calculates the result of raising x to the power of y.
    """
    return math.pow(x, y)


def square_root(x, y=None):
    """
    Calculates the square root of x.
    The 'y' parameter is ignored, allowing it to fit the two-argument structure.
    """
    # The square root is not defined for negative numbers.
    if x < 0:
        raise ValueError("Cannot calculate the square root of a negative number.")
    return math.sqrt(x)


def logarithm(x, y=None):
    """
    Calculates the natural logarithm of x.
    The 'y' parameter is ignored.
    """
    # The logarithm is only defined for positive numbers.
    if x <= 0:
        raise ValueError("Logarithm is only defined for positive numbers.")
    return math.log(x)


# Create an instance of the Calculator class.
calculator = Calculator()

# Extend the calculator with advanced mathematical functions.
# The add_math_operation method is used to add new capabilities.
calculator.add_math_operation("^", exponentiation)
calculator.add_math_operation("sqrt", square_root)
calculator.add_math_operation("log", logarithm)


# Main program
# This section handles the user interface and interaction.
print("=== Python Calculator ===")
print("Available operations:")
print("+  Addition")
print("-  Subtraction")
print("*  Multiplication")
print("/  Division")
print("^  Exponentiation")
print("sqrt  Square Root")
print("log  Natural Logarithm")
print("q  Quit")

# Start an infinite loop to keep the calculator running until the user quits.
while True:
    try:
        # Prompt the user to enter an operation. .strip() removes leading/trailing whitespace.
        operation = input("\nEnter an operation: ").strip()

        # Check if the user wants to quit the program.
        if operation.lower() == "q":
            print("Thank you for using the calculator!")
            break # Exit the while loop.

        # Handle operations that only require a single number (unary operations).
        if operation in ["sqrt", "log"]:
            # Get the number from the user and convert it to a float.
            number = float(input("Enter a number: "))

            # Call the calculate method. A dummy value of 0 is passed for the second number.
            result = calculator.calculate_value(number, operation, 0)
            print(f"Result: {result}")

        else:
            # Handle operations that require two numbers (binary operations).
            # Get the first number from the user.
            first_user_number = float(input("Enter the first number: "))
            # Get the second number from the user.
            second_user_number = float(input("Enter the second number: "))

            # Perform the calculation using the user's input.
            result = calculator.calculate_value(
                first_user_number,
                operation,
                second_user_number
            )

            # Display the result to the user.
            print(f"Result: {result}")

    # Catch specific errors that might occur during execution.
    except ValueError as error:
        print(f"Error: {error}")

    except TypeError as error:
        print(f"Error: {error}")

    except ZeroDivisionError as error:
        print(f"Error: {error}")

    # Catch any other unexpected errors.
    except Exception as error:
        print(f"An unexpected error occurred: {error}")