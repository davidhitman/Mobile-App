
from tkinter import *
from tkinter import StringVar


def show_frame(frame):
    login_frame.pack_forget()
    front_page.pack_forget()
    moneyIn_frame.pack_forget()
    moneyOut_frame.pack_forget()
    budget_frame.pack_forget()
    report_frame.pack_forget()
    summary_frame.pack_forget()
    frame.pack(fill='both', expand=True)


def login():
    username = my_entry1.get()
    password = my_entry2.get()

    if username == "dav" and password == "123":
        show_frame(front_page)
        my_entry1.delete(0, END)
        my_entry2.delete(0, END)
    else:
        print(22)


            
window = Tk()
window.title("Finance Tracker App")
window.geometry("300x200")

###########################################logIn frame #####################################
login_frame = Frame(window)

my_label1 = Label(login_frame, text="Login")
my_label2 = Label(login_frame, text="Username")
my_label3 = Label(login_frame, text="Password")
my_entry1 = Entry(login_frame, placeholder = "Enter your username")
my_entry2 = Entry(login_frame, placeholder = "Enter your password", show='*')

my_button = Button(login_frame, text="LogIn", command=login)
    
my_label1.grid(row=0, column=0)
my_label2.grid(row=1, column=0)
my_label3.grid(row=3, column=0)
my_entry1.grid(row=2, column=0)
my_entry2.grid(row=4, column=0)
my_button.grid(row=5, column=0)

login_frame.pack()

#######################################moneyIn_Frame#######################################

moneyIn_frame = Frame(window)

my_label5 = Label(moneyIn_frame, text="Enter the Amount of money you earned")
my_entry3 = Entry(moneyIn_frame, placeholder = "Enter the amount")
my_button7 = Button(moneyIn_frame, text="Enter")
my_button8 = Button(moneyIn_frame, text="Back", command= lambda: show_frame(front_page))

my_label5.grid(row=0, column=0)
my_entry3.grid(row=1,column=0)
my_button7.grid(row=2, column=0)
my_button8.grid(row=2, column=1)

moneyIn_frame.pack()

####################################### front page frame ##############################
front_page = Frame(window)

my_label4 = Label(front_page, text="Select what action you want to do")

my_button1 = Button(front_page, text="MoneyIn", command=lambda: show_frame(moneyIn_frame))
my_button2 = Button(front_page, text="MoneyOut", command=lambda: show_frame(moneyOut_frame))
my_button3 = Button(front_page, text="Set Budget",command=lambda: show_frame(budget_frame) )
my_button4 = Button(front_page, text="Transcation Report", command=lambda: show_frame(report_frame))
my_button5 = Button(front_page, text="Transcation Summary", command=lambda: show_frame(summary_frame))
my_button6 = Button(front_page, text="LogOut", command=lambda: show_frame(login_frame))

my_label4.grid(row=0, column=0)
my_button1.grid(row=1, column=0)
my_button2.grid(row=2, column=0)
my_button3.grid(row=3, column=0)
my_button4.grid(row=4, column=0)
my_button5.grid(row=5, column=0)
my_button6.grid(row=6, column=0)

front_page.pack()

###################### MoneyOut_Frame ##################

moneyOut_frame = Frame(window)

my_label5 = Label(moneyOut_frame, text="Enter the Amount of money you spent")
my_entry = Entry(moneyOut_frame)

my_label6 = Label(moneyOut_frame, text="transaction means")
selected_option = StringVar()
selected_option.set("Select an option") 
options = ["Mobile Money", "Bank Transfer", "Credit/Debit card", "Cash"]
dropdown = OptionMenu(moneyOut_frame, selected_option, *options)

my_label7 = Label(moneyOut_frame, text="Category")
selected_option = StringVar()
selected_option.set("Select an option") 
options = ["Entertainment", "Groceries", "Transportation", "Work"]
dropdown1 = OptionMenu(moneyOut_frame, selected_option, *options)

my_button9 = Button(moneyOut_frame, text="Enter")
back_button = Button(moneyOut_frame, text="Back", command= lambda: show_frame(front_page))

### add a sub category
my_label5.grid(row=0, column=0)
my_entry.grid(row=1, column=0)
my_label6.grid(row=2, column=0)
dropdown.grid(row=2, column=1)
my_label7.grid(row=3, column=0)
dropdown1.grid(row=3, column=1)
my_button9.grid(row=4, column=0)
back_button.grid(row=4, column=1)

moneyOut_frame.pack()

##################### set Budget frame########################################################
budget_frame = Frame(window)

budget_label = Label(budget_frame, text="Enter the Budget you want to set")
budget_entry = Entry(budget_frame, placeholder="Enter the Amount")
budget_button = Button(budget_frame, text="Enter")
budget_button1 = Button(budget_frame, text="Back", command= lambda: show_frame(front_page))

budget_label.grid(row=0, column=0)
budget_entry.grid(row=1, column=0)
budget_button.grid(row=2, column=0)
budget_button1.grid(row=2, column=1)

budget_frame.pack()

################################### transcaction Report #############################################

report_frame = Frame(window)

report_label = Label(report_frame, text="Enter the time gap you want your report to be in")

report_label1 = Label(report_frame, text="Start From:")
report_label2 = Label(report_frame, text="dd")
report_label3 = Label(report_frame, text="mm")
report_label4 = Label(report_frame, text="yyyy")

report_entry1 = Entry(report_frame, width=2)
report_entry2 = Entry(report_frame, width=2)
report_entry3 = Entry(report_frame, width=2)

report_label5 = Label(report_frame, text="Until:")
report_label6 = Label(report_frame, text="dd")
report_label7 = Label(report_frame, text="mm")
report_label8 = Label(report_frame, text="yyyy")

report_entry4 = Entry(report_frame, width=2)
report_entry5 = Entry(report_frame, width=2)
report_entry6 = Entry(report_frame, width=2)

report_button = Button(report_frame, text="Display")
report_button1 = Button(report_frame, text="Back",  command= lambda: show_frame(front_page))


report_label.grid(row=0, column=0)
report_label1.grid(row=1, column=0)
report_label2.grid(row=1, column=1)
report_entry1.grid(row=1, column=2)
report_label3.grid(row=1, column=3)
report_entry2.grid(row=1, column=4)
report_label4.grid(row=1, column=5)
report_entry3.grid(row=1, column=6)

report_label5.grid(row=2, column=0)
report_label6.grid(row=2, column=1)
report_entry4.grid(row=2,column=2)
report_label7.grid(row=2, column=3)
report_entry5.grid(row=2, column=4)
report_label8.grid(row=2, column=5)
report_entry5.grid(row=2, column=6)

report_button.grid(row=3,column=0)
report_button1.grid(row=3,column=1)


report_frame.pack()
################################### transcaction Summary #############################################

summary_frame = Frame(window)

summary_label = Label(summary_frame, text="Enter the time gap you want your summary to be in")

summary_label1 = Label(summary_frame, text="Start From:")
summary_label2 = Label(summary_frame, text="dd")
summary_label3 = Label(summary_frame, text="mm")
summary_label4 = Label(summary_frame, text="yyyy")

summary_entry1 = Entry(summary_frame, width=2)
summary_entry2 = Entry(summary_frame, width=2)
summary_entry3 = Entry(summary_frame, width=2)

summary_label5 = Label(summary_frame, text="Until:")
summary_label6 = Label(summary_frame, text="dd")
summary_label7 = Label(summary_frame, text="mm")
summary_label8 = Label(summary_frame, text="yyyy")

summary_entry4 = Entry(summary_frame, width=2)
summary_entry5 = Entry(summary_frame, width=2)
summary_entry6 = Entry(summary_frame, width=2)

summary_button = Button(summary_frame, text="Display")
summary_button1 = Button(summary_frame, text="Back",  command= lambda: show_frame(front_page))

summary_label.grid(row=0, column=0)
summary_label1.grid(row=1, column=0)
summary_label2.grid(row=1, column=1)
summary_entry1.grid(row=1, column=2)
summary_label3.grid(row=1, column=3)
summary_entry2.grid(row=1, column=4)
summary_label4.grid(row=1, column=5)
summary_entry3.grid(row=1, column=6)

summary_label5.grid(row=2, column=0)
summary_label6.grid(row=2, column=1)
summary_entry4.grid(row=2,column=2)
summary_label7.grid(row=2, column=3)
summary_entry5.grid(row=2, column=4)
summary_label8.grid(row=2, column=5)
summary_entry5.grid(row=2, column=6)

summary_button.grid(row=3,column=0)
summary_button1.grid(row=3,column=1)

summary_frame.pack()

######################################################################################
show_frame(login_frame)

window.mainloop()

###############