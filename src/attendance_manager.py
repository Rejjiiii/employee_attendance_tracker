import csv
import os
import pandas as pd
from utils import is_valid_date, is_valid_status

DATA_FILE = "data/attendance.csv"


def add_attendance():

    print("\n--- Add Attendance ---")
    print("Type '/back' at any time to cancel and return to the main menu.")

    while True:
        emp_id, name, date, status = None, None, None, None
        step = 0

        while True:
            if step == 0:
                data = input("Enter Employee ID: ")
                if data.lower() == "/back":
                    print("Cancelled.\n")
                    return
                elif not data.strip():
                    print("Error: Employee ID cannot be empty")
                else:
                    emp_id = data.strip()
                    step += 1

            elif step == 1:
                data = input("Enter Name: ")
                if data.lower() == "/back":
                    print("Cancelled.\n")
                    return
                elif not data.strip():
                    print("Error: Name cannot be empty")
                else:
                    name = data.strip()
                    step += 1

            elif step == 2:
                data = input("Enter Date (YYYY-MM-DD): ")
                if data.lower() == "/back":
                    print("Cancelled.\n")
                    return
                elif not is_valid_date(data):
                    print("Error: Invalid date format. Use YYYY-MM-DD.")
                else:
                    date = data
                    step += 1

            elif step == 3:
                data = input("Enter Status (Present / Absent / Late): ")
                if data.lower() == "/back":
                    print("Cancelled.\n")
                    return
                elif not is_valid_status(data):
                    print("Error: Status must be one of: Present, Absent, Late.")
                else:
                    status = data
                    break

        duplicate_found = False
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, mode="r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 4:
                        continue

                    existing_id, existing_name, existing_date, existing_status = row
                    if existing_id == emp_id and existing_date == date:
                        print(
                            f"\nError: Attendance for ID '{emp_id}' on {date} already exist.\n"
                        )
                        duplicate_found = True
                        break

                    if existing_name.lower() == name.lower() and existing_date == date:
                        print(
                            f"\nError: Attendance for '{name}' on {date} already exist.\n"
                        )
                        duplicate_found = True
                        break

        if duplicate_found:
            continue

        write_header = not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0
        with open(DATA_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            if write_header:
                writer.writerow(["Employee ID", "Name", "Date", "Status"])
            writer.writerow([emp_id, name, date, status])
        print("Attendance recorded successfully.")
        break

def view_attendance():
    DATA_FILE = "data/attendance.csv"
    try:
        df = pd.read_csv(DATA_FILE)
        if df.empty:
            print("\nNo attendance records found.")
            return
    except FileNotFoundError:
        print("\nAttendance file not found.")
        return

    while True:
        print("\nView Records Options:")
        print("1. View All Records")
        print("2. View by Date")
        print("3. Return to Main Menu")
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            print("\n     -------- All Attendance Records -------     ")
            print(df.to_string(index=False))
        elif choice == "2":
            date = input("Enter date (YYYY-MM-DD): ").strip()
            # Try to standardize and filter by date
            try:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
                filtered = df[df['Date'] == date]
                if filtered.empty:
                    print(f"\nNo records found for {date}.")
                else:
                    print(f"\n  ----- Attendance Records for {date} -----  ")
                    print(filtered.to_string(index=False))
            except Exception as e:
                print("Error processing date. Please use YYYY-MM-DD format.")
        elif choice == "3":
            break
        else:
            print("Invalid input. Please try again.")