from attendance_record import AttendanceRecord

attendance_tracker = AttendanceRecord(sheet_name="API Call Test") # file name

# spreadsheet = attendance_tracker.__get_spreadsheet()
attendance_tracker.add_record(1)