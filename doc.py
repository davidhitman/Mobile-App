

import sqlite3




def display_report():

    connection = sqlite3.connect('Mobile_app.db')    
    cursor = connection.cursor()

    Sday = 21
    Smonth = 1
    Syear = 2025

    Eday = 21
    Emonth = 1
    Eyear = 2025

    Out_data = []
    start_date =  f"{Syear}-{Smonth:02d}-{Sday:02d}"
    end_date = f"{Eyear}-{Emonth:02d}-{Eday:02d}"
    statement = "SELECT MI.Amount,MI.source, MI.date_and_time, MO.Amount, MO.transcation_means, MO.category, MO.date_and_time  FROM money_in MI JOIN money_out MO ON MI.id == MO.id"
    cursor.execute(statement)
    data=cursor.fetchall()



    for line in data:
        date_time1, date_time2 = line[2], line[6]
        stores_start_date_in = date_time1.split()[0]
        stored_start_date_out = date_time2.split()[0]
        if stores_start_date_in >= start_date and stores_start_date_in <= end_date:
            if stored_start_date_out >= start_date and stored_start_date_out <= end_date:
                Out_data = line
            else:
                Out_data = line[:3]
        elif  stored_start_date_out  >= start_date and stored_start_date_out  <= end_date:
            Out_data.append(line[3:])
        print (Out_data)
        print('david')
    
    In_columns = ["Amount", "source", "date"]
    Out_columns = ["Amount", "transaction_means", "category", "date"]




display_report()