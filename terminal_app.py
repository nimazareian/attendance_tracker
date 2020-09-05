from attendance_record import AttendanceRecord
from colorama import Style

spreadsheet_file_name = "2020-2021 Attendance Tracker"
attendance_tracker = AttendanceRecord(spreadsheet_name=spreadsheet_file_name)

# app running in terminal
while True:
    user_input = input("SCAN YOUR STUDENT CARD: ")
    # filter for only digits from input
    student_num = ''.join(c for c in user_input if c.isdigit())
    
    attendance_tracker.add_record(int(student_num))
    Style.RESET_ALL
    print("\n______________________________________")