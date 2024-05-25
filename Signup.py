import tkinter as tk
import pymysql
from tkinter import *
from tkinter import messagebox
from Main import Main
from PIL import Image, ImageTk

class Signup:
    
    def __init__(self):
        self.signup_window = tk.Tk()
        self.signup_window.resizable(False, False)
        self.signup_window.title('Signup Page')

        # Load the background image
        bg_image = Image.open('home.jpg')
        self.bgImage = ImageTk.PhotoImage(bg_image)

        # Get the dimensions of the original image
        width, height = bg_image.size

        # Create a label for the background image
        self.bgLabel = Label(self.signup_window, image=self.bgImage)
        self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Set the size of the signup window to match the size of the background image
        self.signup_window.geometry(f"{width}x{height}")

        self.frame=Frame(self.signup_window,width=500,height=600,bg='white')
        self.frame.place(x=558,y=190)

        # header
        self.headingLabel = Label(self.frame, text='CREATE A NEW ACCOUNT', font=('Times New Roman', 23),bg='white',fg='black')
        self.headingLabel.grid(row=0, column=0, columnspan=2, padx=50, pady=10,sticky='w')

        # Email
        self.emailLabel = Label(self.frame, text='Email', font=('Times New Roman', 12,'bold'),bg='white',fg='black')
        self.emailLabel.grid(row=1, column=0, padx=40, pady=5, sticky='w')

        self.emailEntry = Entry(self.frame, width=40, font=('Times New Roman',12,'bold'))
        self.emailEntry.grid(row=2, column=0, padx=40, pady=5, sticky='w')

        # Username
        self.UsernameLabel = Label(self.frame, text='Username', font=('Times New Roman', 12,'bold'),bg='white',fg='black')
        self.UsernameLabel.grid(row=4, column=0, padx=40, pady=5, sticky='w')

        self.UsernameEntry = Entry(self.frame, width=40, font=('Times New Roman',12,'bold'))
        self.UsernameEntry.grid(row=5, column=0, padx=40, pady=5, sticky='w')
        
        # Name
        self.NameLabel = Label(self.frame, text='Full Name', font=('Times New Roman', 12,'bold'),bg='white',fg='black')
        self.NameLabel.grid(row=6, column=0, padx=40, pady=(10,0), sticky='w')

        self.NameEntry = Entry(self.frame, width=40, font=('Times New Roman',12,'bold'))
        self.NameEntry.grid(row=7, column=0, padx=40, pady=5, sticky='w')
        


        # Password
        self.PassLabel = Label(self.frame, text='Password', font=('Times New Roman', 12,'bold'),bg='white',fg='black')
        self.PassLabel.grid(row=8, column=0, padx=40, pady=(10,0), sticky='w')

        self.PassEntry = Entry(self.frame, width=40, font=('Times New Roman',12,'bold'))
        self.PassEntry.grid(row=9, column=0, padx=40, pady=5, sticky='w')
        


        # Confirm Password
        self.ConPassLabel = Label(self.frame, text='Confirm Password', font=('Times New Roman', 12,'bold'),bg='white',fg='black')
        self.ConPassLabel.grid(row=10, column=0, padx=40, pady=(10,0), sticky='w')

        self.ConPassEntry = Entry(self.frame, width=40, font=('Times New Roman',12,'bold'))
        self.ConPassEntry.grid(row=11, column=0, padx=40, pady=5, sticky='w')

        #Checkbox
        self.Check=IntVar()
        self.Checkbox=Checkbutton(self.frame,text='I agree with the Terms & Conditions',bg='white',activebackground='white',activeforeground='black',variable=self.Check)
        self.Checkbox.grid(row=12,column=0,padx=40,pady=10,sticky='w')
        
        # Signup button
        self.newaccbutt = Button(self.frame, width=10,text='Sign Up',font=('Segoe UI Black',16),bd=0,bg='#d6d4d4',command=self.connect_database)
        self.newaccbutt.grid(row=13,column=0,padx=50,sticky='w')

        #Login Button
        self.loginbutt = Button(self.frame, width=10,text='Login',font=('Segoe UI Black',16),bd=0,bg='#d6d4d4',command=self.login_page)
        self.loginbutt.grid(row=13,column=0,padx=250,sticky='w')

        self.signup_window.mainloop()
    def clear(self):
        self.emailEntry.delete(0,END)
        self.UsernameEntry.delete(0, END)
        self.NameEntry.delete(0,END)
        self.PassEntry.delete(0,END)
        self.ConPassEntry.delete(0,END)
        self.Check.set(0)


    def connect_database(self):
        if self.emailEntry.get()=='' or self.UsernameEntry.get()=='' or self.PassEntry.get()=='' or self.ConPassEntry.get()=='':
            messagebox.showerror('Error','Please fill in all the field')
        elif self.PassEntry.get()!=self.ConPassEntry.get():
            messagebox.showerror('Error','Password Dismatch')
        elif self.Check.get()==0:
            messagebox.showerror('Error','Please accept the T&C')
        else:
            try:
                con=pymysql.connect(host='localhost', user='root', password='')  # Update username and password here
                mycursor=con.cursor()
        
                # Create the database if not exists
                mycursor.execute('CREATE DATABASE IF NOT EXISTS user')
                mycursor.execute('USE user')

                # Create table if not exists
                mycursor.execute('CREATE TABLE IF NOT EXISTS admin(id INT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(50), username VARCHAR(50), name VARCHAR(50), password VARCHAR(20))')
        
                

                #Check if the username exists
                query='SELECT * FROM admin WHERE username=%s'
                mycursor.execute(query,(self.UsernameEntry.get(),))
                row=mycursor.fetchone()

                if row is not None:
                    messagebox.showerror('Error','Username already exists')
                    self.clear()
                else:
                    # Insert data
                    email = self.emailEntry.get()
                    username = self.UsernameEntry.get()
                    name = self.NameEntry.get()
                    password = self.PassEntry.get()

                    query_insert = 'INSERT INTO data (email, username, name, password) VALUES (%s, %s, %s, %s)'
                    mycursor.execute(query_insert, (email, username, name, password))
            
                    con.commit()  # Commit the transaction
                    messagebox.showinfo('Success', 'Signup Successfully')
                    self.clear()

            except Exception as e:
                messagebox.showerror('Error', f'Error: {str(e)}')
                con.rollback()  # Rollback the transaction in case of error
            finally:
                con.close()  # Close the connection


    def login_page(self):
        self.signup_window.destroy()  # Destroy the signup window
        Main()  # Open the Main window

if __name__ == "__Main__":
    Signup()
