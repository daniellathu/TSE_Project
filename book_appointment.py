import tkinter as tk
from tkinter import *
from tkcalendar import Calendar
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk
import pymysql
from datetime import datetime, time, timedelta

class BookAppointment:
    def __init__(self):
        self.booking_window = tk.Tk()
        self.booking_window.resizable(False, False)
        self.booking_window.title('Book Appointment')

        # Load the background image
        bg_image = Image.open('background.jpg')
        self.bgImage = ImageTk.PhotoImage(bg_image)

        # Get the dimensions of the original image
        width, height = bg_image.size

        # Create a label for the background image
        self.bgLabel = Label(self.booking_window, image=self.bgImage)
        self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Set the size of the home window to match the size of the background image
        self.booking_window.geometry(f"{width}x{height}")

        # Create an outer frame to center the inner frame
        self.outer_frame = Frame(self.booking_window, bg='white')
        self.outer_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.frame = Frame(self.outer_frame, width=870, height=600, bg='white')
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        # Header
        self.headingLabel = Label(self.frame, text='Book Appointment', font=('Times New Roman', 23), bg='white', fg='black')
        self.headingLabel.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

        # IC Label and Entry
        self.icLabel = Label(self.frame, text="IC Number:", font=('Times New Roman', 15), bg='white')
        self.icLabel.grid(row=1, column=0, pady=10, sticky='e')
        self.icEntry = Entry(self.frame, font=('Times New Roman', 15), width=30)
        self.icEntry.grid(row=1, column=1, pady=10, sticky='w')

        # Date Label and Calendar Button
        self.dateLabel = Label(self.frame, text="Choose Date:", font=('Times New Roman', 15), bg='white')
        self.dateLabel.grid(row=2, column=0, pady=10, sticky='e')
        self.dateButton = Button(self.frame, text="Select Date", font=('Times New Roman', 15), command=self.open_calendar)
        self.dateButton.grid(row=2, column=1, pady=10, sticky='w')

        # Display the selected date
        self.selected_date = StringVar()
        self.selected_date_label = Label(self.frame, textvariable=self.selected_date, font=('Times New Roman', 15), bg='white')
        self.selected_date_label.grid(row=2, column=1, padx=(150, 0), pady=10, sticky='w')

        # Time Label and Dropdown
        self.timeLabel = Label(self.frame, text="Choose Time:", font=('Times New Roman', 15), bg='white')
        self.timeLabel.grid(row=3, column=0, pady=10, sticky='e')

        # Create time slots from 8am to 12pm and 1pm to 5pm in 30-minute intervals
        self.time_slots = self.generate_time_slots()
        self.timeVar = StringVar(self.frame)
        self.timeVar.set(self.time_slots[0])  # default value
        self.timeMenu = OptionMenu(self.frame, self.timeVar, *self.time_slots, command=self.update_dentist_options)
        self.timeMenu.config(font=('Times New Roman', 15), bg='white', width=28)
        self.timeMenu.grid(row=3, column=1, pady=10, sticky='w')

        # Service Label and Dropdown
        self.serviceLabel = Label(self.frame, text="Choose Service:", font=('Times New Roman', 15), bg='white')
        self.serviceLabel.grid(row=4, column=0, pady=10, sticky='e')
        self.serviceVar = StringVar(self.frame)
        self.serviceVar.set("Checking")  # default value
        self.serviceMenu = OptionMenu(self.frame, self.serviceVar, "Checking", "Dental Cleaning","Dental Filling", "Orthodontics","Tooth Extraction","Denture Fabrication")
        self.serviceMenu.config(font=('Times New Roman', 15), bg='white', width=28)
        self.serviceMenu.grid(row=4, column=1, pady=10, sticky='w')

        # Dentist Label and Dropdown
        self.dentistLabel = Label(self.frame, text="Choose Dentist:", font=('Times New Roman', 15), bg='white')
        self.dentistLabel.grid(row=5, column=0, pady=10, sticky='e')
        self.dentistVar = StringVar(self.frame)
        self.dentistVar.set("Dr. Tan")  # default value

        # Create a list of dentists
        self.dentists = ["Dr. Tan", "Dr. Marni", "Dr. Tham", "Dr. Thu"]
        self.dentistMenu = OptionMenu(self.frame, self.dentistVar, *self.dentists)
        self.dentistMenu.config(font=('Times New Roman', 15), bg='white', width=28)
        self.dentistMenu.grid(row=5, column=1, pady=10, sticky='w')

        # Submit Button
        self.submitbutt = Button(self.frame, width=10,text='Submit', font=('Segoe UI Black', 16), bd=0, bg='#d6d4d4', command=self.submit_appointment)
        self.submitbutt.grid(row=6, column=1, padx=10, pady=20, sticky="w")

        self.backbutt = Button(self.frame, width=10,text='Back', font=('Segoe UI Black', 16),bd=0, bg='#d6d4d4', command=self.home_page)
        self.backbutt.grid(row=6, column=1, padx=20, pady=20, sticky="e")
        self.booking_window.mainloop()

    def home_page(self):
        self.booking_window.destroy()
        from home import Home
        Home()

    def generate_time_slots(self):
        slots = []
        start_time = time(8, 0)
        end_time = time(12, 0)
        delta = timedelta(minutes=30)

        while start_time < end_time:
            slots.append(start_time.strftime('%H:%M'))
            start_time = (datetime.combine(datetime.today(), start_time) + delta).time()

        start_time = time(13, 0)
        end_time = time(17, 0)
        while start_time < end_time:
            slots.append(start_time.strftime('%H:%M'))
            start_time = (datetime.combine(datetime.today(), start_time) + delta).time()

        return slots

    def open_calendar(self):
        top = Toplevel(self.booking_window)
        top.title("Select Date")
        calendar = Calendar(top, date_pattern='y-mm-dd', mindate=datetime.now().date())
        calendar.pack(pady=20)

        def select_date():
            self.selected_date.set(calendar.get_date())
            self.update_dentist_options()
            top.destroy()

        select_button = Button(top, text="Select", command=select_date)
        select_button.pack(pady=10)

    def update_dentist_options(self, *args):
        appointment_date = self.selected_date.get()
        appointment_time = self.timeVar.get()
        if appointment_date and appointment_time:
            try:
                con = pymysql.connect(host='localhost', user='root', password='', db='user')
                mycursor = con.cursor()
                query = "SELECT dentist, status FROM appointments WHERE date=%s AND time=%s"
                mycursor.execute(query, (appointment_date, appointment_time))
                appointments_info = mycursor.fetchall()

                booked_dentists = [appointment[0] for appointment in appointments_info if appointment[1] != 'cancelled']

                self.dentistMenu['menu'].delete(0, 'end')
                for dentist in self.dentists:
                    state = NORMAL
                    if dentist in booked_dentists:
                        state = DISABLED
                    self.dentistMenu['menu'].add_command(label=dentist, command=tk._setit(self.dentistVar, dentist), state=state)

                con.close()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))

    def submit_appointment(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='', db='user')
            mycursor = con.cursor()
            
            # Ensure appointments table exists and has the correct schema
            create_table_query = '''
                CREATE TABLE IF NOT EXISTS appointments(
                    ic_number INT(12),
                    date DATE,
                    time VARCHAR(5),
                    service VARCHAR(20),
                    dentist VARCHAR(20),
                    status VARCHAR(20),
                    PRIMARY KEY (ic_number)
                )
            '''
            print("Creating appointments table if not exists:", create_table_query)
            mycursor.execute(create_table_query)

            # Check the schema of the 'appointments' table
            mycursor.execute("SHOW CREATE TABLE appointments")
            print("Schema of 'appointments' table:")
            print(mycursor.fetchone()[1])

            ic_number = self.icEntry.get()
            appointment_date = self.selected_date.get()
            appointment_time = self.timeVar.get()
            service = self.serviceVar.get()
            dentist = self.dentistVar.get()

            if ic_number and appointment_date and appointment_time and service and dentist:
                # Check if IC number exists in the member table
                query = "SELECT * FROM member WHERE IC_number=%s"
                mycursor.execute(query, (ic_number,))
                result = mycursor.fetchone()
                if result:
                    print("IC number found in the member table.")

                    # Check if there's a cancelled appointment for the selected date, time, and dentist
                    cancel_check_query = "SELECT * FROM appointments WHERE date=%s AND time=%s AND dentist=%s AND status='cancelled'"
                    mycursor.execute(cancel_check_query, (appointment_date, appointment_time, dentist))
                    cancelled_appointment = mycursor.fetchone()
                    
                    if cancelled_appointment:
                        # If there's a cancelled appointment, update its status to 'reserved'
                        update_query = "UPDATE appointments SET status='reserved' WHERE date=%s AND time=%s AND dentist=%s AND status='cancelled'"
                        mycursor.execute(update_query, (appointment_date, appointment_time, dentist))
                        con.commit()
                        messagebox.showinfo("Success", "Appointment reserved successfully!")
                    else:
                        # If there's no cancelled appointment, insert a new one with 'reserved' status
                        insert_query = "INSERT INTO appointments (ic_number, date, time, service, dentist, status) VALUES (%s, %s, %s, %s, %s, %s)"
                        print("Inserting appointment details into appointments table:", insert_query)
                        mycursor.execute(insert_query, (ic_number, appointment_date, appointment_time, service, dentist, "reserved"))
                        con.commit()
                        messagebox.showinfo("Success", "Appointment booked successfully!")
                else:
                    messagebox.showerror("Error", "IC number not found!")
        except pymysql.err.IntegrityError:
            messagebox.showerror("Error", "This time slot with the selected dentist is already booked.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            con.close()
    
BookAppointment()
