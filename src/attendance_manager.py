import csv
import os
from utils import is_valid_date, is_valid_status

DATA_FILE = "data/attendace.csv"


def add_attendance():
    print("--- Add Attendance ---")
    emp_id = input("Enter Employee ID: ").strip()
    name = input("Enter Name: ").strip()
    date = input("Enter Date (YYYY-MM-DD): ").strip()
    status = input("Enter Status (Present / Absent / Late): ").strip().capitalize()

    if not emp_id or not name:
        print("Error: Employee ID and Name cannot be empty.")
        return
    if not is_valid_date(date):
        print("Error: Invalid date format. Use YYYY-MM-DD.")
    if not is_valid_status(status):
        print("Error: Status must be one of: Present, Absent, Late.")
        return

    try:
        file_exists = os.path.isfile(DATA_FILE)
        with open(DATA_FILE, mode="a", newline="") as file:
            writter = csv.writer(file)
            if not file_exists or os.stat(DATA_FILE).st_size == 0:
                writter.writerow(["EmployeeID", "Name", "Date", "Status"])
            writter.writerow([emp_id, name, date, status])
        print("Attendance recorded successfully.")

    except Exception as e:
        print(f"Error: Failed to write to CSV. Details {e}")
