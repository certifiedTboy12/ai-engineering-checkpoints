from random import randint


def guess_number(x):
    """
    A simple number guessing game where the user tries to guess a randomly
    generated number within a specified range.

    Args:
        x (int): The upper bound of the range for the random number (inclusive).
    """
    # Generate a random integer between 1 and x.
    random_number = randint(1, x)
    # Initialize guess to a value that cannot be the random number.
    guess = 0
    guess_count = 0

    # Loop until the user guesses the correct number.
    while guess != random_number:
        try:
            # Prompt the user for their guess.
            guess = int(input(f'Guess a number between 1 and {x}: '))
            guess_count += 1

            # Provide feedback based on the guess.
            if guess < random_number:
                print("Your guess is too low. Guess again.")
            elif guess > random_number:
                print("Your guess is too high. Guess again.")

        except ValueError:
            # Handle cases where the input is not a valid integer.
            print("Invalid input. Please enter a valid number.")

    print(f"Congratulations! You guessed the number {random_number} correctly in {guess_count} guesses!")


# This block ensures the game runs only when the script is executed directly.
if __name__ == "__main__":
    # Start the game with an upper limit of 100.
    guess_number(100)