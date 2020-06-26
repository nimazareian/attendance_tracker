from tkinter import *
import tkinter.font as font
from attendance_record import AttendanceRecord

#constants
attendance_tracker = AttendanceRecord(sheet_name="API Call Test") # file name
screen_width = 800
screen_height = 480
screen_padding = 10
feedback_color = 'yellow'
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

# creating labels
scan_card_label = Label(label_frame, text="SCAN YOUR STUDENT CARD")
scan_card_label.config(font=('Roboto', 32, 'bold'))
# scan_card_label.grid(row=0, column=0)
scan_card_label.place(relx=0.5, rely=0.15, anchor=CENTER)

welcome_student_label = Label(label_frame, text="Welcome, Nima Zareian")
welcome_student_label.config(font=('Roboto', 26))
welcome_student_label.place(relx=0.5, rely=0.4, anchor=CENTER)

student_num_entry = Label(label_frame, text="Student # ") 
student_num_entry.config(font=('Roboto', 22))
student_num_entry.place(relx=0.5, rely=0.55, anchor=CENTER)
# entry
# student_num_entry = Entry(label_frame, width=15, font="Roboto 24")
# student_num_entry.place(relx=0.5, rely=0.55, anchor=CENTER)
# student_num_entry.focus()


# colored feedback
canvas = Canvas(label_frame, width=600, height=150)
canvas.create_rectangle(0, 0, 600, 150, fill=feedback_color, outline="")
canvas.place(relx=0.5, rely=0.82, anchor=CENTER)


def get_student_num(event):
    global student_num  
    global added_record  
    global feedback_color
    
    if event.char in '12345567890' and len(student_num) < 7:                         
        student_num += event.char                                  
        print('>', student_num)                                           
        student_num_entry['text'] += event.char                                   
    elif len(student_num) == 7:                               # why does it have to be 8 digits to work?
        added_record = attendance_tracker.add_record(int(student_num))
        student_num = ''
        student_num_entry['text'] = "Student # "

        if added_record:
            feedback_color = 'green'
        else:
            feedback_color = 'red'

# bind key
root.bind('<Key>', get_student_num)



root.mainloop()
