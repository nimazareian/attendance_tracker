from attendance_record import AttendanceRecord

attendance_tracker = AttendanceRecord("API Call Test") # change file

while True:
    student_num = int(input("Enter your student #: "))

    attendance_tracker.add_record(student_num)