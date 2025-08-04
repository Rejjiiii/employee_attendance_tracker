# 🕒 Employee Attendance Tracker and Analyzer (Python CLI)

A command-line based tool to manage and analyze employee attendance using CSV and pandas. Ideal for small teams or personal use.

---

## 📦 Project Structure

employee_attendance_tracker/
│
├── data/ # Stores raw attendance data
│ └── attendance.csv # Main CSV file for attendance records
│
├── reports/ # Stores generated reports
│ └── summary_report.csv # Auto-generated summary report
│
├── src/ # Source code for the CLI tool
│ ├── main.py # Entry point; CLI menu interface
│ ├── attendance_manager.py # Add and view attendance records
│ ├── report_generator.py # Generate reports using pandas
│ └── utils.py # Common helper functions (e.g., validations)
│
├── tests/ # Test scripts (optional)
│ └── test_attendance.py # Example test cases
│
├── requirements.txt # Required Python libraries
├── README.md # Project overview and setup guide
└── .gitignore # Git ignored files and folders


## 🚀 Features

- Add attendance entries with input validation
- View all existing records
- Generate attendance reports with:
  - Days present, absent, late
  - Attendance percentage
  - Highlight perfect attendance
  - Top 3 most absent employees
- Filter report by date or month
- Export report to `summary_report.csv`

---

## 🔧 Setup Instructions
- Install Dependencies
    - pip install -r requirements.txt

- Start the CLI app from the src folder
    - python src/main.py

### 1. (Optional) Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/Scripts/activate   # On Windows: venv\Scripts\activate