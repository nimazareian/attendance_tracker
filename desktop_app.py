from tkinter import *
import tkinter.font as font
from attendance_record import AttendanceRecord
import time

#constants
attendance_tracker = AttendanceRecord(sheet_name="API Call Test") # file name
screen_width = 800
screen_height = 480
screen_padding = 10
feedback_color = 'white'
student_num = ''
added_record = False # to determine the feedback_color

# fonts

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
scan_card_label.config(font=('Roboto', 32, 'bold'))
scan_card_label.place(relx=0.5, rely=0.15, anchor=CENTER)

welcome_student_label = Label(label_frame, text="Welcome, ")
welcome_student_label.config(font=('Roboto', 26))
welcome_student_label.place(relx=0.5, rely=0.4, anchor=CENTER)

student_num_entry = Label(label_frame, text="Student # ") 
student_num_entry.config(font=('Roboto', 22))
student_num_entry.place(relx=0.5, rely=0.55, anchor=CENTER)

def get_student_num(event):
    global student_num  
    global added_record  
    global feedback_color

    if event.char in '12345567890' and len(student_num) < 7:    
        if len(student_num) == 0:
            student_num_entry.config(text='Student # ')                         
        student_num += event.char                                  
        print('>', student_num)                                           
        student_num_entry['text'] += event.char                                   
    elif len(student_num) == 7:                               # why does it have to be 8 digits to work?
        print('this is student num ' + student_num)
        added_record = attendance_tracker.add_record(int(student_num))
        student_num_entry['text'] = "Student # "

        if added_record:
            # student_info = attendance_tracker.get_student_record(int(student_num))
            time_added(student_num)
        else:
            flash_red()
                
        student_num = ''

    
def time_added(student_num):
    label_frame['bg'] = 'green'
    same_background_color()

    student_info = attendance_tracker.get_student_record(int(student_num))
    welcome_student_label.config(text='Welcome, ' + student_info['Name']) # todo: differentiate msg between signing in and out
    student_num_entry.config(text='Student # ' + student_num)

    label_frame.after(3000, bg_regular_color)

def flash_red():
    label_frame['bg'] = 'red'
    same_background_color()
    student_num_entry.config(text='')
    welcome_student_label.config(text='')
    label_frame.after(3000, bg_regular_color)

def bg_regular_color():
    label_frame['bg'] = default_color
    same_background_color()
    student_num_entry.config(text='')
    welcome_student_label.config(text='')

def same_background_color():
    scan_card_label['bg'] = label_frame['bg']
    student_num_entry['bg'] = label_frame['bg']
    welcome_student_label['bg'] = label_frame['bg']

# bind key - read key's pressed or code scanned
root.bind('<Key>', get_student_num)

# todo: if wrong code is entered the code crashes?
# todo: instead of adding timer to individual elements, change the entire screen for few seconds

root.mainloop()
