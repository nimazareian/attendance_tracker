from attendance_record import AttendanceRecord

spreadsheet_key = "1LbaJW7H0jgQkCwZh3iQKG0xEEa54a5KUYbm_cikwMtQ"
attendance_tracker = AttendanceRecord(spreadsheet_key=spreadsheet_key)

# spreadsheet = attendance_tracker.__get_spreadsheet()
attendance_tracker.add_record(1)