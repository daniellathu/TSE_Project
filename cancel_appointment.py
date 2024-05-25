import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql

class CancelAppointment:
    def __init__(self):
        self.cancel_window = tk.Tk()
        self.cancel_window.resizable(False, False)
        self.cancel_window.title('Cancel Appointment')

        # Load the background image
        bg_image = Image.open('background.jpg')
        self.bgImage = ImageTk.PhotoImage(bg_image)

        # Create a label for the background image
        self.bgLabel = tk.Label(self.cancel_window, image=self.bgImage)
        self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Set the size of the home window to match the size of the background image
        width, height = bg_image.size
        self.cancel_window.geometry(f"{width}x{height}")

        # Create an outer frame to center the inner frame
        self.outer_frame = tk.Frame(self.cancel_window, bg='white')
        self.outer_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.frame = tk.Frame(self.outer_frame, width=870, height=600, bg='white')
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        # Header
        self.headingLabel = tk.Label(self.frame, text='Cancel Appointment', font=('Times New Roman', 23), bg='white', fg='black')
        self.headingLabel.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

        # IC Label and Entry
        self.icLabel = tk.Label(self.frame, text="IC Number:", font=('Times New Roman', 15), bg='white')
        self.icLabel.grid(row=1, column=0, pady=10, sticky='e')
        self.icEntry = tk.Entry(self.frame, font=('Times New Roman', 15), width=30)
        self.icEntry.grid(row=1, column=1, pady=10, sticky='w')

        # Submit Button
        self.submitbutt = Button(self.frame, width=10,text='Submit', font=('Segoe UI Black', 16), bd=0, bg='#d6d4d4', command=self.cancel_appointment)
        self.submitbutt.grid(row=6, column=1, padx=10, pady=20, sticky="w")

        self.backbutt = Button(self.frame, width=10,text='Back', font=('Segoe UI Black', 16),bd=0, bg='#d6d4d4', command=self.home_page)
        self.backbutt.grid(row=6, column=1, padx=20, pady=20, sticky="e")

        self.cancel_window.mainloop()

    def home_page(self):
        self.cancel_window.destroy()
        from home import Home
        Home()

    def cancel_appointment(self):
        ic_number = self.icEntry.get()

        if ic_number:
            try:
                # Connect to the database
                con = pymysql.connect(host='localhost', user='root', password='', db='user')
                with con:
                    # Create cursor
                    cursor = con.cursor()

                    # Check for active appointments with the given IC number
                    query = "SELECT * FROM appointments WHERE ic_number=%s AND status='reserved'"
                    cursor.execute(query, (ic_number,))
                    appointments = cursor.fetchall()

                    if appointments:
                        # Create a new window to display the appointments
                        cancel_window = tk.Toplevel(self.cancel_window)
                        cancel_window.title("Select Appointment to Cancel")
                        
                        # Create a listbox to display the appointments
                        appointment_listbox = tk.Listbox(cancel_window, font=('Times New Roman', 15), width=50, height=10)
                        appointment_listbox.pack(padx=10, pady=10)

                        # Add each appointment to the listbox
                        for appointment in appointments:
                            appointment_str = f"Date: {appointment[1]}, Time: {appointment[2]}, Dentist: {appointment[4]}"
                            appointment_listbox.insert(tk.END, appointment_str)

                        # Create a button to cancel the selected appointment
                        cancel_button = tk.Button(cancel_window, text="Cancel Selected Appointment", font=('Times New Roman', 15), bg='lightblue', command=lambda: cancel_selected_appointment(ic_number, appointments, appointment_listbox))
                        cancel_button.pack(pady=10)
                    else:
                        messagebox.showerror("Error", "No active appointments found with this IC number!")
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Warning", "Please enter the IC number.")

def cancel_selected_appointment(ic_number, appointments, appointment_listbox):
    selected_index = appointment_listbox.curselection()
    if selected_index:
        # Get the appointment from the appointments list using the selected index
        selected_appointment = appointments[selected_index[0]]
        try:
            # Connect to the database
            con = pymysql.connect(host='localhost', user='root', password='', db='user')
            with con:
                # Create cursor
                cursor = con.cursor()

                # Update the status of the selected appointment to 'cancelled'
                update_query = "UPDATE appointments SET status='cancelled' WHERE ic_number=%s AND date=%s AND time=%s AND dentist=%s AND status='reserved'"
                cursor.execute(update_query, (ic_number, selected_appointment[1], selected_appointment[2], selected_appointment[4]))
                con.commit()
                messagebox.showinfo("Success", "Appointment cancelled successfully!")
                
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
    else:
        messagebox.showwarning("Warning", "Please select an appointment to cancel.")

# Run the application
if __name__ == "__main__":
    app = CancelAppointment()
