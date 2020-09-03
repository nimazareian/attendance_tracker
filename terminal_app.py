from attendance_record import AttendanceRecord
from colorama import Style

attendance_tracker = AttendanceRecord(sheet_name="API Call Test") # file name
# app running in terminal
while True:
    user_input = input("SCAN YOUR STUDENT CARD: ")
    # filter for only digits from input
    student_num = ''.join(c for c in user_input if c.isdigit())
    
    attendance_tracker.add_record(int(student_num))
    Style.RESET_ALL
    print("\n______________________________________")