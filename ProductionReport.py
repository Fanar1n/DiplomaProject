import telebot
import sqlite3


conn = sqlite3.connect('db/ZagoskyDB.db', check_same_thread=False)
cursor = conn.cursor()


details = ['Detail_Name','Name_DCE','Workshop','Number_Of_Details']


def db_details_val(Detail_Name: str,Name_DCE: str,Workshop: int,Number_Of_Details: int):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Details (Detail_Name,Name_DCE,Workshop,Number_Of_Details) VALUES (?,?,?,?)', (Detail_Name,Name_DCE,Workshop,Number_Of_Details))
    conn.commit()
    cursor.close()


def ProductionReportMenu(message,bot):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    addProductionReportYear = telebot.types.KeyboardButton("1")
    addDetailButton = telebot.types.KeyboardButton("2")
    findDetailButton = telebot.types.KeyboardButton("3")
    backButton = telebot.types.KeyboardButton("Назад")
    keyboard.add(showDetailsButton, addDetailButton, findDetailButton,backButton)
    bot.send_message(message.chat.id, 'Выберите пункт меню:')
    bot.send_message(message.chat.id, "\n1. Показать отчёт предприятия за год"
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