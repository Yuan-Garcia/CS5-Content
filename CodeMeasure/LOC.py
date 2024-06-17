#an example project for parsing
#also completely chatGPT created
def validate_input(n):
    """
    Validates that the input is a non-negative integer.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer.")
    return True

def is_base_case(n):
    """
    Checks if the base case for Fibonacci is reached.
    """
    return n in (0, 1)

def get_base_case_value(n):
    """
    Returns the Fibonacci value for the base cases.
    """
    return n

def perform_recursive_calls(n, recursive_function):
    """
    Performs the recursive calls for Fibonacci calculation.
    """
    return recursive_function(n - 1), recursive_function(n - 2)

def sum_recursive_results(result1, result2):
    """
    Sums the results of the two recursive calls.
    """
    return result1 + result2

def fibonacci(n):
    """
    Main Fibonacci function that uses recursion and helper functions.
    """
    # Step 1: Validate input
    validate_input(n)
    
    # Step 2: Check for base case
    if is_base_case(n):
        return get_base_case_value(n)

    # Step 3: Perform the recursive calls
    result1, result2 = perform_recursive_calls(n, fibonacci)

    # Step 4: Sum the results of the recursive calls
    return sum_recursive_results(result1, result2)

# Example usage:
try:
    number = 6
    result = fibonacci(number)
    print(f"The Fibonacci number for {number} is {result}.")
except ValueError as e:
    print(e)
