import tkinter as tk
from tkinter import END, Button, Entry, Frame, Label
import pymysql
from Main import Main
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

class forgot_password:
    
    def __init__(self):
        self.forgot_password_window = tk.Tk()
        self.forgot_password_window.resizable(False, False)
        self.forgot_password_window.title('Forgot Password Page')

        # Load the background image
        bg_image = Image.open('home.jpg')
        self.bgImage = ImageTk.PhotoImage(bg_image)

        # Get the dimensions of the original image
        width, height = bg_image.size

        # Create a label for the background image
        self.bgLabel = Label(self.forgot_password_window, image=self.bgImage)
        self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Set the size of the forgot_password window to match the size of the background image
        self.forgot_password_window.geometry(f"{width}x{height}")

        self.frame=Frame(self.forgot_password_window,width=500,height=600,bg='white')
        self.frame.place(x=558,y=190)

        # header
        self.headingLabel = Label(self.frame, text='Change Your Password', font=('Times New Roman', 23),bg='white',fg='black')
        self.headingLabel.grid(row=0, column=0, columnspan=2, padx=50, pady=10,sticky='w')

        # Username
        self.UsernameLabel = Label(self.frame, text='Username', font=('Times New Roman', 12),bg='white',fg='black')
        self.UsernameLabel.grid(row=4, column=0, padx=40, pady=5, sticky='w')

        self.UsernameEntry = Entry(self.frame, width=40, font=('Times New Roman',12,'bold'))
        self.UsernameEntry.grid(row=5, column=0, padx=40, pady=5, sticky='w')

        # New Password
        self.NewPassLabel = Label(self.frame, text='New Password', font=('Times New Roman', 12),bg='white',fg='black')
        self.NewPassLabel.grid(row=8, column=0, padx=40, pady=(10,0), sticky='w')

        self.NewPassEntry = Entry(self.frame, width=40, font=('Times New Roman',12,'bold'))
        self.NewPassEntry.grid(row=9, column=0, padx=40, pady=5, sticky='w')
        


        # Confirm Password
        self.ConPassLabel = Label(self.frame, text='Confirm Password', font=('Times New Roman', 12),bg='white',fg='black')
        self.ConPassLabel.grid(row=10, column=0, padx=40, pady=(10,0), sticky='w')

        self.ConPassEntry = Entry(self.frame, width=40, font=('Times New Roman',12,'bold'))
        self.ConPassEntry.grid(row=11, column=0, padx=40, pady=5, sticky='w')

        # Back button
        self.backbutt = Button(self.frame, width=10,text='Back',height=2,font=('Segoe UI Black',12),bd=0,bg='#d6d4d4',command=self.back)
        self.backbutt.grid(row=13,column=0,padx=50, pady=(10,0),sticky='w')

        #Update Password Button
        self.updatebutt = Button(self.frame, width=16,height=2,text='Update Password',font=('Segoe UI Black',12),bd=0,bg='#d6d4d4',command=self.connect_database)
        self.updatebutt.grid(row=13,column=0,padx=250,pady=(10,0),sticky='w')

        self.forgot_password_window.mainloop()

    def clear(self):
        self.UsernameEntry.delete(0, END)
        self.NewPassEntry.delete(0,END)
        self.ConPassEntry.delete(0,END)


    def connect_database(self):
        username = self.UsernameEntry.get()
        new_password = self.NewPassEntry.get()
        confirm_password = self.ConPassEntry.get()

        # Check if any field is empty
        if any(field == '' for field in [username, new_password, confirm_password]):
            messagebox.showerror('Error', 'Please fill in all the fields')
            return

        # Check if the new password matches the confirm password
        if new_password != confirm_password:
            messagebox.showerror('Error', 'Password mismatch')
            self.clear()
            return

        try:
            con = pymysql.connect(host='localhost', user='root', password='', database='user')
            mycursor = con.cursor()

            # Check if the username exists
            query = 'SELECT * FROM data WHERE username=%s'
            mycursor.execute(query, (username,))
            row = mycursor.fetchone()

            if row is None:
                messagebox.showerror('Error', 'Username does not exist')
                self.clear()
                return

            # Update the password for the username
            query_update = 'UPDATE data SET password=%s WHERE username=%s'
            mycursor.execute(query_update, (new_password, username))

            con.commit()
            messagebox.showinfo('Success', 'Password updated successfully')

        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}')
            con.rollback()
        finally:
            con.close()

    def back(self):
        self.forgot_password_window.destroy()
        from Main import Main
        Main()

# Check if the script is run directly
if __name__ == "__Main__":
    forgot_password()
