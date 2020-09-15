import gspread
from oauth2client.service_account import ServiceAccountCredentials
from enum_status import Status
from util import *

from colorama import Fore, Back, Style, init
init(autoreset=True)

# Global Variables
template_worksheet_name = 'Template - DO NOT TOUCH'
spreadsheet = None
worksheet = None
matched_student = None
current_time = None

# log time in google sheet
# Google GSpread API Examples: https://developers.google.com/sheets/api/reference/rest
# Detailed GSpread Documentation: https://gspread.readthedocs.io/en/latest/index.html
# NOTE: spreadsheet is the name of the entire document. 
#       worksheet refers to 1 sheet within spreadsheet 
class AttendanceRecord:
    # class constructor
    def __init__(self, spreadsheet_key):
        self.spreadsheet_key = spreadsheet_key

    # API set up - Getting entire sheet
    def __get_spreadsheet(self):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(self.spreadsheet_key)  # Get Spreadsheet based on name "API Call Test"
        return spreadsheet

    # get worksheet with the same name as current month
    def get_worksheet(self):
        global spreadsheet
        global worksheet

        spreadsheet = self.__get_spreadsheet()
        current_month = get_current_month()

        for worksheet in spreadsheet.worksheets():
            if (worksheet.title == current_month):
                worksheet = spreadsheet.worksheet(current_month)
                return worksheet

        worksheet = self.add_new_month_sheet()
        return worksheet

    # At the start of the month, duplicates the Template sheet with the new month as the name
    def add_new_month_sheet(self):
        global spreadsheet
        current_month = get_current_month()
        new_sheet = spreadsheet.worksheet(template_worksheet_name).duplicate(insert_sheet_index=1 , new_sheet_name=current_month)
        return new_sheet

    # get all sheet filled cells
    def get_all_sheet_records(self):
        global worksheet
        return worksheet.get_all_records()

    # look for User Row based on Student # in list of dicts
    # retuns dictionary of student hours
    def get_student_record(self, student_num): 
        global matched_student
        student_records = self.get_all_sheet_records()
        matched_student = next((student for student in student_records if student['ID'] == student_num), 'User not Found')
        return matched_student

    # what row is student's data in, in the GSheet
    def get_student_row_num(self, student_num):
        sheet_data = self.get_all_sheet_records()
        index = next((i for i, item in enumerate(sheet_data) if item['ID'] == student_num), 'Student Num not found')
        row_num = index + 2  # Adding 2 since it doesnt take into account first row and index starts at 0
        return row_num

    # add current time to google sheet for student with student_num
    def add_record(self, student_num):
        global matched_student

        worksheet = self.get_worksheet()
        matched_id = self.get_student_record(student_num)
        row_num = self.get_student_row_num(student_num)
        
        # get current date
        current_day = get_current_day()
        current_hour = get_current_hour()

        # check if has already tapped in
        col_in_name = current_day + ' IN'
        col_out_name = current_day + ' OUT'
        already_tapped_in = matched_id[col_in_name] != ''
        already_tapped_out = matched_id[col_out_name] != ''

        # add tapped time
        if not already_tapped_in and not already_tapped_out:
            col_num = worksheet.find(col_in_name).col
            worksheet.update_cell(row_num, col_num, current_hour)
            
            print(Back.GREEN + Style.BRIGHT + 'TIMED IN ')# + matched_student['Name'])
            return Status.LOGGED_IN

        elif already_tapped_in and not already_tapped_out:
            col_num = worksheet.find(col_out_name).col
            worksheet.update_cell(row_num, col_num, current_hour)
            print(Back.GREEN + Style.BRIGHT + 'TIMED OUT ')# + matched_student['Name'])
            return Status.LOGGED_OUT

        else:
            print(Back.RED + Style.BRIGHT + "COULDN'T TIME IN/OUT ")# + matched_student['Name'] + " - Have you already timed in and out for today?")   
            return Status.ALREADY_LOGGED_OUT



    # Add Sheet todo steps:
    #   - Take all of the names and student numbers from the main sheet and add them to the first 2 columns
    #   - Add titles for Name, Student ID, and dates of the month in/out
    #
    # Future Steps:
    #   - Add formulas to the cells to calculate the time spent for each day 
    #   - Display the time spent in a new column 