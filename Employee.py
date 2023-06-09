import telebot
import sqlite3

conn = sqlite3.connect('db/ZagoskyDB.db', check_same_thread=False)
cursor = conn.cursor()


colums = ['First_Name','Second_Name','Third_Name','Email','Phone_Number','Date_Of_Birth','Address','Department','Position','Hire_Date','Employment_Status','Word_Schedule','Vacation_Days','Device_ID']


def db_table_val(First_Name: str,Second_Name: str,Third_Name: str,Email: str,Phone_Number: str,Date_Of_Birth: str,Address: str,Department: str,Position: str,Hire_Date: str,Employment_Status: str,Word_Schedule : str,Vacation_Days: int, Device_ID: str):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Employees (First_Name,Second_Name,Third_Name,Email,Phone_Number,Date_Of_Birth,Address,Department,Position,Hire_Date,Employment_Status,Word_Schedule,Vacation_Days,Device_ID) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (First_Name, Second_Name, Third_Name, Email, Phone_Number, Date_Of_Birth , Address,Department,Position,Hire_Date,Employment_Status,Word_Schedule,Vacation_Days,Device_ID))
    conn.commit()
    cursor.close()


def RegistrationEmployee(message,bot):
    bot.send_message(message.chat.id, 'Вам необходимо зарегестрироваться,введите своё имя')
    bot.register_next_step_handler(message, get_First_Name, bot)


def EmployeeMenu(message,bot):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    editEmployeeButton = telebot.types.KeyboardButton("1")
    backButton = telebot.types.KeyboardButton("Назад")
    keyboard.add(editEmployeeButton, backButton)
    bot.send_message(message.chat.id, 'Выберите пункт меню:')
    bot.send_message(message.chat.id, "\n1. Найти сотрудника"
                                      "\n2. Назад", reply_markup=keyboard)
    bot.register_next_step_handler(message, Employee_Menu_Handler,bot)


def Employee_Menu_Handler(message,bot):
    if message.text == '1':
        bot.send_message(message.chat.id, 'Введите фамилию сотрудника, которого вы ищите:')
        bot.register_next_step_handler(message, Find_Employee,bot)
    elif message.text == 'Назад' or message.text == '2':
        bot.send_message(message.chat.id, "/start")
    else:
        EmployeeMenu(message,bot)


def Find_Employee(message,bot):
    cursor = conn.cursor()
    query = "SELECT Employee_ID,First_Name,Second_Name,Third_Name,Email,Phone_Number,Date_Of_Birth,Address,Department,Position,Hire_Date,Employment_Status,Word_Schedule,Vacation_Days FROM Employees WHERE Second_Name = ?"
    cursor.execute(query, (message.text,))
    result = cursor.fetchall()

    if len(result) == 0:
        bot.send_message(message.chat.id, f"Сотрудник c фамилией {message.text} не был найден.")

        EmployeeMenu(message,bot)
    else:
        for row in result:
            employee_id, first_name, second_name, third_name, email, phone_number, date_of_birth, address, department, position, hire_date, employment_status, work_schedule, vacation_days = row
            employee_info = f"ID: {employee_id}\nИмя: {first_name}\nФамилия: {second_name}\nОтчество: {third_name}\nEmail: {email}\nНомер телефона: {phone_number}\nДата рождения: {date_of_birth}\nАдрес: {address}\nОтдел: {department}\nДолжность: {position}\nДата приема на работу: {hire_date}\nСтатус занятости: {employment_status}\nРабочий график: {work_schedule}\nКоличество отпускных дней: {vacation_days}"
            bot.send_message(message.chat.id, employee_info)

        cursor.close()
        Find_Menu(message,bot)


def Find_Menu(message,bot):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    delete_employee_button = telebot.types.KeyboardButton("Удалить")
    edit_employee_button = telebot.types.KeyboardButton("Редактировать")
    backButton = telebot.types.KeyboardButton("Назад")
    keyboard.add(delete_employee_button,edit_employee_button, backButton)
    bot.send_message(message.chat.id, 'Выберите пункт меню:')
    bot.send_message(message.chat.id, "\n1. Удалить сотрудника"
                                      "\n2. Редактировать информацию о сотруднике"
                                      "\n3. Назад", reply_markup=keyboard)
    bot.register_next_step_handler(message, Find_Menu_Handler,bot)

def Find_Menu_Handler(message,bot):
    if message.text == '1' or message.text.lower() == 'удалить':
        bot.send_message(message.chat.id, 'Введите ID сотрудника, которого вы хотите удалить')
        bot.register_next_step_handler(message, Delete_Employee,bot)
    elif message.text == '2' or message.text.lower() == 'редактировать':
        bot.send_message(message.chat.id, 'Введите ID сотрудника, информацию которого вы хотите изменить')
        bot.register_next_step_handler(message, Edit_Employee_Menu,bot)
    elif message.text == 'Назад' or message.text == '3':
        EmployeeMenu(message,bot)
    else:
        Find_Menu(message,bot)


def Edit_Employee_Menu(message,bot):
    id_employee = message.text
    bot.send_message(message.chat.id, 'Выберите, что вы хотите изменить:')
    bot.send_message(message.chat.id, "\n1. Имя"
                                      "\n2. Фамилию"
                                      "\n3. Отчество"
                                      "\n4. Email"
                                      "\n5. Номер телефона"
                                      "\n6. Дата рождения"
                                      "\n7. Адрес"
                                      "\n8. Департамент"
                                      "\n9. Позиция"
                                      "\n10. Дата трудоустройства"
                                      "\n11. Статус занятости"
                                      "\n12. Рассписание"
                                      "\n13. Дни отпуска"
                                      "\n14. Назад")
    bot.register_next_step_handler(message, Update_Employee, id_employee,bot)


def Update_Employee(message,id_employee,bot):
    if message.text == '1':
        bot.send_message(message.chat.id, 'Введите новое Имя для сотрудника с ID: '+id_employee)
        column_name = 'First_Name'
        bot.register_next_step_handler(message,Save_Employee_Update, id_employee,column_name,bot)
    if message.text == '2':
        bot.send_message(message.chat.id, 'Введите новую Фамилию для сотрудника с ID: '+id_employee)
        column_name = 'Second_Name'
        bot.register_next_step_handler(message,Save_Employee_Update, id_employee,column_name,bot)
    if message.text == '3':
        bot.send_message(message.chat.id, 'Введите новое Отчество для сотрудника с ID: '+id_employee)
        column_name = 'Third_Name'
        bot.register_next_step_handler(message,Save_Employee_Update, id_employee,column_name,bot)
    if message.text == '4':
        bot.send_message(message.chat.id, 'Введите новый Email для сотрудника с ID: '+id_employee)
        column_name = 'Email'
        bot.register_next_step_handler(message,Save_Employee_Update, id_employee,column_name,bot)
    if message.text == '5':
        bot.send_message(message.chat.id, 'Введите новый Номер Мобильного Телефона для сотрудника с ID: '+id_employee)
        column_name = 'Phone_Number'
        bot.register_next_step_handler(message,Save_Employee_Update, id_employee,column_name,bot)
    if message.text == '6':
        bot.send_message(message.chat.id, 'Введите новую Дату Рождения для сотрудника с ID: '+id_employee)
        column_name = 'Date_Of_Birth'
        bot.register_next_step_handler(message,Save_Employee_Update, id_employee,column_name,bot)
    if message.text == '7':
        bot.send_message(message.chat.id, 'Введите новый Адрес проживания для сотрудника с ID: '+id_employee)
        column_name = 'Address'
        bot.register_next_step_handler(message,Save_Employee_Update, id_employee,column_name,bot)
    if message.text == '8':
        bot.send_message(message.chat.id, 'Введите новый Отдел для сотрудника с ID: '+id_employee)
        column_name = 'Department'
        bot.register_next_step_handler(message,Save_Employee_Update, id_employee,column_name,bot)
    if message.text == '9':
        bot.send_message(message.chat.id, 'Введите новую Должность для сотрудника с ID: '+id_employee)
        column_name = 'Position'
        bot.register_next_step_handler(message,Save_Employee_Update, id_employee,column_name,bot)
    if message.text == '10':
        bot.send_message(message.chat.id, 'Введите новую Дату Трудоустройства для сотрудника с ID: '+id_employee)
        column_name = 'Hire_Date'
        bot.register_next_step_handler(message,Save_Employee_Update, id_employee,column_name,bot)
    if message.text == '11':
        bot.send_message(message.chat.id, 'Введите новую Форму Занятости для сотрудника с ID: '+id_employee)
        column_name = 'Employment_Status'
        bot.register_next_step_handler(message,Save_Employee_Update, id_employee,column_name,bot)
    if message.text == '12':
        bot.send_message(message.chat.id, 'Введите новое Рассписание для сотрудника с ID: '+id_employee)
        column_name = 'Work_Schedule'
        bot.register_next_step_handler(message,Save_Employee_Update, id_employee,column_name,bot)
    if message.text == '13':
        bot.send_message(message.chat.id, 'Введите новое количество дней отпуска для сотрудника с ID: '+id_employee)
        column_name = 'Vacation_Days'
        bot.register_next_step_handler(message,Save_Employee_Update, id_employee,column_name,bot)

def Save_Employee_Update(message, employee_id, column_name,bot):
    query = f"UPDATE Employees SET {column_name} = ? WHERE Employee_ID = ?"
    data = (message.text, employee_id)

    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    EmployeeMenu(message,bot)


def Delete_Employee(message,bot):
    cursor = conn.cursor()
    query = "DELETE FROM Employees WHERE Employee_ID = ?"

    cursor.execute(query, message.text)
    conn.commit()
    cursor.close()
    bot.send_message(message.chat.id, 'Сотрудник с ID: '+message.text+' был удалён')
    bot.send_message(message.chat.id, "/start")



def get_First_Name(message,bot):
    result = message.text
    colums[0] = result

    bot.send_message(message.chat.id, "Отлично, теперь введите фамилию")
    bot.register_next_step_handler(message, get_Second_Name,bot)

def get_Second_Name(message,bot):
    result = message.text
    colums[1] = result

    bot.send_message(message.chat.id, "Введите отчество")
    bot.register_next_step_handler(message, get_Third_Name,bot)

def get_Third_Name(message,bot):
    result = message.text
    colums[2] = result

    bot.send_message(message.chat.id, "Введите Email")
    bot.register_next_step_handler(message, get_Email,bot)

def get_Email(message,bot):
            result = message.text
            colums[3] = result

            bot.send_message(message.chat.id, "Введите номер мобильного телефона")
            bot.register_next_step_handler(message, get_Phone_Number,bot)

def get_Phone_Number(message,bot):
            result = message.text
            colums[4] = result

            bot.send_message(message.chat.id, "Введите дату рождения")
            bot.register_next_step_handler(message, get_Date_Of_Birth,bot)

def get_Date_Of_Birth(message,bot):
    result = message.text
    colums[5] = result

    bot.send_message(message.chat.id, "Введите адрес проживания")
    bot.register_next_step_handler(message, get_Address,bot)

def get_Address(message,bot):
    result = message.text
    colums[6] = result

    bot.send_message(message.chat.id, "Введите отдел в котором работает сотрудник")
    bot.register_next_step_handler(message, get_Department,bot)

def get_Department(message,bot):
    result = message.text
    colums[7] = result

    bot.send_message(message.chat.id, "Введите должность сотрудника")
    bot.register_next_step_handler(message, get_Position,bot)

def get_Position(message,bot):
    result = message.text
    colums[8] = result

    bot.send_message(message.chat.id, "Введите дату приёма сотрудника на работу")
    bot.register_next_step_handler(message, get_Hire_Date,bot)

def get_Hire_Date(message,bot):
    result = message.text
    colums[9] = result

    bot.send_message(message.chat.id, "Введите статус занятости сотрудника(полная, частичная)")
    bot.register_next_step_handler(message, get_Employment_Status,bot)

def get_Employment_Status(message,bot):
    result = message.text
    colums[10] = result

    bot.send_message(message.chat.id, "Введите рассписание работы сотрудника")
    bot.register_next_step_handler(message, get_Word_Schedule,bot)

def get_Word_Schedule(message,bot):
    result = message.text
    colums[11] = result

    bot.send_message(message.chat.id, "Введите количество дней отпуска")
    bot.register_next_step_handler(message, get_Vacation_Days,bot)

def get_Vacation_Days(message,bot):
    result = message.text
    colums[12] = result

    db_table_val(First_Name=colums[0], Second_Name=colums[1], Third_Name=colums[2],
                         Email=colums[3], Phone_Number=colums[4], Date_Of_Birth=colums[5], Address=colums[6],
                         Department=colums[7], Position=colums[8], Hire_Date=colums[9], Employment_Status=colums[10],
                         Word_Schedule=colums[11], Vacation_Days=colums[12],Device_ID=message.from_user.id)

    bot.send_message(message.chat.id, "Вы успешно зарегестрированны")

    employee_info = f"Имя: {colums[0]}\nФамилия: {colums[1]}\nОтчество: {colums[2]}\nEmail: {colums[3]}\nНомер телефона: {colums[4]}\nДата рождения: {colums[5]}\nАдрес: {colums[6]}\nОтдел: {colums[7]}\nДолжность: {colums[8]}\nДата приема на работу: {colums[9]}\nСтатус занятости: {colums[10]}\nРабочий график: {colums[11]}\nКоличество отпускных дней: {colums[12]}"
    bot.send_message(message.chat.id, employee_info)

    bot.send_message(message.chat.id, "/start")
