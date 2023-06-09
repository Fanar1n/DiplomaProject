import telebot
import sqlite3
import Employee
import Detail
import EmployeeReport


bot = telebot.TeleBot("6104580443:AAGtmGn996paSF2TTiXxcboDC-R4jPtYqr4")


conn = sqlite3.connect('db/ZagoskyDB.db', check_same_thread=False)
cursor = conn.cursor()

@bot.message_handler(commands=['start'])
def start_message(message):
    query = f"SELECT * FROM Employees WHERE Device_ID = {message.from_user.id}"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
        employeeButton = telebot.types.KeyboardButton("1")
        detailsButton = telebot.types.KeyboardButton("2")
        employeeReportButton = telebot.types.KeyboardButton("3")
        keyboard.add(employeeButton, detailsButton,employeeReportButton)
        bot.send_message(message.chat.id, "Выберите пункт из меню что вы хотите сделать"
                                          "\n1.Сотрудники"
                                          "\n2.Детали"
                                          "\n3.Отчёт сотрудника", reply_markup=keyboard)
    else:
        Employee.RegistrationEmployee(message, bot)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '1':
        Employee.EmployeeMenu(message,bot)
    elif message.text == '2':
        Detail.DetailsMenu(message,bot)
    elif message.text == '3':
        EmployeeReport.EmployeeReportMenu(message,bot)
    else:
        start_message(message)


bot.polling()