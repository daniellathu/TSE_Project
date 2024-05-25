import tkinter as tk
import pymysql
from tkinter import *
from tkinter import messagebox
from Main import Main
from PIL import Image, ImageTk

class RegisterMember:

    def __init__(self):
        self.register_window = tk.Tk()
        self.register_window.resizable(False, False)
        self.register_window.title('Add New Member Page')

        # Load the background image
        bg_image = Image.open('background.jpg')
        self.bgImage = ImageTk.PhotoImage(bg_image)

        # Get the dimensions of the original image
        width, height = bg_image.size

        # Create a label for the background image
        self.bgLabel = Label(self.register_window, image=self.bgImage)
        self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Set the size of the home window to match the size of the background image
        self.register_window.geometry(f"{width}x{height}")
        
        # Create an outer frame to center the inner frame
        self.outer_frame = Frame(self.register_window, bg='white')
        self.outer_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.frame = Frame(self.outer_frame, width=870, height=500, bg='white')
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        # Header
        self.headingLabel = Label(self.frame, text='Register New Member', font=('Times New Roman', 23), bg='white', fg='black')
        self.headingLabel.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")
        
        # Name
        self.NameLabel = Label(self.frame, text='Full Name', font=('Times New Roman', 12), bg='white', fg='black')
        self.NameLabel.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="e")

        self.NameEntry = Entry(self.frame, width=40, font=('Times New Roman', 12, 'bold'))
        self.NameEntry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # IC number
        self.ICLabel = Label(self.frame, text='Identification Card Number ', font=('Times New Roman', 12), bg='white', fg='black')
        self.ICLabel.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="e")

        self.ICEntry = Entry(self.frame, width=40, font=('Times New Roman', 12, 'bold'))
        self.ICEntry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.ICEntry.insert(0, 'Exp. 020202116684')
        self.ICEntry.bind("<FocusIn>", self.clear_placeholder_ic)
        self.ICEntry.bind("<FocusOut>", self.add_placeholder_ic)

        # Age
        self.AgeLabel = Label(self.frame, text='Age', font=('Times New Roman', 12), bg='white', fg='black')
        self.AgeLabel.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        self.AgeEntry = Entry(self.frame, width=40, font=('Times New Roman', 12, 'bold'))
        self.AgeEntry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Gender
        self.GenderLabel = Label(self.frame, text='Gender (Female/Male)', font=('Times New Roman', 12), bg='white', fg='black')
        self.GenderLabel.grid(row=4, column=0, padx=10, pady=5, sticky="e")

        self.GenderEntry = Entry(self.frame, width=40, font=('Times New Roman', 12, 'bold'))
        self.GenderEntry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Phone number
        self.PhnoLabel = Label(self.frame, text='Phone number', font=('Times New Roman', 12), bg='white', fg='black')
        self.PhnoLabel.grid(row=5, column=0, padx=10, pady=5, sticky="e")

        self.PhnoEntry = Entry(self.frame, width=40, font=('Times New Roman', 12, 'bold'))
        self.PhnoEntry.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        self.PhnoEntry.insert(0, 'Exp. 0123456789')
        self.PhnoEntry.bind("<FocusIn>", self.clear_placeholder_phno)
        self.PhnoEntry.bind("<FocusOut>", self.add_placeholder_phno)

        # Email
        self.EmailLabel = Label(self.frame, text='Email', font=('Times New Roman', 12), bg='white', fg='black')
        self.EmailLabel.grid(row=6, column=0, padx=10, pady=5, sticky="e")

        self.EmailEntry = Entry(self.frame, width=40, font=('Times New Roman', 12, 'bold'))
        self.EmailEntry.grid(row=6, column=1, padx=10, pady=5, sticky="w")
        self.EmailEntry.insert(0, 'Exp. ali@gmail.com')
        self.EmailEntry.bind("<FocusIn>", self.clear_placeholder_email)
        self.EmailEntry.bind("<FocusOut>", self.add_placeholder_email)


        # Register button

        self.Registerbutt = Button(self.frame, width=10,text='Register', font=('Segoe UI Black', 16), bd=0, bg='#d6d4d4', command=self.connectdatabase)
        self.Registerbutt.grid(row=7, column=1, padx=10, pady=20, sticky="w")

        self.backbutt = Button(self.frame, width=10,text='Back', font=('Segoe UI Black', 16),bd=0, bg='#d6d4d4', command=self.home_page)
        self.backbutt.grid(row=7, column=1, padx=40, pady=20, sticky="e")

        self.register_window.mainloop()
    
    def home_page(self):
        self.register_window.destroy()
        from home import Home
        Home()

    def clear_placeholder_ic(self, event):
        if self.ICEntry.get() == 'Exp. 020202116684':
            self.ICEntry.delete(0, END)
            self.ICEntry.config(fg='black')

    def add_placeholder_ic(self, event):
        if self.ICEntry.get() == '':
            self.ICEntry.insert(0, 'Exp. 020202116684')
            self.ICEntry.config(fg='grey')

    def clear_placeholder_phno(self, event):
        if self.PhnoEntry.get() == 'Exp. 0123456789':
            self.PhnoEntry.delete(0, END)
            self.PhnoEntry.config(fg='black')

    def add_placeholder_phno(self, event):
        if self.PhnoEntry.get() == '':
            self.PhnoEntry.insert(0, 'Exp. 0123456789')
            self.PhnoEntry.config(fg='grey')

    def clear_placeholder_email(self, event):
        if self.EmailEntry.get() == 'Exp. ali@gmail.com':
            self.EmailEntry.delete(0, END)
            self.EmailEntry.config(fg='black')

    def add_placeholder_email(self, event):
        if self.EmailEntry.get() == '':
            self.EmailEntry.insert(0, 'Exp. ali@gmail.com')
            self.EmailEntry.config(fg='grey')

    def connectdatabase(self):
        if self.NameEntry.get() == '' or self.ICEntry.get() == '' or self.AgeEntry.get() == '' or self.GenderEntry.get() == '' or self.PhnoEntry.get() == '' or self.EmailEntry.get() == '':
            messagebox.showerror('Error', 'Please fill in all the fields')
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='')  # Update username and password here
                mycursor = con.cursor()
        
                # Create the database if not exists
                mycursor.execute('CREATE DATABASE IF NOT EXISTS user')
                mycursor.execute('USE user')

                # Create table if not exists
                mycursor.execute('''
                    CREATE TABLE IF NOT EXISTS member(
                        IC_number VARCHAR(12) PRIMARY KEY, 
                        name VARCHAR(50), 
                        age INT, 
                        gender VARCHAR(6), 
                        phone_number VARCHAR(10), 
                        email VARCHAR(50)
                    )
                ''')

                # Check if the IC number exists
                query = 'SELECT * FROM member WHERE IC_number=%s'
                mycursor.execute(query, (self.ICEntry.get(),))
                row = mycursor.fetchone()

                if row is not None:
                    messagebox.showerror('Error', 'Member already exists')
                else:
                    # Insert data
                    icnum = self.ICEntry.get()
                    name = self.NameEntry.get()
                    age = self.AgeEntry.get()
                    gender = self.GenderEntry.get()
                    phone_number = self.PhnoEntry.get()
                    email = self.EmailEntry.get()

                    query_insert = 'INSERT INTO member (IC_number, name, age, gender, phone_number, email) VALUES (%s, %s, %s, %s, %s, %s)'
                    mycursor.execute(query_insert, (icnum, name, age, gender, phone_number, email))
            
                    con.commit()  # Commit the transaction
                    messagebox.showinfo('Success', 'Member registered successfully')
                    self.clear()

            except Exception as e:
                messagebox.showerror('Error', f'Error: {str(e)}')
                con.rollback()  # Rollback the transaction in case of error
            finally:
                con.close()  # Close the connection

    def clear(self):
        self.NameEntry.delete(0, END)
        self.ICEntry.delete(0, END)
        self.ICEntry.insert(0, 'Exp. 020202116684')
        self.ICEntry.config(fg='grey')
        self.AgeEntry.delete(0, END)
        self.GenderEntry.delete(0, END)
        self.PhnoEntry.delete(0, END)
        self.PhnoEntry.insert(0, 'Exp. 0123456789')
        self.PhnoEntry.config(fg='grey')
        self.EmailEntry.delete(0, 'Exp,ali@gmail.com')

if __name__ == "__Main__":
    RegisterMember()

