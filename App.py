
####    and make the system look presentable(add one extra visulisation) and add multiple users to the system including registration, and add commenets


from tkinter import *
from tkinter import StringVar
import sqlite3
from datetime import datetime
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import font


def show_frame(frame):
    login_frame.pack_forget()
    front_page.pack_forget()
    moneyIn_frame.pack_forget()
    moneyOut_frame.pack_forget()
    budget_frame.pack_forget()
    report_frame.pack_forget()
    summary_frame.pack_forget()
    frame.pack(fill='both', expand=True)

def money_in_dispaly():
    window.geometry("480x240")
    show_frame(moneyIn_frame)

def front_page_display():
    window.geometry("320x440")
    show_frame(front_page)

def log_in_display():
    window.geometry("300x400")
    show_frame(login_frame)

def show_money_out_display():
    window.geometry("320x300")
    show_frame(moneyOut_frame)



def login():
    totalspent = 0
    username = my_entry1.get()
    password = my_entry2.get()

    cursor.execute("SELECT budget_set FROM budget")
    data=cursor.fetchall()
    cursor.execute("SELECT Amount FROM money_out")
    data1=cursor.fetchall()
    for line1 in data:
        number_str = line1[0]
        stored_budget = int(number_str.replace(",", ""))
    for line in data1:
        spent = line[0]
        amount_spent = int(spent.replace(",", ""))
        totalspent += amount_spent
    
    remain = stored_budget - totalspent

    cursor.execute("select username, password from Users")
    rows = cursor.fetchall()

    for row in rows:
        if username == row[0] and password == row[1]:
            window.geometry("320x440")
            show_frame(front_page)
            if remain <=(remain * 0.15):
                budget_front_page_label.config(text=" Warning: Your are about to reach your budget ", fg= "red")
            error_label.config(text="")
            my_entry1.delete(0, END)
            my_entry2.delete(0, END)
        
        else:
            error_label.config(text = "Worng Username or password")


def money_in(): 
    time = datetime.now()

    entered_amount = my_entry3.get()
    selected_value = selected_sourceOption.get()
    current_time = time.replace(microsecond=0)
    id = "42"

    data = (entered_amount, selected_value, current_time, id)
    cursor.execute("INSERT INTO money_in (Amount, source, date_and_Time, Id) VALUES (?, ?, ?, ?)", data)
    connection.commit()
    moneyin_message.config(text = "The amount have been successfully registered")

def money_out(): 
    time = datetime.now()
    current_time = time.replace(microsecond=0)
    entered_amount = my_entry.get()
    selected_value = selected_categoryOption.get()
    selected_value1 = selected_meansOption.get()
    id = "48"

    data = (entered_amount, selected_value1, selected_value, current_time, id)
    cursor.execute("INSERT INTO money_out ( amount, transcation_means, category, date_and_Time, Id) VALUES (?, ?, ?,?, ?)", data)
    connection.commit()
    moneyout_message.config(text = "The amount have been successfully registered")
    

def setBudget():
    budget_entered = budget_entry.get()
    Id_entered = 34
    data = (Id_entered, budget_entered)
    cursor.execute("INSERT INTO budget (Id, budget_set) VALUES (?,?)", data)
    connection.commit()
    budget_message.config(text = "The Budget has been registered successully")


def show_report():
    Sday = selected_day.get()
    Smonth = selected_month.get()
    Syear = selected_year.get()

    Eday = selected_day1.get()
    Emonth = selected_month1.get()
    Eyear = selected_year1.get()

    start_date =  f"{Syear}-{int(Smonth):02d}-{int(Sday):02d}"
    end_date = f"{Eyear}-{int(Emonth):02d}-{int(Eday):02d}"
    statement = "SELECT MI.Amount,MI.source, MI.date_and_time, MO.Amount, MO.transcation_means, MO.category, MO.date_and_time  FROM money_in MI JOIN money_out MO ON MI.id == MO.id"
    cursor.execute(statement)
    data=cursor.fetchall()

    # Define sample data for the tables
    money_in_data = []
    money_out_data = []
    totalIn = 0
    totalOut = 0
    balance = 0

    for line in data:
        date_time1, date_time2 = line[2], line[6]
        stores_start_date_in = date_time1.split()[0]
        stored_start_date_out = date_time2.split()[0]
        if stores_start_date_in >= start_date and stores_start_date_in <= end_date:
            money_in_data.append(line[:3])
        if  stored_start_date_out  >= start_date and stored_start_date_out  <= end_date:
            money_out_data.append(line[3:])

        number_str = line[0]
        number_str1 = line[3]
        number = int(number_str.replace(",", ""))
        number1 = int(number_str1.replace(",", ""))
        totalIn += number
        totalOut += number1
    
    balance = totalIn - totalOut

    In_columns = ["Amount", "source", "date"]
    Out_columns = ["Amount", "transaction_means", "category", "date"]

    def create_table(parent, title, data, cl, position_column):
        frame = Frame(parent)
        frame.grid(row=5, column=position_column)
        label = Label(frame, text=title, font=("Arial", 14, "bold"))
        label.grid(row=0, column=0)
        tree = ttk.Treeview(frame, columns=cl, show="headings", height=10)
        tree.grid(row=1, column=0)
        for col in cl:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        for row in data:
            tree.insert("", "end", values=row)

        return tree
    balance_label_money.config(text = balance)
    money_in_table = create_table(report_frame, "Money In", money_in_data, In_columns, 0)
    money_out_table = create_table(report_frame, "Money Out", money_out_data, Out_columns, 3)

def visualisation():
    Sday1 = summary_entry1.get()
    Smonth1 = summary_entry2.get()
    Syear1 = summary_entry3.get()

    Eday1 = summary_entry4.get()
    Emonth1 = summary_entry5.get()
    Eyear1 = summary_entry6.get()

    def create_chart (parent,Amounts, categories):
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(Amounts,labels=categories, autopct='%1.1f%%', textprops={'fontsize': 5})
        ax.set_title('Expenditure Pie Chart')

        canvas = FigureCanvasTkAgg(fig, master=summary_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0)
    
    start_date =  f"{Syear1}-{int(Smonth1):02d}-{int(Sday1):02d}"
    end_date = f"{Eyear1}-{int(Emonth1):02d}-{int(Eday1):02d}"
    statement = "SELECT  Amount , category , date_and_time from money_out "
    cursor.execute(statement)
    data = cursor.fetchall()

    categories = []
    Amounts = []
    
    for line in data:
        date_and_time_set = line[2].split()[0]
        if date_and_time_set >= start_date and date_and_time_set <= end_date:
            amount = line[0]
            number = amount.replace(",", "")
        if line[1] not in categories:
            Amounts.append(int(number))
            categories.append(line[1])
        else: 
            index = categories.index(line[1])
            Amounts[index] += int(number)

    create_chart(window, Amounts, categories)
            



connection = sqlite3.connect('Mobile_app.db')    
cursor = connection.cursor()

window = Tk()
window.title("Finance Tracker App")
window.geometry("300x400")

###########################################logIn frame ########################################################################################
# create frames to be used in the login section
login_frame = Frame(window, bg="white")
login_label_frame = Frame(login_frame, bg="white")
second_frame =Frame(login_frame, bg="white")
center_frame = Frame(login_frame, bg="white")
bottom_frame = Frame(login_frame, bg="white")

# create the labels to be used in the login frame
my_label1 = Label(login_label_frame, text="Login", bg="white")
my_label1.config(font=("Helvetica", 25, "bold"))
label_create_accout = Label( second_frame, text="Need an account?", bg="white")
label_create_accout1 = Label( second_frame, text="Create an account", fg="Teal", bg="white")
label_create_accout1.config(font=("Helvetica", 10, "underline"))
my_label2 = Label(center_frame, text="Username", bg="white")
my_label2.config(font=("Helvetica", 10, "bold"))
my_label3 = Label(center_frame, text="Password", bg="white")
my_label3.config(font=("Helvetica", 10,"bold"))
error_label = Label(center_frame, text="", fg="red", bg="white")
forgot_label = Label(bottom_frame, text="Forgot username?", fg="Teal", bg="white")
forgot_label.config(font=("Helvetica", 10, "underline"))
forgot_label1 = Label(bottom_frame, text="Forgot password?", fg="Teal", bg="white")
forgot_label1.config(font=("Helvetica", 10, "underline"))

# create the entries to be used in the login frame
my_entry1 = Entry(center_frame, borderwidth=1, relief="solid", highlightbackground="white")
my_entry2 = Entry(center_frame, show='*', borderwidth=0.5, relief="solid", highlightbackground="white")

#create the button to be used in the login frame
my_button = Button(center_frame, text="LogIn", highlightbackground="white", command=login)

# pack the frames
login_label_frame.pack() 
second_frame.pack()
center_frame.pack()
bottom_frame.pack()
login_frame.pack()

# grid the labels
my_label1.pack(pady=10)
label_create_accout.grid(row=0, column=0, pady=20)
label_create_accout1.grid(row=0, column=1)
my_label2.grid(row=1, column=0)
my_label3.grid(row=3, column=0)
forgot_label.grid(row=0,column=0, pady=15, padx=10)
forgot_label1.grid(row=0,column=1, pady=15, padx=10)
error_label.grid(row=6, column=0)

# grid the entries
my_entry1.grid(row=2, column=0, ipadx=30, ipady=4)
my_entry2.grid(row=4, column=0, ipadx=30, ipady=4)

#  grid the button
my_button.grid(row=5, column=0, ipady=7, ipadx=15, pady=10)


####################################### front page frame #################################################################################
# frames to be used
front_page = Frame(window, bg="white")
upper_frame = Frame(front_page, bg="white")
budget_frame = Frame(front_page, bg="white")
center_frame= Frame(front_page, bg="white")

# labes to be used
my_label4 = Label(upper_frame, text="Select what action you want to do", bg="white")
budget_front_page_label = Label(budget_frame, text="", bg="white")

# buttons 
my_button1 = Button(center_frame, text="MoneyIn", highlightbackground="white", command= money_in_dispaly)
my_button2 = Button(center_frame, text="MoneyOut", highlightbackground="white",command= show_money_out_display)
my_button3 = Button(center_frame, text="Set Budget", highlightbackground="white",command=lambda: show_frame(budget_frame) )
my_button4 = Button(center_frame, text="Transcation Report", highlightbackground="white",command=lambda: show_frame(report_frame))
my_button5 = Button(center_frame, text="Transcation Summary",highlightbackground="white",command=lambda: show_frame(summary_frame))
my_button6 = Button(center_frame, text="LogOut",highlightbackground="white",command=log_in_display)

# grid labels, and buttons
my_label4.grid(row=0, column=0)
budget_front_page_label.grid(row=0, column=0)
my_button1.grid(row=0, column=0, ipady=7, ipadx=15, pady=10)
my_button2.grid(row=1, column=0, ipady=7, ipadx=15, pady=10)
my_button3.grid(row=2, column=0, ipady=7, ipadx=15, pady=10)
my_button4.grid(row=3, column=0, ipady=7, ipadx=15, pady=10)
my_button5.grid(row=4, column=0, ipady=7, ipadx=15, pady=10)
my_button6.grid(row=5, column=0, ipady=7, ipadx=15, pady=10)

# pack frames
upper_frame.pack()
budget_frame.pack()
center_frame.pack()
front_page.pack()

#######################################moneyIn_Frame########################################################################################
# the section for adding money
# frames
moneyIn_frame = Frame(window)
up_frame = Frame(moneyIn_frame)
middle_frame = Frame(moneyIn_frame)
button_frame = Frame(moneyIn_frame)

# labels
my_label5 = Label(up_frame, text="Enter the Amount of money you earned")
my_label5.config(font=("Helvetica", 10, "bold"))
source_label = Label(middle_frame, text="Source:")
source_label.config(font=("Helvetica", 10, "bold"))
moneyin_message = Label(button_frame, text="", fg='green')

# drop down
selected_sourceOption = StringVar()
selected_sourceOption.set("Select an option") 
options = ["Income", "Family help", "business profit"]
source_dropdown = OptionMenu(middle_frame, selected_sourceOption, *options)

# Entries
my_entry3 = Entry(up_frame, borderwidth=1, relief="solid")

# buttons
my_button7 = Button(button_frame, text="Enter", command= money_in)
my_button8 = Button(button_frame, text="Back", command= front_page_display)


# Grid label
my_label5.grid(row=0, column=0, pady=20)
source_label.grid(row=0,column=0)
moneyin_message.grid(row=1, column=0)

# Grid drop_down
source_dropdown.grid(row=0,column=1)

# Grid entry
my_entry3.grid(row=1,column=0, ipadx=30, ipady=4)

# Grid Button
my_button7.grid(row=0, column=0, ipady=7, ipadx=15, padx=20)
my_button8.grid(row=0, column=1, ipady=7, ipadx=15)

# Pack Frames
up_frame.pack()
middle_frame.pack(pady=20)
button_frame.pack()
moneyIn_frame.pack()

###################### MoneyOut_Frame ######################################################################################################################

moneyOut_frame = Frame(window)
first_frame = Frame(moneyOut_frame)
second_frame = Frame(moneyOut_frame)
button_frame = Frame(moneyOut_frame)
last_frame = Frame(moneyOut_frame)

my_label5 = Label(first_frame, text="Enter the Amount of money you spent")
my_label5.config(font=("Helvetica", 10, "bold"))
my_entry = Entry(first_frame, borderwidth=1, relief="solid")

my_label6 = Label(second_frame, text="Transaction means")
my_label6.config(font=("Helvetica", 10, "bold"))
selected_meansOption = StringVar()
selected_meansOption.set("Select an option") 
options = ["Mobile Money", "Bank Transfer", "Credit/Debit card", "Cash"]
dropdown = OptionMenu(second_frame, selected_meansOption, *options)

my_label7 = Label(second_frame, text="Category")
my_label7.config(font=("Helvetica", 10, "bold"))
selected_categoryOption = StringVar()
selected_categoryOption.set("Select an option") 
options = ["Entertainment", "Groceries", "Transportation", "Work"]
dropdown1 = OptionMenu(second_frame, selected_categoryOption, *options)

my_button9 = Button(button_frame, text="Enter", command=money_out)
back_button = Button(button_frame, text="Back", command=front_page_display)
moneyout_message = Label(last_frame, text="", fg='green')

### add a sub category
my_label5.grid(row=0, column=0, pady=20)
my_entry.grid(row=1, column=0, ipadx=30, ipady=4)
my_label6.grid(row=0, column=0, pady=20)
dropdown.grid(row=0, column=1)
my_label7.grid(row=1, column=0)
dropdown1.grid(row=1, column=1)
my_button9.grid(row=0, column=0, ipady=7, ipadx=15, padx=20)
back_button.grid(row=0, column=1, ipady=7, ipadx=15)
moneyout_message.grid(row=0, column=0)

first_frame.pack()
second_frame.pack()
button_frame.pack(pady=20)
last_frame.pack()
moneyOut_frame.pack()

##################### set Budget frame########################################################
budget_frame = Frame(window)

budget_label = Label(budget_frame, text="Enter Your monthly")
budget_entry = Entry(budget_frame, placeholder="Enter the Amount")

budget_button = Button(budget_frame, text="Enter",command=setBudget)
budget_button1 = Button(budget_frame, text="Back", command= lambda: show_frame(front_page))
budget_message = Label(budget_frame, text="", fg='green')

budget_label.grid(row=0, column=0)
budget_entry.grid(row=1, column=0)
budget_button.grid(row=4, column=0)
budget_button1.grid(row=4, column=1)
budget_message.grid(row=6, column=0)

budget_frame.pack()

################################### transcaction Report #############################################

report_frame = Frame(window)
report_label = Label(report_frame, text="Enter the time gap you want your report to be in")
report_label1 = Label(report_frame, text="Start From:")


selected_day = StringVar()
selected_day.set("dd") 
day_options = ["1", "2", "3", "4", "5", "6", "7", "8", 
           "9", "10", "11", "12", "13", "14", "15", 
           "16", "17", "18", "19", "20", "21", "22", 
           "23", "24", "25", "26", "27", "28", "29", "30"]
day_dropdown = OptionMenu(report_frame, selected_day, *day_options)
day_dropdown.grid(row=1,column=1)

selected_month = StringVar()
selected_month.set("mm") 
month_options = ["1", "2", "3", "4", "5", "6", "7", "8", 
           "9", "10", "11", "12"]
month_dropdown = OptionMenu(report_frame, selected_month, *month_options)
month_dropdown.grid(row=1,column=2)

selected_year = StringVar()
selected_year.set("yyy") 
year_options = ["2020", "2021", "2022", "2023", "2024", "2025"]
year_dropdown = OptionMenu(report_frame, selected_year, *year_options)
year_dropdown.grid(row=1,column=3)


report_label5 = Label(report_frame, text="Until:")

selected_day1 = StringVar()
selected_day1.set("dd") 
day_options1 = ["1", "2", "3", "4", "5", "6", "7", "8", 
           "9", "10", "11", "12", "13", "14", "15", 
           "16", "17", "18", "19", "20", "21", "22", 
           "23", "24", "25", "26", "27", "28", "29", "30"]
day_dropdown1 = OptionMenu(report_frame, selected_day1, *day_options1)
day_dropdown1.grid(row=2,column=1)

selected_month1 = StringVar()
selected_month1.set("mm") 
month_options1 = ["1", "2", "3", "4", "5", "6", "7", "8", 
           "9", "10", "11", "12"]
month_dropdown1 = OptionMenu(report_frame, selected_month1, *month_options1)
month_dropdown1.grid(row=2,column=2)

selected_year1 = StringVar()
selected_year1.set("yyy") 
year_options1 = ["2020", "2021", "2022", "2023", "2024", "2025"]
year_dropdown1 = OptionMenu(report_frame, selected_year1, *year_options1)
year_dropdown1.grid(row=2,column=3)



report_button = Button(report_frame, text="Display", command=show_report)
report_button1 = Button(report_frame, text="Back",  command= lambda: show_frame(front_page))
balance_label = Label(report_frame, text="Balance")
balance_label_money = Label(report_frame, text="")


report_label.grid(row=0, column=0)
report_label1.grid(row=1, column=0)
report_label5.grid(row=2, column=0)
report_button.grid(row=3,column=0)
report_button1.grid(row=3,column=1)
balance_label.grid(row=4, column=0)
balance_label_money.grid(row=4, column=1)


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

summary_button = Button(summary_frame, text="Display", command=visualisation)
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
summary_entry6.grid(row=2, column=6)

summary_button.grid(row=3,column=0)
summary_button1.grid(row=3,column=1)

summary_frame.pack()

######################################################################################
show_frame(login_frame)

window.mainloop()

###############