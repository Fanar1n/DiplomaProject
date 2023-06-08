import telebot
import Employee
import Detail

bot = telebot.TeleBot("6104580443:AAGtmGn996paSF2TTiXxcboDC-R4jPtYqr4")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Выберите пункт из меню что вы хотите сделать')
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    employeeButton = telebot.types.KeyboardButton("1")
    detailsButton = telebot.types.KeyboardButton("2")
    keyboard.add(employeeButton,detailsButton)
    bot.send_message(message.chat.id, "1.Сотрудники"
                     "\n2. Детали", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '1':
        Employee.EmployeeMenu(message,bot)
    elif message.text == '2':
        Detail.DetailsMenu(message,bot)
    else:
        start_message(message)


bot.polling()