
#### do the visualisation and add multiple users to the system including registration, and make the system look presentable


from tkinter import *
from tkinter import StringVar
import sqlite3
from datetime import datetime
from tkinter import ttk


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
            show_frame(front_page)
            budget_front_page_label.config(text= "the budget you set is:"+ stored_budget +","+" you have:"+ str(remain) + "left to reach your budget limit")
            if remain <=(remain * 0.15):
                budget_front_page_label.config(fg = 'red')
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
    id = "34"

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
    id = "34"

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





connection = sqlite3.connect('Mobile_app.db')    
cursor = connection.cursor()

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
error_label = Label(login_frame, text="", fg='red')
    
my_label1.grid(row=0, column=0)
my_label2.grid(row=1, column=0)
my_label3.grid(row=3, column=0)
my_entry1.grid(row=2, column=0)
my_entry2.grid(row=4, column=0)
my_button.grid(row=5, column=0)
error_label.grid(row=6, column=0)

login_frame.pack()

#######################################moneyIn_Frame#######################################

moneyIn_frame = Frame(window)

my_label5 = Label(moneyIn_frame, text="Enter the Amount of money you earned")
my_entry3 = Entry(moneyIn_frame, placeholder = "Enter the amount")
moneyin_message = Label(moneyIn_frame, text="", fg='green')

source_label = Label(moneyIn_frame, text="Source:")
selected_sourceOption = StringVar()
selected_sourceOption.set("Select an option") 
options = ["Income", "Family help", "business profit"]
source_dropdown = OptionMenu(moneyIn_frame, selected_sourceOption, *options)

my_button7 = Button(moneyIn_frame, text="Enter", command= money_in)
my_button8 = Button(moneyIn_frame, text="Back", command= lambda: show_frame(front_page))

my_label5.grid(row=0, column=0)
my_entry3.grid(row=1,column=0)
source_label.grid(row=2,column=0)
source_dropdown.grid(row=2,column=1)
my_button7.grid(row=3, column=0)
my_button8.grid(row=3, column=1)
moneyin_message.grid(row=4, column=0)

moneyIn_frame.pack()

####################################### front page frame ##############################
front_page = Frame(window)

my_label4 = Label(front_page, text="Select what action you want to do")
budget_front_page_label = Label(front_page, text="", fg='green')

my_button1 = Button(front_page, text="MoneyIn", command=lambda: show_frame(moneyIn_frame))
my_button2 = Button(front_page, text="MoneyOut", command=lambda: show_frame(moneyOut_frame))
my_button3 = Button(front_page, text="Set Budget",command=lambda: show_frame(budget_frame) )
my_button4 = Button(front_page, text="Transcation Report", command=lambda: show_frame(report_frame))
my_button5 = Button(front_page, text="Transcation Summary", command=lambda: show_frame(summary_frame))
my_button6 = Button(front_page, text="LogOut", command=lambda: show_frame(login_frame))


my_label4.grid(row=0, column=0)
budget_front_page_label.grid(row=1, column=0)
my_button1.grid(row=2, column=0)
my_button2.grid(row=3, column=0)
my_button3.grid(row=4, column=0)
my_button4.grid(row=5, column=0)
my_button5.grid(row=6, column=0)
my_button6.grid(row=7, column=0)


front_page.pack()

###################### MoneyOut_Frame ##################

moneyOut_frame = Frame(window)

my_label5 = Label(moneyOut_frame, text="Enter the Amount of money you spent")
my_entry = Entry(moneyOut_frame, placeholder="Enter Amount")

my_label6 = Label(moneyOut_frame, text="transaction means")
selected_meansOption = StringVar()
selected_meansOption.set("Select an option") 
options = ["Mobile Money", "Bank Transfer", "Credit/Debit card", "Cash"]
dropdown = OptionMenu(moneyOut_frame, selected_meansOption, *options)

my_label7 = Label(moneyOut_frame, text="Category")
selected_categoryOption = StringVar()
selected_categoryOption.set("Select an option") 
options = ["Entertainment", "Groceries", "Transportation", "Work"]
dropdown1 = OptionMenu(moneyOut_frame, selected_categoryOption, *options)

my_button9 = Button(moneyOut_frame, text="Enter", command=money_out)
back_button = Button(moneyOut_frame, text="Back", command= lambda: show_frame(front_page))
moneyout_message = Label(moneyOut_frame, text="", fg='green')

### add a sub category
my_label5.grid(row=0, column=0)
my_entry.grid(row=1, column=0)
my_label6.grid(row=2, column=0)
dropdown.grid(row=2, column=1)
my_label7.grid(row=3, column=0)
dropdown1.grid(row=3, column=1)
my_button9.grid(row=4, column=0)
back_button.grid(row=4, column=1)
moneyout_message.grid(row=5, column=0)

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