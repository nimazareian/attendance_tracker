import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pytz

class AttendanceRecord:

    def __init__(self, sheet_name):
        self.sheet_name = sheet_name

    # API set up - Getting entire sheet
    def get_google_sheet(self):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        GSheet = client.open(self.sheet_name)  # Get Spreadsheet based on name "API Call Test"
        return GSheet

    def get_all_sheet_record(self):
        sheet = self.get_google_sheet()
        return sheet.sheet1.get_all_records()


    # look for User Row based on ID in list of dicts
    def get_student_record(self, student_num): 
        student_record = self.get_all_sheet_record()
        matched_student = next((student for student in student_record if student['ID'] == student_num), 'User not Found')
        return matched_student

    # what row is student's data in, in the GSheet
    def get_student_row_num(self, student_num):
        sheet_data = self.get_all_sheet_record()
        index = next((i for i, item in enumerate(sheet_data) if item["ID"] == student_num), 'Student Num not found')
        row_num = index + 2  # Adding 2 since it doesnt take into account first row and index starts at 0
        return row_num

    def add_record(self, student_num):
        sheet = self.get_google_sheet().sheet1 # todo: refactor sheet1 so you can select between different sheets
        matched_id = self.get_student_record(student_num)
        row_num = self.get_student_row_num(student_num)

        # get current date
        pst = pytz.timezone('America/Los_Angeles')
        currentTime = datetime.now(pst)

        currentDay = str(currentTime.day) # calendar day
        currentHour = str(currentTime.time())  # hour:min:sec

        # check if has already tapped in
        colInName = currentDay + ' IN'
        colOutName = currentDay + ' OUT'
        alreadyTappedIn = matched_id[colInName] != ''
        alreadyTappedOut = matched_id[colOutName] != ''

        # add tapped time
        if not alreadyTappedIn and not alreadyTappedOut:
            colNum = sheet.find(colInName).col
            sheet.update_cell(row_num, colNum, currentHour)
            print('timed in')
        elif alreadyTappedIn and not alreadyTappedOut:
            colNum = sheet.find(colOutName).col
            sheet.update_cell(row_num, colNum, currentHour)
            print('timed out')
        else:
            print("couldn't time in/out - Have you already timed in and out for today?")


    # Add Sheet todo steps:
    #   - create a new sheet within the Google Sheet document
    #       - Name it what the month is
    #   - Take all of the names and student numbers from the main sheet and add them to the first 2 columns
    #   - Add titles for Name, Student ID, and dates of the month in/out
    #
    # Future Steps:
    #   - Add formulas to the cells to calculate the time spent for each day 
    #   - Display the time spent in a new column 

    # todo:
    #   - if user is not found throw exception or write error so next steps don't run