import telebot
import sqlite3


conn = sqlite3.connect('db/ZagoskyDB.db', check_same_thread=False)
cursor = conn.cursor()


details = ['Detail_Name','Name_DCE','Workshop','Number_Of_Details']


def db_details_val(Detail_Name: str,Name_DCE: str,Workshop: int,Number_Of_Details: int):
    cursor.execute('INSERT INTO Details (Detail_Name,Name_DCE,Workshop,Number_Of_Details) VALUES (?,?,?,?)', (Detail_Name,Name_DCE,Workshop,Number_Of_Details))
    conn.commit()


def DetailsMenu(message,bot):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    addEmployeeButton = telebot.types.KeyboardButton("1")
    editEmployeeButton = telebot.types.KeyboardButton("2")
    findEmployeeButton = telebot.types.KeyboardButton("3")
    backButton = telebot.types.KeyboardButton("Назад")
    keyboard.add(addEmployeeButton, editEmployeeButton, findEmployeeButton,backButton)
    bot.send_message(message.chat.id, 'Выберите пункт меню:')
    bot.send_message(message.chat.id, "\n1. Посмотреть все детали"
                                      "\n2. Добавить деталь"
                                      "\n3. Найти деталь"
                                      "\n4. Назад", reply_markup=keyboard)
    bot.register_next_step_handler(message, Details_Menu_Handler, bot)


def Details_Menu_Handler(message,bot):
    if message.text == '1':
        DetailsList(message,bot)
    elif message.text == '2':
        bot.send_message(message.chat.id, 'Введите название детали')
        bot.register_next_step_handler(message, get_Detail_Name,bot)
    elif message.text == '3':
        bot.send_message(message.chat.id, 'Введите название детали, которую вы хотите найти:')
        bot.register_next_step_handler(message, Find_Detail,bot)
    elif message.text == 'Назад' or message.text == '4':
        bot.send_message(message.chat.id, "/start")
    else:
        DetailsMenu(message,bot)


def Find_Detail(message,bot):
    query = "SELECT * FROM Details WHERE Detail_Name LIKE '%" + message.text.lower() + "%'"
    cursor.execute(query)
    result = cursor.fetchall()

    if len(result) == 0:
        bot.send_message(message.chat.id, f"Деталь с названием {message.text} не была найдена.")

        DetailsMenu(message,bot)
    else:
        for row in result:
            detail_id, detail_name, number_of_details = row
            details_info = f"ID: {detail_id}\nНазвание детали: {detail_name}\nКоличество деталей: {number_of_details}"
            bot.send_message(message.chat.id, details_info)

        DetailsMenu(message,bot)

def get_Detail_Name(message,bot):
    result = message.text.lower()
    details[0] = result

    bot.send_message(message.chat.id, "Введите сборочное название детали")
    bot.register_next_step_handler(message, get_Name_DCE,bot)


def get_Name_DCE(message,bot):
    result = message.text.lower()
    details[1] = result

    bot.send_message(message.chat.id, "Введите цех производства детали")
    bot.register_next_step_handler(message, get_Workshop, bot)


def get_Workshop(message,bot):
    result = message.text.lower()
    details[2] = result

    bot.send_message(message.chat.id, "Введите количество имеющихся деталей")
    bot.register_next_step_handler(message, get_Number_Of_Details, bot)


def get_Number_Of_Details(message,bot):
    result = message.text.lower()
    details[3] = result

    db_details_val(Detail_Name=details[0],Name_DCE=details[1],Workshop=details[2],Number_Of_Details=details[3])

    bot.send_message(message.chat.id, "Добавлена новая деталь: ")

    details_info = f"Наименование Детали: {details[0]}\nКоличество Деталей: {details[1]}"
    bot.send_message(message.chat.id, details_info)

    DetailsMenu(message,bot)

def DetailsList(message,bot):
    query = "SELECT Detail_ID,Detail_Name FROM Details"
    cursor.execute(query)
    result = cursor.fetchall()

    for row in result:
        detail_id, detail_name,detail_name_DCE,detail_workshop,number_of_Details = row
        detail_info = f"ID: {detail_id}\nНаименование детали: {detail_name}\nСборочное назв. детали: {detail_name_DCE}\nЦех: {detail_workshop}\nКоличество деталей: {number_of_Details}"
        bot.send_message(message.chat.id, detail_info)

    DetailsMenu(message,bot)