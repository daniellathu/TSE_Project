import tkinter as tk
import pymysql
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

class Edit:
    def __init__(self):
        self.edit_window = tk.Tk()
        self.edit_window.resizable(False, False)
        self.edit_window.title('Edit Member')

        # Load the background image
        bg_image = Image.open('background.jpg')
        self.bgImage = ImageTk.PhotoImage(bg_image)

        # Get the dimensions of the original image
        width, height = bg_image.size

        # Create a label for the background image
        self.bgLabel = Label(self.edit_window, image=self.bgImage)
        self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Set the size of the home window to match the size of the background image
        self.edit_window.geometry(f"{width}x{height}")

        # Create an outer frame to center the inner frame
        self.outer_frame = Frame(self.edit_window, bg='white')
        self.outer_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.frame = Frame(self.outer_frame, width=870, height=600, bg='white')
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        # Header
        self.headingLabel = Label(self.frame, text='Edit Member', font=('Times New Roman', 23), bg='white', fg='black')
        self.headingLabel.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

        # IC number
        self.ICLabel = Label(self.frame, text='Identification Card Number ', font=('Times New Roman', 12), bg='white', fg='black')
        self.ICLabel.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="e")

        self.ICEntry = Entry(self.frame, width=40, font=('Times New Roman', 12, 'bold'))
        self.ICEntry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Search Button to Search Member
        self.searchbutt = Button(self.frame,width=10, text="Search", font=('Segoe UI Black', 15), bd=0, bg='#d6d4d4', command=self.search_member)
        self.searchbutt.grid(row=2, column=1,padx=10,pady=20,sticky='w')

        self.backbutt = Button(self.frame, width=10,text='Back', font=('Segoe UI Black', 15),bd=0, bg='#d6d4d4', command=self.home_page)
        self.backbutt.grid(row=2, column=1,padx=20,pady=20,sticky='e')

        # Name
        self.NameLabel = Label(self.frame, text='Full Name', font=('Times New Roman', 12), bg='white', fg='black')
        self.NameLabel.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        self.NameEntry = Entry(self.frame, width=40, font=('Times New Roman', 12, 'bold'))
        self.NameEntry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Gender
        self.GenderLabel = Label(self.frame, text='Gender (Female/Male)', font=('Times New Roman', 12), bg='white', fg='black')
        self.GenderLabel.grid(row=4, column=0, padx=10, pady=5, sticky="e")

        self.GenderEntry = Entry(self.frame, width=40, font=('Times New Roman', 12, 'bold'))
        self.GenderEntry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Age
        self.AgeLabel = Label(self.frame, text='Age', font=('Times New Roman', 12), bg='white', fg='black')
        self.AgeLabel.grid(row=5, column=0, padx=10, pady=5, sticky="e")

        self.AgeEntry = Entry(self.frame, width=40, font=('Times New Roman', 12, 'bold'))
        self.AgeEntry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Phone number
        self.PhnoLabel = Label(self.frame, text='Phone number', font=('Times New Roman', 12), bg='white', fg='black')
        self.PhnoLabel.grid(row=6, column=0, padx=10, pady=5, sticky="e")

        self.PhnoEntry = Entry(self.frame, width=40, font=('Times New Roman', 12, 'bold'))
        self.PhnoEntry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Email
        self.EmailLabel = Label(self.frame, text='Email', font=('Times New Roman', 12), bg='white', fg='black')
        self.EmailLabel.grid(row=7, column=0, padx=10, pady=5, sticky="e")

        self.EmailEntry = Entry(self.frame, width=40, font=('Times New Roman', 12, 'bold'))
        self.EmailEntry.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        # Edit Button
        self.edit_button = Button(self.frame, text="Edit", width=10, font=('Segoe UI Black', 15),bd=0, bg='#d6d4d4', command=self.edit_member)
        self.edit_button.grid(row=8, column=0, columnspan=2, pady=20)

        self.edit_window.mainloop()

    def home_page(self):
        self.edit_window.destroy()
        from home import Home

    def search_member(self):
        # Get the IC number from the entry field
        ic_number = self.ICEntry.get()

        if ic_number:
            try:
                # Connect to the database
                con = pymysql.connect(host='localhost', user='root', password='', db='user')
                mycursor = con.cursor()

                # Fetch member details based on IC number
                query = "SELECT * FROM member WHERE IC_number=%s"
                mycursor.execute(query, (ic_number,))
                member_details = mycursor.fetchone()

                if member_details:
                    # Fill member details in the respective entry fields
                    self.NameEntry.delete(0, END)
                    self.NameEntry.insert(END, member_details[1])

                    self.GenderEntry.delete(0, END)
                    self.GenderEntry.insert(END, member_details[2])

                    self.AgeEntry.delete(0, END)
                    self.AgeEntry.insert(END, member_details[3])

                    self.PhnoEntry.delete(0, END)
                    self.PhnoEntry.insert(END, member_details[5])

                    self.EmailEntry.delete(0, END)
                    self.EmailEntry.insert(END, member_details[4])

                else:
                    messagebox.showerror("Error", "No member found with this IC number!")
                con.close()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Warning", "Please enter the IC number.")

    def edit_member(self):
        # Get the IC number from the entry field
        ic_number = self.ICEntry.get()

        # Get the edited details from the entry fields
        name = self.NameEntry.get()
        gender = self.GenderEntry.get()
        age = self.AgeEntry.get()
        phone = self.PhnoEntry.get()
        email = self.EmailEntry.get()

        # Update the member details in the database
        if ic_number:
            try:
                # Connect to the database
                con = pymysql.connect(host='localhost', user='root', password='', db='user')
                mycursor = con.cursor()

                # Update member details
                query = "UPDATE member SET Name=%s, Gender=%s, Age=%s, Phone=%s, Email=%s WHERE IC_number=%s"
                mycursor.execute(query, (name, gender, age, phone, email, ic_number))
                con.commit()

                messagebox.showinfo("Success", "Member details updated successfully!")

                # Clear entry fields after updating
                self.clear_fields()

            except Exception as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                con.close()
        else:
            messagebox.showwarning("Warning", "Please enter the IC number.")

    def clear_fields(self):
        # Clear all entry fields
        self.NameEntry.delete(0, END)
        self.GenderEntry.delete(0, END)
        self.AgeEntry.delete(0, END)
        self.PhnoEntry.delete(0, END)
        self.EmailEntry.delete(0, END)
Edit()
