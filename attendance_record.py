import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pytz
from enum_status import Status

from colorama import Fore, Back, Style, init
init(autoreset=True)

# Constants
returned_sheet = None
matched_student = None

# log time in google sheet
class AttendanceRecord:
    # class constructor
    def __init__(self, sheet_name):
        self.sheet_name = sheet_name

    # API set up - Getting entire sheet
    def get_google_sheet(self):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        g_sheet = client.open(self.sheet_name)  # Get Spreadsheet based on name "API Call Test"
        return g_sheet

    # get all sheet filled cells
    def get_all_sheet_record(self):
        global returned_sheet
        return returned_sheet.sheet1.get_all_records()

    # look for User Row based on ID in list of dicts
    def get_student_record(self, student_num): 
        global matched_student
        student_record = self.get_all_sheet_record()
        matched_student = next((student for student in student_record if student['ID'] == student_num), 'User not Found')
        return matched_student

    # what row is student's data in, in the GSheet
    def get_student_row_num(self, student_num):
        sheet_data = self.get_all_sheet_record()
        index = next((i for i, item in enumerate(sheet_data) if item["ID"] == student_num), 'Student Num not found')
        row_num = index + 2  # Adding 2 since it doesnt take into account first row and index starts at 0
        return row_num

    # add current time to google sheet for student with student_num
    def add_record(self, student_num):
        global returned_sheet
        returned_sheet = self.get_google_sheet()

        sheet = returned_sheet.sheet1 # todo: refactor sheet1 so you can select between different sheets
        matched_id = self.get_student_record(student_num)
        row_num = self.get_student_row_num(student_num)
        
        # get current date
        pst = pytz.timezone('America/Los_Angeles')
        current_time = datetime.now(pst)
        current_day = str(current_time.day) # calendar day
        current_hour = str(current_time.time())  # hour:min:sec

        # check if has already tapped in
        col_in_name = current_day + ' IN'
        col_out_name = current_day + ' OUT'
        already_tapped_in = matched_id[col_in_name] != ''
        already_tapped_out = matched_id[col_out_name] != ''

        # add tapped time
        if not already_tapped_in and not already_tapped_out:
            col_num = sheet.find(col_in_name).col
            sheet.update_cell(row_num, col_num, current_hour)
            
            print(Back.GREEN + Style.BRIGHT + 'TIMED IN ' + matched_student['Name'])
            return Status.LOGGED_IN

        elif already_tapped_in and not already_tapped_out:
            col_num = sheet.find(col_out_name).col
            sheet.update_cell(row_num, col_num, current_hour)
            print(Back.GREEN + Style.BRIGHT + 'TIMED OUT ' + matched_student['Name'])
            return Status.LOGGED_OUT

        else:
            print(Back.RED + Style.BRIGHT + "COULDN'T TIME IN/OUT " + matched_student['Name'] + " - Have you already timed in and out for today?")   
            return Status.ALREADY_LOGGED_OUT



    # Add Sheet todo steps:
    #   - create a new sheet within the Google Sheet document
    #       - Name it what the month is
    #   - Take all of the names and student numbers from the main sheet and add them to the first 2 columns
    #   - Add titles for Name, Student ID, and dates of the month in/out
    #
    # Future Steps:
    #   - Add formulas to the cells to calculate the time spent for each day 
    #   - Display the time spent in a new column 