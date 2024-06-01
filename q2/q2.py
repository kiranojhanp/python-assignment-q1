import csv
import sys
import os

from models import Customer, Sale
from util import get_input

MIN_CUSTOMER_ID = 100000
MIN_SALE_ID = 100000000
MENU_TEXT = """
Menu:
1. Load customer and sales records
2. Save customer records
3. Save sales records
4. Add new customer
5. Add new sales record (for existing customer)
6. Search customers
7. Search sales records
8. Display all sales for a customer
9. Delete a sale record with a given transaction id
10. Delete customer (and associated sales)
11. Quit
"""

data = {}


class DataManager:
    def __init__(self):
        global data

        self.customers = {}  # Use a instance variable to store customer data
        self.next_customer_id = MIN_CUSTOMER_ID
        self.next_sale_id = MIN_SALE_ID

        

    def add_customer(self, name, postcode="", phone_number=""):
        customers = data["customers"]
        if customers:
            max_existing_id = max([int(record["cust_id"]) for record in customers])
            customer_id = max(
                MIN_CUSTOMER_ID, max_existing_id + 1
            )  # Start from 100000 or next available ID
        else:
            customer_id = MIN_CUSTOMER_ID

        while customer_id in customers:
            customer_id += 1

        customer = Customer(customer_id, name, postcode, phone_number)
        data["customers"].append(customer)

        print(f"Customer added with ID: {customer_id}")
        return customer

    def add_sale(self, customer_id, date, category, value):
        if customer_id in self.customers:
            sale_id = self.next_sale_id
            self.next_sale_id += 1
            sale = Sale(sale_id, customer_id, date, category, value)
            self.customers[customer_id].sales.append(sale)
            print(f"Sale added with transaction ID: {sale_id}")
        else:
            print(f"Error: Customer with ID {customer_id} not found.")

    def load_data(self, customer_file, sales_file):
        """Loads customer and sales data from CSV files into a dictionary."""
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

    def save_data(self, file_path, key):
        """Saves customer or sales data from the dictionary to a CSV file."""
        if key not in data:
            print(f"No {key} data to save.")
            return

        if os.path.exists(file_path):
            overwrite = get_input(
                f"File '{file_path}' exists. Overwrite? (y/n): ",
                valid_options=["y", "n"],
            )
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
    data_manager = DataManager()

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

            data_manager.load_data(customer_file, sales_file)
            if "customers" in data and "sales" in data:
                print("Data loaded successfully.")

        elif choice == 2:
            file_path = get_input("Enter file path to save customer records: ")
            data_manager.save_data(file_path, "customers")
        elif choice == 3:
            file_path = get_input("Enter file path to save sale records: ")
            data_manager.save_data(file_path, "sales")
        elif choice == 4:
            name = get_input("Enter customer name: ")
            postcode = get_input("Enter customer postcode (optional): ", required=False)
            phone_number = get_input(
                "Enter customer phone number (optional): ", required=False
            )
            data_manager.add_customer(name, postcode, phone_number)
        elif choice == 11:
            break
        else:
            print("Invalid choice.")


main()
