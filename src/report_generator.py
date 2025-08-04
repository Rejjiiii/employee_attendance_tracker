import pandas as pd
from datetime import datetime
import csv
import os

ATTENDANCE_FILE = "data/attendance.csv"
REPORT_FILE = "reports/summary_report.csv"

# Generate and display report, with optional date/month filter
def generate_report_menu():
    while True:
        print("\nReport Options:")
        print("1. Full Report")
        print("2. Filter by Date/Month")
        print("3. Export Report to CSV")
        print("4. Return to Main Menu")
        sub_choice = input("Enter your choice (1-4): ").strip()
        if sub_choice == "1":
            generate_report()
        elif sub_choice == "2":
            filter_date = input("Enter date (YYYY-MM-DD) or month (YYYY-MM): ").strip()
            generate_report(filter_date)
        elif sub_choice == "3":
            export_report_to_csv()
        elif sub_choice == "4":
            break
        else:
            print("Invalid input. Please try again.")

def generate_report(filter_date=None):
    try:
        df = pd.read_csv(ATTENDANCE_FILE)
    except FileNotFoundError:
        print("No attendance records found.")
        return
    if df.empty:
        print("No records to analyze.")
        return
    
    # This function only generates and displays the report. Menu logic should be handled elsewhere.
    # Standardize date format to YYYY-MM-DD
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Drop rows with invalid dates
    df = df.dropna(subset=['Date'])
    if filter_date:
        if len(filter_date) == 7:  # YYYY-MM
            df = df[df['Date'].str.startswith(filter_date)]
        elif len(filter_date) == 10:  # YYYY-MM-DD
            df = df[df['Date'] == filter_date]
    if df.empty:
        print("No records for the given date/month.")
        return
    summary = df.groupby(['EmployeeID', 'Name', 'Status']).size().unstack(fill_value=0)
    summary['Total'] = summary.sum(axis=1)
    summary['Attendance %'] = (summary.get('Present', 0) / summary['Total'] * 100).round(2)
    print("\n--- Attendance Report ---")
    print(summary)
    # Perfect attendance
    # Ensure 'Absent' and 'Late' columns exist, if not, create them with 0s
    if 'Absent' not in summary:
        summary['Absent'] = 0
    if 'Late' not in summary:
        summary['Late'] = 0
    perfect = summary[(summary['Absent'] == 0) & (summary['Late'] == 0)]
    if not perfect.empty:
        print("\nEmployees with perfect attendance:")
        print(perfect.index.get_level_values('Name').tolist())
    # Top 3 most absent
    if 'Absent' in summary:
        top_absent = summary['Absent'].sort_values(ascending=False).head(3)
        print("\nTop 3 most absent employees:")
        for idx, val in top_absent.items():
            print(f"{summary.loc[idx].name[1]}: {val} absences")

def export_report_to_csv():
    try:
        df = pd.read_csv(ATTENDANCE_FILE)
    except FileNotFoundError:
        print("No attendance records found.")
        return
    if df.empty:
        print("No records to export.")
        return
    summary = df.groupby(['EmployeeID', 'Name', 'Status']).size().unstack(fill_value=0)
    summary['Total'] = summary.sum(axis=1)
    summary['Attendance %'] = (summary.get('Present', 0) / summary['Total'] * 100).round(2)
    summary.to_csv(REPORT_FILE)
    print(f"Report exported to {REPORT_FILE}.")
