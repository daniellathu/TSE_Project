import tkinter as tk
import pymysql
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

class FeedbackMember:

    def __init__(self):
        self.Feedback_window = tk.Tk()
        self.Feedback_window.resizable(False, False)
        self.Feedback_window.title('Feedback Page')

        # Load the background image
        bg_image = Image.open('background.jpg')
        self.bgImage = ImageTk.PhotoImage(bg_image)

        # Get the dimensions of the original image
        width, height = bg_image.size

        # Create a label for the background image
        self.bgLabel = Label(self.Feedback_window, image=self.bgImage)
        self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Set the size of the home window to match the size of the background image
        self.Feedback_window.geometry(f"{width}x{height}")

        # Create an outer frame to center the inner frame
        self.outer_frame = Frame(self.Feedback_window, bg='white')
        self.outer_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.frame = Frame(self.outer_frame, width=870, height=500, bg='white')
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        # Header
        self.headingLabel = Label(self.frame, text='Feedback and Comment', font=('Times New Roman', 23), bg='white', fg='black')
        self.headingLabel.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

        # Name Entry
        self.name_label = Label(self.frame, text='Member Name:', font=('Times New Roman', 12), bg='white', fg='black')
        self.name_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="e")

        self.name_entry = Entry(self.frame, width=60, font=('Times New Roman', 12))
        self.name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Comment Entry
        self.comment_label = Label(self.frame, text='Enter your comment:', font=('Times New Roman', 12), bg='white', fg='black')
        self.comment_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.comment_entry = Text(self.frame, width=60, height=5, font=('Times New Roman', 12))
        self.comment_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Submit Button to Add Comment
        self.submitButton = Button(self.frame, text="Add Comments", font=('Segoe UI Black', 15),bd=0, bg='#d6d4d4', command=self.add_comment)
        self.submitButton.grid(row=3, column=1, padx=0, pady=20,sticky='w')

        self.backbutt = Button(self.frame, width=10,text='Back', font=('Segoe UI Black', 15),bd=0, bg='#d6d4d4', command=self.home_page)
        self.backbutt.grid(row=3, column=1,padx=0,pady=20,sticky='e')

        # Comment Table
        self.comment_table = Listbox(self.frame, width=60, height=10, font=('Times New Roman', 12), bg='light grey')
        self.comment_table.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Connect to the database
        self.connection = pymysql.connect(host='localhost', user='root', password='', db='user')
        self.cursor = self.connection.cursor()

        # Create table if not exists
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS comments(
                        member_name VARCHAR(100),
                        comment_text VARCHAR(300)
                    )
                ''')

        # Retrieve comments from the database and display them
        self.retrieve_comments()

        self.Feedback_window.mainloop()

    def home_page(self):
        self.Feedback_window.destroy()
        from home import Home

    def add_comment(self):
        # Get the member name and comment from the entry fields
        member_name = self.name_entry.get()
        comment = self.comment_entry.get("1.0", "end-1c")

        

        if member_name and comment:
            # Save the comment to the database
            try:
                query = "INSERT INTO comments (member_name, comment_text) VALUES (%s, %s)"
                self.cursor.execute(query, (member_name, comment))
                self.connection.commit()

                # Format the comment with member's name
                formatted_comment = f"{comment} - {member_name}"

                # Add the formatted comment to the comment table
                self.comment_table.insert(END, formatted_comment)

                # Clear the entry fields after adding the comment
                self.name_entry.delete(0, END)
                self.comment_entry.delete("1.0", "end")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add comment: {e}")
        else:
            messagebox.showwarning("Warning", "Please enter member's name and your comment.")

    def retrieve_comments(self):
        try:
            query = "SELECT member_name, comment_text FROM comments"
            self.cursor.execute(query)
            comments = self.cursor.fetchall()

            for comment in comments:
                formatted_comment = f"{comment[0]}: {comment[1]}"
                self.comment_table.insert(END, formatted_comment)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve comments: {e}")

FeedbackMember()