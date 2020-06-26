from tkinter import *
import tkinter.font as font

#constants
screen_width = 800
screen_height = 480
screen_padding = 10
feedback_color = 'yellow'

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

# entry
student_num_entry = Entry(label_frame, width=15, font="Roboto 24")
# student_num_entry.grid(row=2, column=0)
student_num_entry.place(relx=0.5, rely=0.55, anchor=CENTER)
student_num_entry.focus()
student_num_entered = student_num_entry.get()
print(student_num_entered)

# colored feedback
canvas = Canvas(label_frame, width=600, height=150)
canvas.create_rectangle(0, 0, 600, 150, fill=feedback_color, outline="")
canvas.place(relx=0.5, rely=0.82, anchor=CENTER)


root.mainloop()