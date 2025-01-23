
import sqlite3
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

window = Tk()
window.title("Finance Tracker App")
window.geometry("500x500")

connection = sqlite3.connect('Mobile_app.db')    
cursor = connection.cursor()


def create_chart (parent,Amounts, categories):

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(Amounts,labels=categories, autopct='%1.1f%%', textprops={'fontsize': 5})
    ax.set_title('Expenditure Pie Chart')

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

Sday1 = "23"
Smonth1 = "01"
Syear1 = "2025"

Eday1 = "23"
Emonth1 = "01"
Eyear1 = "2025"

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

window.mainloop()






