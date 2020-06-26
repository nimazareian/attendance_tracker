from attendance_record import AttendanceRecord

attendance_tracker = AttendanceRecord(sheet_name="API Call Test") # file name

while True:
    student_num = int(input("Enter your student #: "))

    attendance_tracker.add_record(student_num)