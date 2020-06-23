import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import json

# set up
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("API Call Test").sheet1  # Open the spreadhseet

# get data
data = sheet.get_all_records()  # Get a list of all records
print(data)

# print ID of second user
print(data[1]['ID'])

# look for User based on name in list of dicts
matchedName = list(filter(lambda person: person['Name'] == 'Nima Zareian', data))
print(matchedName)

# look for User based on ID in list of dicts
matchedID = next((person for person in data if person['ID'] == 1280761), 'User not Found')
print(matchedID)


# Extra data from sheets
# row = sheet.row_values(2)  # Get a specific row
# col = sheet.col_values(3)  # Get a specific column
# cell = sheet.cell(1,2).value  # Get the value of a specific cell
#
# insertRow = ["hello", 5, "red", "blue"]
# sheet.add_rows(insertRow, 4)  # Insert the list as a row at index 4
#
# sheet.update_cell(2,2, "CHANGED")  # Update one cell
#
# numRows = sheet.row_count  # Get the number of rows in the sheet