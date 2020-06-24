import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pytz

# API set up - Getting entire sheet
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("API Call Test").sheet1  # Open the spreadhseet

# get data
data = sheet.get_all_records()  # Get a list of all records
# print(data)

# scanned student #
studentNum = int(input("Enter your student #: "))

# look for User Row based on ID in list of dicts todo: if user is not found throw exception or write error so next
#  steps don't run
matchedID = next((person for person in data if person['ID'] == studentNum), 'User not Found')
print(matchedID)

# index of item
index = next((i for i, item in enumerate(data) if item["ID"] == studentNum), 'Student Num not found')
rowNum = index + 2  # Adding 2 since it doesnt take into account first row and index starts at 0

# get current date
pst = pytz.timezone('America/Los_Angeles')
currentTime = datetime.now(pst)

currentDay = str(currentTime.day) # calendar day
currentHour = str(currentTime.time())  # hour:min:sec

# check if has already tapped in
colInName = currentDay + ' IN'
colOutName = currentDay + ' OUT'
alreadyTappedIn = matchedID[colInName] != ''
alreadyTappedOut = matchedID[colOutName] != ''
print(alreadyTappedOut)

# add tapped time
if not alreadyTappedIn and not alreadyTappedOut:
    sheet.update_cell(rowNum, 3, currentHour) # todo: find a better way to determine what col to update. eg. use date?
    print('timed in')
elif alreadyTappedIn and not alreadyTappedOut:
    sheet.update_cell(rowNum, 4, currentHour)
    print('timed out')
else:
    print("couldn't time in/out - Have you already timed in and out for today?")