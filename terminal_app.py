from attendance_record import AttendanceRecord
from colorama import Style

spreadsheet_key = "1LbaJW7H0jgQkCwZh3iQKG0xEEa54a5KUYbm_cikwMtQ"
attendance_tracker = AttendanceRecord(spreadsheet_key=spreadsheet_key)

# app running in terminal
while True:
    user_input = input("SCAN YOUR STUDENT CARD: ")
    # filter for only digits from input
    student_num = ''.join(c for c in user_input if c.isdigit())
    
    attendance_tracker.add_record(int(student_num))
    Style.RESET_ALL
    print("\n______________________________________")