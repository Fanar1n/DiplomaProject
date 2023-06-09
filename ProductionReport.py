import datetime

import telebot
import sqlite3
import datetime


conn = sqlite3.connect('db/ZagoskyDB.db', check_same_thread=False)


productionReportYear = ['Total_Details_Produced','Total_Employees','Year','Avg_Dateails_Per_Employee','Date_Created_Report']


def db_YEARreport_val(Total_Details_Produced: int,Total_Employees: int,Year: int,Avg_Dateails_Per_Employee: float,Date_Created_Report: datetime.date):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Details (Total_Details_Produced,Total_Employees,Year,Avg_Dateails_Per_Employee,Date_Created_Report) VALUES (?,?,?,?,?)', (Total_Details_Produced,Total_Employees,Year,Avg_Dateails_Per_Employee,Date_Created_Report))
    conn.commit()
    cursor.close()


def ProductionReport(message,bot):
    cursor = conn.cursor()
    query = "SELECT SUM(Number_Of_Details) FROM Details"
    cursor.execute(query)
    result1 = cursor.fetchone()
    cursor.close()

    productionReportYear[0] = result1[0]

    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM Employees"
    cursor.execute(query)
    result2 = cursor.fetchone()
    cursor.close()

    productionReportYear[1] = result2[0]

    productionReportYear[2]=datetime.datetime.now().year
    AVG = result1[0]/result2[0]
    productionReportYear[3]=AVG
    productionReportYear[4]=datetime.datetime.now().date()

    bot.send_message(message.chat.id, "Отчёт за год:")

    details_info = f"Год: {productionReportYear[2]}\nОбщеее количество деталей за год: {result1[0]}\nОбщее количество работающих сотрудников: {productionReportYear[1]}\nСреднее количество деталей на человека: {productionReportYear[3]}\nДата создания отчёта: {productionReportYear[4]}"
    bot.send_message(message.chat.id, details_info)

    bot.send_message(message.chat.id, "/start")

def asads(message,bot):
    result1 = 2
    result2 = 1
    AVG = result1 / result2
    productionReportYear[3] = AVG
    productionReportYear[4] = datetime.date

    db_YEARreport_val(Total_Details_Produced=productionReportYear[0], Total_Employees=productionReportYear[1],
                      Year=productionReportYear[2], Avg_Dateails_Per_Employee=productionReportYear[3],
                      Date_Created_Report=productionReportYear[4])

    bot.send_message(message.chat.id, "Отчёт за год")

    details_info = f"Год: {productionReportYear[2]}\nОбщеее количество деталей за год: {productionReportYear[0]}\nОбщее количество работающих сотрудников: {productionReportYear[1]}\nСреднее количество деталей на человека: {productionReportYear[3]}\nДата создания отчёта: {productionReportYear[4]}"
    bot.send_message(message.chat.id, details_info)

    bot.send_message(message.chat.id, "/start")