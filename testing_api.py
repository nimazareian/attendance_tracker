from attendance_record import AttendanceRecord

spreadsheet_file_name = "2020-2021 Attendance Tracker"
attendance_tracker = AttendanceRecord(spreadsheet_name=spreadsheet_file_name)

# spreadsheet = attendance_tracker.__get_spreadsheet()
attendance_tracker.add_record(1)