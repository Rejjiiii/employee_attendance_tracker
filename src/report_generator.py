import pandas as pd
from datetime import datetime
import csv
import os

ATTENDANCE_FILE = "data/attendance.csv"
REPORT_FILE = "reports/summary_report.csv"

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
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df = df.dropna(subset=['Date'])
    if filter_date:
        import re
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        month_pattern = r"^\d{4}-\d{2}$"
        if re.match(month_pattern, filter_date):
            df = df[df['Date'].str.startswith(filter_date)]
        elif re.match(date_pattern, filter_date):
            df = df[df['Date'] == filter_date]
        else:
            print("Invalid date format. Please enter YYYY-MM-DD or YYYY-MM.")
            return
    if df.empty:
        print("No records for the given date/month.")
        return
    summary = df.groupby(['Employee ID', 'Name', 'Status']).size().unstack(fill_value=0)
    summary['Total'] = summary.sum(axis=1)
    summary['Attendance %'] = (summary.get('Present', 0) / summary['Total'] * 100).round(2)
    print("\n--- Attendance Report ---")
    print(summary)
    
    if 'Absent' not in summary:
        summary['Absent'] = 0
    if 'Late' not in summary:
        summary['Late'] = 0
    perfect = summary[(summary['Absent'] == 0) & (summary['Late'] == 0)]
    if not perfect.empty:
        print("\nEmployees with perfect attendance:")
        print(perfect.index.get_level_values('Name').tolist())
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
    summary = df.groupby(['Employee ID', 'Name', 'Status']).size().unstack(fill_value=0)
    summary['Total'] = summary.sum(axis=1)
    summary['Attendance %'] = (summary.get('Present', 0) / summary['Total'] * 100).round(2)
    summary.to_csv(REPORT_FILE)
    print(f"Report exported to {REPORT_FILE}.")
