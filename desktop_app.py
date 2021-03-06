from tkinter import *
import tkinter.font as font
from attendance_record import AttendanceRecord
import time
from datetime import datetime
import pytz
from enum_status import Status

#constants
spreadsheet_key = "1LbaJW7H0jgQkCwZh3iQKG0xEEa54a5KUYbm_cikwMtQ"
attendance_tracker = AttendanceRecord(spreadsheet_key=spreadsheet_key)
screen_width = 800 # max screen size for desired Raspberry Pi screen
screen_height = 480
screen_padding = 10
feedback_color = 'white'
student_num = ''

# window
root = Tk()
root.title("Ten Ton Robotics")
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.attributes('-fullscreen', True)
root.resizable(False, False)
root.iconphoto(False, PhotoImage(file='./icon.png'))

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

# displays time on screen
def tick():
    # get the current local time from the PC 
    time_string = time.strftime('%H:%M') #:%S
    # if time string has changed, update it
    clock_label.config(text=time_string)
    clock_label.after(30000, tick) # could be 60000ms

# gets student num and logs it in the main Google Sheet
def get_student_num(event):
    global student_num  
    global feedback_color

    if event.char in '12345567890' and len(student_num) < 7:    
        if len(student_num) == 0:
            student_num_entry.config(text='Student # ')                         
        student_num += event.char                                  
        print('>', student_num)                                           
        student_num_entry['text'] += event.char                                   
    elif event.keysym == 'Return': # If enter pressed, add record
        print('Attempting to add record for student #' + student_num)
        try:
            scan_status = attendance_tracker.add_record(int(student_num))
        except Exception as e:
            print('Wrong Student #')
            print(e)
            scan_status = Status.NOT_FOUND
            student_num = ''

        student_num_entry['text'] = "Student # "

        if scan_status == Status.LOGGED_IN or scan_status == Status.LOGGED_OUT:
            successful_scan(scan_status, student_num)
        else:
            unsuccessful_scan(scan_status)

        # reset student num after scan        
        student_num = ''

# flashes green and writes a message to user
def successful_scan(status, student_num_parameter):
    label_frame['bg'] = 'green'
    same_background_color()

    # student_info = attendance_tracker.get_student_record(int(student_num_parameter))#########################################################
    if status == Status.LOGGED_IN:
        # welcome_student_label.config(text='Welcome, ' + student_info['Name']) #########################################################
        student_num_entry.config(text='Logged in Student # ' + student_num_parameter)
    else:
        # welcome_student_label.config(text='Bye ' + student_info['Name'])#########################################################
        student_num_entry.config(text='Logged out Student # ' + student_num_parameter)
    
    # after 1000 ms resets background  
    label_frame.after(1500, bg_regular_color)

# flashes red and writes a msg to user
def unsuccessful_scan(status):
    label_frame['bg'] = 'red'
    same_background_color()
    
    if status == Status.ALREADY_LOGGED_OUT:
        welcome_student_label.config(text='Already logged in and out for today')
    else:
        welcome_student_label.config(text='User not found')
    student_num_entry.config(text='')

    # after 1000 ms resets background  
    label_frame.after(1500, bg_regular_color)

# reset background and texts
def bg_regular_color():
    global student_num

    label_frame['bg'] = default_color
    same_background_color()

    student_num_entry.config(text='')
    welcome_student_label.config(text='')

    student_num = ''

# makes the text backgrounds the same color as the background of window
def same_background_color():
    frame_bg = label_frame['bg']
    scan_card_label['bg'] = frame_bg
    student_num_entry['bg'] = frame_bg
    welcome_student_label['bg'] = frame_bg
    clock_label['bg'] = frame_bg


# bind key - read key's pressed or code scanned
root.bind('<Key>', get_student_num)
tick()
 

root.mainloop()