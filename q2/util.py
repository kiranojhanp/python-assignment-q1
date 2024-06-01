
def get_input(prompt, input_type=str, valid_options=None, required=True):
    """
    Gets user input with type validation, option restrictions, and required input handling.

    Args:
        prompt (str): The prompt to display to the user.
        input_type (type, optional): The expected data type of the input (default: str).
        valid_options (list, optional): A list of valid options for the input (default: None).
        required (bool, optional): Whether the input is required (default: True).

    Returns:
        The validated and converted user input.
    """
    while True:
        user_input = input(prompt).strip()

        # Check if input is required
        if required and not user_input:
            print("Input is required. Please try again.")
            continue

        # Check if input is a valid option
        if valid_options and user_input not in valid_options:
            print(f"Invalid input. Please choose from: {valid_options}")
            continue

        # Attempt to convert input to the specified type
        try:
            converted_input = input_type(user_input)
            return converted_input
        except ValueError:
            print(f"Invalid input type. Please enter a valid {input_type.__name__}.")

# USAGE
# file_path = get_input("Enter file path: ")
# quantity = get_input("Enter quantity: ", int)
# choice = get_input("Choose an option (A, B, C): ", valid_options=["A", "B", "C"])
# optional_input = get_input("Enter optional info (or press Enter to skip): ", required=False)