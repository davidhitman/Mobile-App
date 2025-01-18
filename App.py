
from tkinter import *

class App(Tk):
    def __init__ (self):
        super().__init__ ()

        def login():
            username = my_entry1.get()
            password = my_entry2.get()

            if username == "dav" and password == "123":
                print(11)
            else:
                print(22)
            
            self.login_frame.configure('disable')

        self.title("Finance Tracker App")
        self.geometry("300x200")

        self.login_frame = Frame(self)

        my_label1 = Label(self.login_frame, text="Login")

        my_label2 = Label(self.login_frame, text="Username")
        my_label3 = Label(self.login_frame, text="Password")
        my_entry1 = Entry(self.login_frame, placeholder = "Enter your username")
        my_entry2 = Entry(self.login_frame, placeholder = "Enter your password")
        my_button = Button(self.login_frame, text="LogIn", command=login)
    
        my_label1.grid(row=0, column=0)
        my_label2.grid(row=1, column=0)
        my_label3.grid(row=3, column=0)
        my_entry1.grid(row=2, column=0)
        my_entry2.grid(row=4, column=0)
        my_button.grid(row=5, column=0)

        self.login_frame.pack()

        
if __name__ == "__main__":
    app = App()
    app.mainloop()

# continue 