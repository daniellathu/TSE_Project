import tkinter as tk
import pymysql
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

class Main:
    
    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.resizable(False, False)
        self.login_window.title('Login Page')
        
        # Load the background image
        bg_image = Image.open('home.jpg')
        self.bgImage = ImageTk.PhotoImage(bg_image)

        # Get the dimensions of the original image
        width, height = bg_image.size

        # Create a label for the background image
        self.bgLabel = tk.Label(self.login_window, image=self.bgImage)
        self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Set the size of the signup window to match the size of the background image
        self.login_window.geometry(f"{width}x{height}")

        self.frame = Frame(self.login_window, width=500, height=600, bg='white')
        self.frame.place(x=558, y=190)

        # header
        self.headingLabel = Label(self.frame, text='LOGIN', font=('Times New Roman', 18), bg='white', fg='black')
        self.headingLabel.grid(row=0, column=0, columnspan=2, padx=50, pady=10)

        # username
        self.usernameLabel = Label(self.frame, text='Username', font=('Times New Roman', 15,'bold'), bg='white', fg='black')
        self.usernameLabel.grid(row=1, column=0, padx=40, pady=10, sticky='e')

        self.username = Entry(self.frame,font=('Times New Roman', 12), bg='white', fg='black')
        self.username.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.username.insert(0, 'Username')
        self.username.bind('<FocusIn>', self.UserName_enter)


        # password
        self.passwordLabel = Label(self.frame, text='Password', font=('Times New Roman', 15,'bold'), bg='white', fg='black')
        self.passwordLabel.grid(row=3, column=0, padx=40, pady=10, sticky='e')

        self.password = Entry(self.frame,font=('Times New Roman', 12), bg='white', fg='black')
        self.password.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        self.password.insert(0, 'Password')
        self.password.bind('<FocusIn>', self.pass_enter)


        # Forgot password button
        self.forgotpassbutt = Button(self.frame, text='Forgot Password',font=('Segoe UI Black',12),bd=0,bg='#d6d4d4', command=self.forgotpass)
        self.forgotpassbutt.grid(row=5, column=1, padx=130,pady=20,sticky='w')

        # login button
        self.loginbutt = Button(self.frame, width=10, text='Login', font=('Segoe UI Black',12),bd=0,bg='#d6d4d4',command=self.login_user)
        self.loginbutt.grid(row=5, column=1, padx=0, pady=20, sticky='w')

        # sign up label
        self.signuplabel = Label(self.frame, text='---------Dont have an account?-----------',font=('Times New Roman',12), bg='white')
        self.signuplabel.grid(row=7, column=0, columnspan=2, padx=40, pady=10)

        # go to sign up page button
        self.newaccbutt = Button(self.frame, text='Create a new account', font=('Segoe UI Black',12),bd=0,bg='#d6d4d4', command=self.signup_page)
        self.newaccbutt.grid(row=8, column=0, columnspan=2, padx=40, pady=5)

        self.login_window.mainloop()
    
    def login_user(self):
        if self.username.get() == '' or self.password.get() == '':
            messagebox.showerror('Error', 'All fields are required')
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='')
                mycursor = con.cursor()
            except:
                messagebox.showerror('Error', 'Connection is not established. Please try again.')
                return
            
            try:
                query = 'USE user'
                mycursor.execute(query)
                query = 'SELECT * FROM data WHERE username=%s AND password=%s'
                mycursor.execute(query, (self.username.get(), self.password.get()))
                row = mycursor.fetchone()
                if row is None:
                    messagebox.showerror('Error', 'Invalid username or password')
                    self.clear()
                else:
                    messagebox.showinfo('Success', 'Login is successful')
                    self.login_window.destroy()
                    from home import Home
                    Home()
                    
            except Exception as e:
                messagebox.showerror('Error', f'An error occurred: {str(e)}')
            finally:
                con.close()

    def forgotpass(self):
        self.login_window.destroy()
        from forgot_password import forgot_password
        forgot_password()

    def clear(self):
        self.username.delete(0,END)
        self.password.delete(0,END)

    def UserName_enter(self, event):
        if self.username.get() == 'Username':
            self.username.delete(0, END)

    def pass_enter(self, event):
        if self.password.get() == 'Password':
            self.password.delete(0, END)
            self.password.config(show='*')

    def signup_page(self):
        self.login_window.destroy()  # Destroy the login window
        from Signup import Signup
        Signup()  # Create an instance of the Signup class

Main()
