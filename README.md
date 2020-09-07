# Automated Attendance Tracking System

We are using a Raspberry Pi 4 alongside with a barcode scanner to scan after school students' student card to sign them in and out. After each scan, a Google Sheets document is updated with the time in/out added for each student. This way multiple attendance trackers can be running simultaneously and they will all update the same database. The classroom teachers will also be easily able to check and update the stored information remotely.

At the start of a month, the application will automatically add a new custom sheet for that month to the main Spreadsheet document to keep the logs organized and easily trackable.

## Goal
The goal of this project is to automate student logging in and out of classroom, so the amount of time they spent in the shop is tracked which can be evaluated for their grade and to be able to predict the amount of time required to finish a project. This project can also be used at a workplace to track employees time.

## Run The App
#### Setup Google Drive API
Setting up Google Drive's API is difficult to explain here, so here is a video tutorial explaining it instead (The first 1:35 walks you through the required steps)!
https://www.youtube.com/watch?v=vISRn5qFrkM

#### Setup App
To run this app:
1. Make sure have Python 3 installed on your system. Check by running the following in CMD:
```
python --version
```
2. Clone or download this repository
3. Install the required packages.
```
pip install gspread oauth2client pytz
```
4. Finally run the app:

GUI:
```
python desktop_app.py
```
or in terminal
```
python terminal_app.py
```

## Hardware Used
This project can be **%100 free**, however if you are looking for logging system running at all times the following Hardware is **recommended**.

- Raspberry Pi 4 (CA$ 47.45+)
- 32GB SD Card (CA$ 21.99)
- Raspberry Pi power supply (CA$ 10.95)
- Barcode Scanner (CA$ 35.99)
- Mini display for Pi to confirm student signing in/out (optional)
- Micro HDMI to HDMI cable (optional)

A Basic setup to run this system can be purchased online for *~CA $116.38* before tax.

## Benefits of This Setup
- The Raspberry Pi allows for a small and inexpensive set up so multiple rooms can be running this system at the same time.
- The barcode scanner allows for almost instant card scanning of students card for logging, while also allowing for a contactless user interaction which is very important for students safety, specially during the COVID-19 outbreak (**Note** not all barcode scanners have touchless setting! We used *Symcode Embedded Mini USB Fixed Mount Barcode Scanner* which has automatic turn on when something is hover infront of it).  
- The mini LCD display allows for feedback to the students so they can assure that they were tapped in/out or are told if there was a problem in the process.

## App GUI
Some pictures of the different pages of the GUI application. The GUI is kept simple with large text so it can be shown on a small LCD screen.

#### Main Screen
<img src="https://github.com/nimazareian/attendance_tracker/blob/master/demo_pictures/demo_main_screen.png" width="400" title="Main Screen">

#### Log in/out Screen
<img src="https://github.com/nimazareian/attendance_tracker/blob/master/demo_pictures/demo_logged_in_screen.png" width="400" title="Logged in Screen">

#### User Not Found Error Screen
<img src="https://github.com/nimazareian/attendance_tracker/blob/master/demo_pictures/demo_user_not_found_screen.png" width="400" title="Error Screen">
