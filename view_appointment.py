import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
from PIL import Image, ImageTk
import pymysql
from datetime import datetime, timedelta
from tkinter import ttk

class ViewAppointment:
    def __init__(self):
        self.view_window = tk.Tk()
        self.view_window.resizable(False, False)
        self.view_window.title('View Appointment')

        # Load the background image
        bg_image = Image.open('background.jpg')
        self.bgImage = ImageTk.PhotoImage(bg_image)

        # Get the dimensions of the original image
        width, height = bg_image.size

        # Create a label for the background image
        self.bgLabel = Label(self.view_window, image=self.bgImage)
        self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Set the size of the home window to match the size of the background image
        self.view_window.geometry(f"{width}x{height}")
        
        # Create an outer frame to center the inner frame
        self.outer_frame = Frame(self.view_window, bg='white')
        self.outer_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.frame = Frame(self.outer_frame, width=870, height=600, bg='white')
        self.frame.grid(row=0, column=0, padx=20, pady=10)

        # Header
        self.headingLabel = Label(self.frame, text='View Appointment', font=('Times New Roman', 23), bg='white', fg='black')
        self.headingLabel.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

        # Date Label and Calendar Button
        self.dateLabel = Label(self.frame, text="Choose Date:", font=('Times New Roman', 15), bg='white')
        self.dateLabel.grid(row=1, column=0, pady=10, sticky='e')
        self.dateButton = Button(self.frame, text="Select Date", font=('Times New Roman', 15), command=self.open_calendar)
        self.dateButton.grid(row=1, column=1, pady=10, sticky='w')

        # Display the selected date
        self.selected_date = StringVar()
        self.selected_date_label = Label(self.frame, textvariable=self.selected_date, font=('Times New Roman', 15), bg='white')
        self.selected_date_label.grid(row=1, column=1, padx=(150, 0), pady=10, sticky='w')

        # Filter options for appointments
        self.filter_var = StringVar(value="today")
        self.filter_frame = Frame(self.frame, bg='white')
        self.filter_frame.grid(row=2, column=0, columnspan=2, pady=10)
        self.today_radio = Radiobutton(self.filter_frame, text="Appointments for Today", variable=self.filter_var, value="today", bg='white', font=('Times New Roman', 15))
        self.today_radio.pack(side=LEFT, padx=10)
        self.upcoming_radio = Radiobutton(self.filter_frame, text="Upcoming Appointments", variable=self.filter_var, value="upcoming", bg='white', font=('Times New Roman', 15))
        self.upcoming_radio.pack(side=LEFT, padx=10)
        self.past_radio = Radiobutton(self.filter_frame, text="Past Appointments", variable=self.filter_var, value="past", bg='white', font=('Times New Roman', 15))
        self.past_radio.pack(side=LEFT, padx=10)

        # Filter options for appointment status
        self.status_var = StringVar(value="none")
        self.status_frame = Frame(self.frame, bg='white')
        self.status_frame.grid(row=3, column=0, columnspan=2, pady=10)
        self.all_status_radio = Radiobutton(self.status_frame, text="All Status", variable=self.status_var, value="none", bg='white', font=('Times New Roman', 15))
        self.all_status_radio.pack(side=LEFT, padx=10)
        self.reserved_radio = Radiobutton(self.status_frame, text="Reserved", variable=self.status_var, value="reserved", bg='white', font=('Times New Roman', 15))
        self.reserved_radio.pack(side=LEFT, padx=10)
        self.cancelled_radio = Radiobutton(self.status_frame, text="Cancelled", variable=self.status_var, value="cancelled", bg='white', font=('Times New Roman', 15))
        self.cancelled_radio.pack(side=LEFT, padx=10)

        # Initialize the table
        self.init_table()

        # View Button
        self.viewButton = Button(self.frame, text="View Appointments", font=('Segoe UI Black', 15),bd=0, bg='#d6d4d4', command=self.view_appointments)
        self.viewButton.grid(row=4, column=0, columnspan=1)

        self.backbutt = Button(self.frame, width=10,text='Back', font=('Segoe UI Black', 15),bd=0, bg='#d6d4d4', command=self.home_page)
        self.backbutt.grid(row=4, column=1,columnspan=2)

        self.view_window.mainloop()
    
    def home_page(self):
        self.view_window.destroy()
        from home import Home
        Home()

    def open_calendar(self):
        top = Toplevel(self.view_window)
        top.title("Select Date")
        calendar = Calendar(top, date_pattern='y-mm-dd', mindate=datetime(2024,1,1))
        calendar.pack(pady=10)

        def select_date():
            self.selected_date.set(calendar.get_date())
            top.destroy()

        select_button = Button(top, text="Select", command=select_date)
        select_button.pack(pady=10)

    def view_appointments(self):
        appointment_date = self.selected_date.get()
        filter_option = self.filter_var.get()
        status_option = self.status_var.get()
        current_date = datetime.now().date()

        try:
            con = pymysql.connect(host='localhost', user='root', password='', db='user')
            mycursor = con.cursor()

            if filter_option == "today":
                if status_option == "none":
                    query = """
                    SELECT member.name, appointments.ic_number, appointments.date, appointments.time, appointments.service, appointments.dentist, appointments.status 
                    FROM appointments 
                    JOIN member ON appointments.ic_number = member.ic_number 
                    WHERE appointments.date = %s
                    """
                    mycursor.execute(query, (current_date,))
                else:
                    query = """
                    SELECT member.name, appointments.ic_number, appointments.date, appointments.time, appointments.service, appointments.dentist, appointments.status 
                    FROM appointments 
                    JOIN member ON appointments.ic_number = member.ic_number 
                    WHERE appointments.date = %s AND appointments.status = %s
                    """
                    mycursor.execute(query, (current_date, status_option))
            elif filter_option == "upcoming":
                if status_option == "none":
                    query = """
                    SELECT member.name, appointments.ic_number, appointments.date, appointments.time, appointments.service, appointments.dentist, appointments.status 
                    FROM appointments 
                    JOIN member ON appointments.ic_number = member.ic_number 
                    WHERE appointments.date >= %s
                    """
                    mycursor.execute(query, (current_date,))
                else:
                    query = """
                    SELECT member.name, appointments.ic_number, appointments.date, appointments.time, appointments.service, appointments.dentist, appointments.status 
                    FROM appointments 
                    JOIN member ON appointments.ic_number = member.ic_number 
                    WHERE appointments.date >= %s AND appointments.status = %s
                    """
                    mycursor.execute(query, (current_date, status_option))
            else:  # past
                if status_option == "none":
                    query = """
                    SELECT member.name, appointments.ic_number, appointments.date, appointments.time, appointments.service, appointments.dentist, appointments.status 
                    FROM appointments 
                    JOIN member ON appointments.ic_number = member.ic_number 
                    WHERE appointments.date < %s
                    """
                    mycursor.execute(query, (current_date,))
                else:
                    query = """
                    SELECT member.name, appointments.ic_number, appointments.date, appointments.time, appointments.service, appointments.dentist, appointments.status 
                    FROM appointments 
                    JOIN member ON appointments.ic_number = member.ic_number 
                    WHERE appointments.date < %s AND appointments.status = %s
                    """
                    mycursor.execute(query, (current_date, status_option))

            results = mycursor.fetchall()
            con.close()

            self.display_appointments(results)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def init_table(self):
        # Initialize treeview
        self.tree = ttk.Treeview(self.frame, columns=("Name", "IC Number", "Date", "Time", "Service", "Dentist", "Status"), show="headings")
        self.tree.grid(row=5, column=0, columnspan=2, pady=10)

        # Configure column headings
        self.tree.heading("Name", text="Name")
        self.tree.heading("IC Number", text="IC Number")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Service", text="Service")
        self.tree.heading("Dentist", text="Dentist")
        self.tree.heading("Status", text="Status")

        # Set column widths
        self.tree.column("Name", width=150)
        self.tree.column("IC Number", width=100)
        self.tree.column("Date", width=100)
        self.tree.column("Time", width=100)
        self.tree.column("Service", width=100)
        self.tree.column("Dentist", width=100)
        self.tree.column("Status", width=100)

    def display_appointments(self, results):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Populate table with new data
        if results:
            for row in results:
                self.tree.insert("", "end", values=row)
ViewAppointment()
