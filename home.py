import tkinter as tk
from tkinter import *
from tkinter import Frame
from tkinter import Label
from tkinter import Button
from tkinter import messagebox
from PIL import Image, ImageTk

class Home:
    def __init__(self):
        self.home_window = tk.Tk()
        self.home_window.resizable(False, False)
        self.home_window.title('Home Page')

        # Load the background image
        bg_image = Image.open('background.jpg')
        self.bgImage = ImageTk.PhotoImage(bg_image)

        # Get the dimensions of the original image
        width, height = bg_image.size

        # Create a label for the background image
        self.bgLabel = tk.Label(self.home_window, image=self.bgImage)
        self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Set the size of the home window to match the size of the background image
        self.home_window.geometry(f"{width}x{height}")
        
        self.frame = Frame(self.home_window, width=870, height=500, bg='white')
        self.frame.place(x=80, y=180)

        # Configure grid layout with two rows and three columns
        for i in range(3):
            self.frame.columnconfigure(i, weight=1)
        for j in range(2):
            self.frame.rowconfigure(j, weight=1)

        # Create and place labels in the grid for structure
        for row in range(2):
            for col in range(3):
                label = Label(self.frame, text=f"Row {row+1}, Col {col+1}", bg='white', width=38, height=15)
                label.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Create and place buttons in the grid
        self.NewMember = Button(self.frame, text="Add New Member",font=('Segoe UI Black', 10), bg='#d6d4d4', command=self.register)
        self.NewMember.grid(row=0, column=0, sticky="nsew")

        self.MakeAppointment = Button(self.frame, text="Make Appointment",font=('Segoe UI Black', 10), bg='#d6d4d4', command=self.booking)
        self.MakeAppointment.grid(row=0, column=1, sticky="nsew")

        self.CancelAppointment = Button(self.frame, text="Cancel Appointment",font=('Segoe UI Black', 10), bg='#d6d4d4',command=self.cancel)
        self.CancelAppointment.grid(row=0, column=2, sticky="nsew")

        self.View = Button(self.frame, text="View Appointments and Members Records",font=('Segoe UI Black', 10), bg='#d6d4d4',command=self.view)
        self.View.grid(row=1, column=0, sticky="nsew")

        self.SearchAndEdit = Button(self.frame, text="Search and Edit Patient records",font=('Segoe UI Black', 10),bg='#d6d4d4',command=self.search)
        self.SearchAndEdit.grid(row=1, column=1, sticky="nsew")

        self.Feedback = Button(self.frame, text="Feedbacks & Comments",font=('Segoe UI Black', 10), bg='#d6d4d4', command=self.feedback)
        self.Feedback.grid(row=1, column=2, sticky="nsew")

        self.Logout=Button(self.home_window,text="Logout",width=10,height=2,font=('Segoe UI Black', 10), bg='#d6d4d4',command=self.logout)
        self.Logout.grid(row=3,column=5, padx=880,pady=50)

        self.home_window.mainloop()

    def register(self):
        self.home_window.destroy()
        from register_member import RegisterMember 
        RegisterMember()
    
    def booking(self):
        self.home_window.destroy()
        from book_appointment import BookAppointment
        BookAppointment() 

    def cancel(self):
        self.home_window.destroy()
        from cancel_appointment import CancelAppointment
        CancelAppointment() 

    def view(self):
        self.home_window.destroy()
        from view_appointment import ViewAppointment 
        ViewAppointment()

    def search(self):
        self.home_window.destroy()
        from search_edit import Edit
        Edit() 

    def feedback(self):
        self.home_window.destroy()
        from feedback import FeedbackMember
        FeedbackMember()

    def logout(self):
        # Ask for confirmation before logout
        confirm = messagebox.askquestion("Logout", "Are you sure you want to logout?", icon='warning')
        
        if confirm == 'yes':
            # Destroy the current window and open the login window
            self.home_window.destroy()
            from Main import Main
            Main()

Home()
