import csv
import sys
import os
from util import get_input

MENU_TEXT = """
Menu:
1. Load customer and sales records
2. Save customer records
3. Save sales records
4. Quit
"""

data = {}


def load_data(customer_file, sales_file):
    """Loads customer and sales data from CSV files into a dictionary."""
    global data
    data.clear()

    for file, key in [(customer_file, "customers"), (sales_file, "sales")]:
        try:
            with open(file, "r") as file_path:
                reader = csv.reader(file_path)
                header = next(reader)  # Skip header row
                data[key] = []

                for row in reader:
                    record = dict(zip(header, row))
                    data[key].append(record)

                if not data[key]:
                    print(f"Warning: No valid records found in {file}.")

        except FileNotFoundError as nfe:
            print(f"Error: File not found - {nfe}")
        except csv.Error as e:
            print(f"Error reading CSV file '{file_path}': {e}")
        except Exception as e:
            print(f"Unexpected error loading data: {e}")


def save_data(file_path, key):
    """Saves customer or sales data from the dictionary to a CSV file."""
    if key not in data:
        print(f"No {key} data to save.")
        return

    if os.path.exists(file_path):
        overwrite = get_input(f"File '{file_path}' exists. Overwrite? (y/n): ",  valid_options=["y", "n"])
        if overwrite.lower() != "y":
            print("Operation cancelled.")
            return

    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        header = list(data[key][0].keys())  # Get header from data
        writer.writerow(header)

        for row in data[key]:
            writer.writerow(row.values())  # Write values only

        print(f"{key.capitalize()} records saved to {file_path}")


def main():
    """Main function to handle user interaction and menu options."""
    while True:
        print(MENU_TEXT)

        choice = get_input("Enter your choice: ", int)

        if choice == 1:
            if len(sys.argv) >= 3:
                customer_file = sys.argv[1]
                sales_file = sys.argv[2]
            else:
                customer_file = get_input("Enter customer records file path: ")
                sales_file = get_input("Enter sales records file path: ")

            load_data(customer_file, sales_file)
            if "customers" in data and "sales" in data:
                print("Data loaded successfully.")

        elif choice == 2:
            file_path = get_input("Enter file path to save customer records: ")
            save_data(file_path, "customers")
        elif choice == 3:
            file_path = get_input("Enter file path to save sale records: ")
            save_data(file_path, "sales")
        elif choice == 4:
            break
        else:
            print("Invalid choice.")


main()
