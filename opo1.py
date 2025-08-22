import telebot

# Replace with your actual bot token
BOT_TOKEN = '7396204915:AAFxxQ2kL9ylgLjMFdwUdDsMsRXhObn7dEY'
# Replace with your actual tech support group chat ID
TECH_SUPPORT_CHAT_ID = '-1002631818202'

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}


def create_keyboard(buttons):
    """Creates a ReplyKeyboardMarkup with the given buttons."""
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for button in buttons:
        keyboard.add(telebot.types.KeyboardButton(button))
    return keyboard


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Handles the /start command."""
    user_data[message.chat.id] = {}
    msg = bot.send_message(message.chat.id, "Здравствуйте! Я ваш помощник по решению проблем с ПК. "
                                            "Пожалуйста, укажите ваш внутренний номер:",
                           reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_internal_number)


def get_internal_number(message):
    """Gets the user's internal number."""
    user_data[message.chat.id]['internal_number'] = message.text
    msg = bot.send_message(message.chat.id, "Теперь укажите ваше рабочее место:")
    bot.register_next_step_handler(msg, get_workplace)


def get_workplace(message):
    """Gets the user's workplace."""
    user_data[message.chat.id]['workplace'] = message.text
    ask_main_problem(message)


def ask_main_problem(message):
    """Asks the user to choose a main problem category."""
    keyboard = create_keyboard([
        "1. Проблемы с почтой",
        "2. Не слышно клиентов (проблемы со звуком/микрофоном)",
        "3. [Третья категория проблемы]",
        "4. [Четвертая категория проблемы]",
        "5. [Пятая категория проблемы]"
    ])
    bot.send_message(message.chat.id, "С какой проблемой вы столкнулись?", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in ["1. Проблемы с почтой",
                                                           "2. Не слышно клиентов (проблемы со звуком/микрофоном)"])
def handle_main_problem(message):
    """Handles the user's choice of main problem."""
    problem_text = message.text
    if problem_text == "1. Проблемы с почтой":
        ask_mail_subproblem(message)
    elif problem_text == "2. Не слышно клиентов (проблемы со звуком/микрофоном)":
        ask_audio_subproblem(message)
    else:
        # Handle other main problems here
        bot.send_message(message.chat.id, "Эта категория еще не реализована. Пожалуйста, выберите другую.")
        ask_main_problem(message)


def ask_mail_subproblem(message):
    """Asks the user to choose a sub-problem for 'Проблемы с почтой'."""
    keyboard = create_keyboard([
        "1.1. Не отправляются сообщения",
        "1.2. Не открывается почта",
        "1.3. Не хватает памяти"
    ])
    bot.send_message(message.chat.id, "Укажите, что именно не так с почтой?", reply_markup=keyboard)


@bot.message_handler(
    func=lambda message: message.text in ["1.1. Не отправляются сообщения", "1.2. Не открывается почта",
                                          "1.3. Не хватает памяти"])
def handle_mail_subproblem(message):
    """Handles the user's choice of mail sub-problem."""
    subproblem_text = message.text
    user_data[message.chat.id]['problem'] = subproblem_text

    # Provide instructions based on the sub-problem
    if subproblem_text == "1.1. Не отправляются сообщения":
        # Example of sending a screenshot and instructions
        bot.send_message(message.chat.id,
                         "При попытке отправить письмо, оно попадает в папку 'Исходящие'? Если да, попробуйте следующий способ:")
        # You would send a screenshot here. Replace 'path/to/screenshot.png' with the actual path or file ID.
        # with open('path/to/screenshot.png', 'rb') as photo:
        #     bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id,
                         "Инструкция: Проверьте, что у вас есть подключение к интернету. Попробуйте перезапустить Outlook. Если не помогает, проверьте настройки учетной записи.")
    elif subproblem_text == "1.2. Не открывается почта":
        bot.send_message(message.chat.id,
                         "Инструкция: Убедитесь, что у вас есть свободное место на диске. Попробуйте запустить Outlook в безопасном режиме.")
    elif subproblem_text == "1.3. Не хватает памяти":
        bot.send_message(message.chat.id,
                         "Инструкция: Удалите ненужные файлы, очистите корзину. Ознакомьтесь с текстовым или видео-мануалом по очистке диска.")

    ask_solution_status(message)


def ask_audio_subproblem(message):
    """Asks the user to choose a sub-problem for 'Не слышно клиентов'."""
    keyboard = create_keyboard([
        "2.1. Не работает микрофон",
        "2.2. Не слышно звук"
    ])
    bot.send_message(message.chat.id, "Что именно не работает?", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in ["2.1. Не работает микрофон", "2.2. Не слышно звук"])
def handle_audio_subproblem(message):
    """Handles the user's choice of audio sub-problem."""
    subproblem_text = message.text
    user_data[message.chat.id]['problem'] = subproblem_text

    # Provide instructions based on the sub-problem
    bot.send_message(message.chat.id,
                     "Инструкция: Проверьте, что наушники/микрофон правильно подключены. Проверьте настройки звука в вашей операционной системе и в приложении, которое вы используете (например, Skype, Zoom). Ознакомьтесь с текстовым или видео-мануалом.")

    ask_solution_status(message)


def ask_solution_status(message):
    """Asks the user if the problem was solved."""
    keyboard = create_keyboard(["Да, решил", "Нет, не решил"])
    msg = bot.send_message(message.chat.id, "Я решил вашу проблему?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, handle_solution_status)


def handle_solution_status(message):
    """Handles the user's response to whether the problem was solved."""
    response = message.text
    if response == "Да, решил":
        bot.send_message(message.chat.id, "Отлично! Рад был помочь. Если возникнут еще проблемы, обращайтесь.",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        del user_data[message.chat.id]
    elif response == "Нет, не решил":
        internal_number = user_data[message.chat.id]['internal_number']
        workplace = user_data[message.chat.id]['workplace']
        problem = user_data[message.chat.id]['problem']

        support_message = (
            f"Новая заявка на помощь:\n"
            f"Внутренний номер сотрудника: {internal_number}\n"
            f"Рабочее место: {workplace}\n"
            f"Проблема: {problem}"
        )
        # Send the message to the tech support group
        bot.send_message(TECH_SUPPORT_CHAT_ID, support_message)

        bot.send_message(message.chat.id,
                         "Заявка на помощь отправлена специалистам. Ожидайте, они скоро с вами свяжутся.",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        del user_data[message.chat.id]
    else:
        ask_solution_status(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)