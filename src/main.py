from attendance_manager import add_attendance, view_attendance
from report_generator import generate_report_menu
# import sys


def show_menu():
    print("\nEmployee Attendance Tracker")
    print("1. Add Attendance")
    print("2. View All Records")
    print("3. Generate Report")
    print("4. Exit")


def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            add_attendance()
        elif choice == "2":
            print("This feature is under construction.")
            view_attendance()
        elif choice == "3":
             generate_report_menu()
        elif choice == "4":
            print("Exiting.... Good bye!")
            # sys.exit(0)
            break
        else:
            print("Invalid Input. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
