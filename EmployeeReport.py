import telebot
import sqlite3
import Employee
import datetime



conn = sqlite3.connect('db/ZagoskyDB.db', check_same_thread=False)

report = ['Detail_ID','Amount_Of_Details','Date_report','Employee_ID']


def db_report_val(Detail_ID: int,Amount_Of_Details: int,Date_report: datetime.datetime,Employee_ID: int):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO EmployeeReport (Detail_ID,Employee_ID,Date_report,Amount_Of_Details) VALUES (?,?,?,?)', (Detail_ID,Employee_ID,Date_report,Amount_Of_Details))
    conn.commit()
    cursor.close()


def EmployeeReportMenu(message,bot):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    addCompletedWorkButton = telebot.types.KeyboardButton("1")
    showYourWorkAtDay = telebot.types.KeyboardButton("2")
    backButton = telebot.types.KeyboardButton("Назад")
    keyboard.add(addCompletedWorkButton, showYourWorkAtDay,backButton)
    bot.send_message(message.chat.id, 'Выберите пункт меню:')
    bot.send_message(message.chat.id, "\n1. Добавить выполненую работу за день"
                                      "\n2. Посмотреть кол.во выполенной работы за день"
                                      "\n3. Назад", reply_markup=keyboard)
    bot.register_next_step_handler(message, EmployeeReport_Menu_Handler, bot)


def EmployeeReport_Menu_Handler(message,bot):
    if message.text == '1':
        AddCompletedWord(message,bot)
    elif message.text == '2':
        bot.send_message(message.chat.id, 'Введите дату, чтобы посмотреть отчёт о работе в этот день(формат: год-месяц-день')
        bot.register_next_step_handler(message, ShowYourWorkAtDay, bot)
    elif message.text == 'Назад' or message.text == '3':
        bot.send_message(message.chat.id, "/start")
    else:
        EmployeeReportMenu(message,bot)


def ShowYourWorkAtDay(message,bot):
    if is_valid_date(message.text,date_format):
        cursor = conn.cursor()
        query = "SELECT * FROM EmployeeReport WHERE Date_report LIKE '%" + message.text.lower() + "%'"
        cursor.execute(query)
        result = cursor.fetchall()

        if len(result) == 0:
            bot.send_message(message.chat.id, f"Отчёт о работе в дату {message.text} не был найден.")

            EmployeeReportMenu(message, bot)
        else:
            for row in result:
                employeeReport_Id, detail_ID, employee_ID, date_report, amount_of_details = row
                report_info = f"ID: {employeeReport_Id}\nID детали: {detail_ID}\nДата внесение отчёта: {date_report}\nКоличество деталей: {amount_of_details}\n"
                bot.send_message(message.chat.id, report_info)

            cursor.close()
            EmployeeReportMenu(message, bot)
    else:
        bot.send_message(message.chat.id, 'Дата невалидна, введите дату в формате день-месяц-год ещё раз(например: 2021-03-12')
        bot.register_next_step_handler(message, ShowYourWorkAtDay, bot)

def AddCompletedWord(message,bot):
    DetailsList(message,bot)
    bot.send_message(message.chat.id, 'Введите ID детали, по который вы хотите сделать отчёт')
    bot.register_next_step_handler(message, get_ID_Of_Details, bot)


def get_ID_Of_Details(message,bot):
    result = message.text.lower()
    report[0] = result

    Detail_Id = result
    bot.send_message(message.chat.id, 'Введите количество произведённых деталей')
    bot.register_next_step_handler(message, get_Amount_Of_Details, bot,Detail_Id)


def get_Amount_Of_Details(message,bot,Details_Id):
    result = message.text.lower()
    report[1] = result
    report[2] = datetime.datetime.now()
    report[3] = message.from_user.id

    db_report_val(Detail_ID=report[0],Employee_ID=report[3],Date_report=report[2],Amount_Of_Details=report[1])

    bot.send_message(message.chat.id, "Добавлен новый отчёт по работе: ")

    amount_info = f"ID произведённой детали: {report[0]}\nКоличество произведённых деталей: {report[1]}\nВремя занесения отчёта: {report[2]}"
    bot.send_message(message.chat.id, amount_info)

    cursor = conn.cursor()
    query = f"UPDATE Details SET Number_Of_Details = Number_Of_Details + {result} WHERE Detail_ID = {Details_Id}"
    cursor.execute(query)
    conn.commit()
    cursor.close()

    EmployeeReportMenu(message, bot)

def DetailsList(message,bot):
    cursor = conn.cursor()
    query = "SELECT Detail_ID,Detail_Name FROM Details"
    cursor.execute(query)
    result = cursor.fetchall()

    for row in result:
        detail_id, detail_name = row
        detail_info = f"ID: {detail_id}\nНаименование детали: {detail_name}"
        bot.send_message(message.chat.id, detail_info)

    cursor.close()


def is_valid_date(date_string, date_format):
    try:
        datetime.datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False

# Пример использования
date_format = "%Y-%m-%d"