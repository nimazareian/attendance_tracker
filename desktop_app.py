from tkinter import *
import tkinter.font as font
from attendance_record import AttendanceRecord
import time
from datetime import datetime
import pytz
from enum_status import Status

#constants
attendance_tracker = AttendanceRecord(sheet_name="API Call Test") # file name
screen_width = 800
screen_height = 480
screen_padding = 10
feedback_color = 'white'
student_num = ''
# scan_status = False # to determine the feedback_color

# time
# pst = pytz.timezone('America/Los_Angeles')
# current_time = datetime.now(pst)

# current_day = str(current_time.day) # calendar day
# current_hour = str(current_time.time())  # hour:min:sec

# window
root = Tk()
root.title("Ten Ton Robotics")
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.resizable(False, False)

# adding frame
label_frame = LabelFrame(root, text="Ten Ton Robotics Automated Attendance Tracking System", padx=50, pady=20, height=400, width=700)
label_frame.pack(fill="both", expand="yes")
default_color = label_frame.cget('bg')

# creating labels
scan_card_label = Label(label_frame, text="SCAN YOUR STUDENT CARD")
scan_card_label.config(font=('Roboto', 38, 'bold'))
scan_card_label.place(relx=0.5, rely=0.15, anchor=CENTER)

clock_label = Label(label_frame, text='') 
clock_label.config(font=('Digital-7', 65))
clock_label.place(relx=0.5, rely=0.4, anchor=CENTER)

welcome_student_label = Label(label_frame, text='') #''
welcome_student_label.config(font=('Roboto', 26))
welcome_student_label.place(relx=0.5, rely=0.80, anchor=CENTER)

student_num_entry = Label(label_frame, text='') #Student # 
student_num_entry.config(font=('Roboto', 22))
student_num_entry.place(relx=0.5, rely=0.65, anchor=CENTER)

def tick():
    # get the current local time from the PC
    time_string = time.strftime('%H:%M') #:%S
    # if time string has changed, update it
    clock_label.config(text=time_string)
    clock_label.after(30000, tick) # could be 60000ms

def get_student_num(event):
    global student_num  
    # global scan_status  
    global feedback_color

    if event.char in '12345567890' and len(student_num) < 7:    
        if len(student_num) == 0:
            student_num_entry.config(text='Student # ')                         
        student_num += event.char                                  
        print('>', student_num)                                           
        student_num_entry['text'] += event.char                                   
    elif len(student_num) == 7:                               # why does it have to be 8 digits to work?
        print('this is student num ' + student_num)
        try:
            scan_status = attendance_tracker.add_record(int(student_num))
        except:
            print('Wrong Student #')
            unsuccessful_scan(Status.NOT_FOUND)
            student_num = ''

        student_num_entry['text'] = "Student # "

        if scan_status == Status.LOGGED_IN or scan_status == Status.LOGGED_OUT:
            successful_scan(scan_status, student_num)
        else:
            unsuccessful_scan(scan_status)
                
        student_num = ''

    
def successful_scan(status, student_num_parameter):
    label_frame['bg'] = 'green'
    same_background_color()

    student_info = attendance_tracker.get_student_record(int(student_num_parameter))
    if status == Status.LOGGED_IN:
        welcome_student_label.config(text='Welcome, ' + student_info['Name']) # todo: differentiate msg between signing in and out
        student_num_entry.config(text='Logged in Student # ' + student_num_parameter)
    else:
        welcome_student_label.config(text='Bye ' + student_info['Name']) # todo: differentiate msg between signing in and out
        student_num_entry.config(text='Logged out Student # ' + student_num_parameter)
    
    # global student_num
    # student_num = ''

    label_frame.after(1000, bg_regular_color)


def unsuccessful_scan(status):
    label_frame['bg'] = 'red'
    same_background_color()
    
    if status == Status.ALREADY_LOGGED_OUT:
        welcome_student_label.config(text='Already logged in and out') # todo: differentiate msg between signing in and out
    else:
        welcome_student_label.config(text='User not found') # todo: differentiate msg between signing in and out
    student_num_entry.config(text='')

    # global student_num
    # student_num = ''

    label_frame.after(1000, bg_regular_color)


def bg_regular_color():
    global student_num

    label_frame['bg'] = default_color
    same_background_color()

    student_num_entry.config(text='')
    welcome_student_label.config(text='')

    student_num = ''

def same_background_color():
    scan_card_label['bg'] = label_frame['bg']
    student_num_entry['bg'] = label_frame['bg']
    welcome_student_label['bg'] = label_frame['bg']
    clock_label['bg'] = label_frame['bg']


# bind key - read key's pressed or code scanned
root.bind('<Key>', get_student_num)
tick()


root.mainloop()
