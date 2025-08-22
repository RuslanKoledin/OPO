import telebot
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
TECH_SUPPORT_CHAT_ID = os.getenv('TECH_SUPPORT_CHAT_ID')

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

PHOTO_1_ID = os.getenv('PHOTO_1_ID')
PHOTO_2_ID = os.getenv('PHOTO_2_ID')
PHOTO_3_ID = os.getenv('PHOTO_3_ID')


# получение айдишек скринов (эту функцию можно удалить после получения всех ID)
@bot.message_handler(content_types=['photo'])
def get_photo_id(message):
    file_id = message.photo[-1].file_id
    bot.reply_to(message, f"File ID этого фото: {file_id}")


def create_keyboard(buttons):
    """Создает клавиатуру с кнопками."""
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for button in buttons:
        keyboard.add(telebot.types.KeyboardButton(button))
    return keyboard


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Handles the /start command."""
    user_data[message.chat.id] = {}
    keyboard = create_keyboard(["Да", "Нет"])
    msg = bot.send_message(message.chat.id, "Здравствуйте! Я ваш помощник по решению проблем с ПК. "
                                            "Вы сотрудник Входящей Линии?",
                           reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_department)


def ask_department(message):
    """Спрашивает, является ли сотрудник специалистом Входящей Линии."""
    response = message.text
    if response == "Да":
        user_data[message.chat.id]['department'] = "Входящая Линия"
        msg = bot.send_message(message.chat.id, "Отлично! Пожалуйста, укажите ваш внутренний номер и ваше имя:",
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_user_info)
    elif response == "Нет":
        msg = bot.send_message(message.chat.id, "Пожалуйста, укажите название вашего отдела:",
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_department_name)
    else:
        keyboard = create_keyboard(["Да", "Нет"])
        msg = bot.send_message(message.chat.id, "Пожалуйста, выберите 'Да' или 'Нет'. Вы сотрудник Входящей Линии?",
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, ask_department)


def get_department_name(message):
    """Получает название отдела и запрашивает имя."""
    user_data[message.chat.id]['department'] = message.text
    msg = bot.send_message(message.chat.id, "Спасибо. Напишите ваше имя:")
    bot.register_next_step_handler(msg, get_user_info_other)


def get_user_info(message):
    """Получает внутренний номер и имя сотрудника Входящей Линии."""
    try:
        parts = message.text.split(' ', 1)
        if len(parts) < 2:
            raise ValueError
        user_data[message.chat.id]['internal_number'] = parts[0]
        user_data[message.chat.id]['name'] = parts[1]
        msg = bot.send_message(message.chat.id, "Теперь укажите ваше рабочее место: ")
        bot.register_next_step_handler(msg, get_workplace)
    except (IndexError, ValueError):
        msg = bot.send_message(message.chat.id,
                               "Пожалуйста, введите данные в формате 'номер имя'. Например, '1234 Руслан'.")
        bot.register_next_step_handler(msg, get_user_info)


def get_user_info_other(message):
    """Получает имя сотрудника другого отдела."""
    user_data[message.chat.id]['name'] = message.text
    user_data[message.chat.id]['internal_number'] = 'Не указан'
    msg = bot.send_message(message.chat.id, "Теперь укажите ваше рабочее место:")
    bot.register_next_step_handler(msg, get_workplace)


def get_workplace(message):
    """Получает рабочее место."""
    user_data[message.chat.id]['workplace'] = message.text
    ask_main_problem(message)


def ask_main_problem(message):
    """Спрашивает, с какой проблемой столкнулся пользователь."""
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
    """Обрабатывает выбор основной проблемы."""
    problem_text = message.text
    if problem_text == "1. Проблемы с почтой":
        ask_mail_subproblem(message)
    elif problem_text == "2. Не слышно клиентов (проблемы со звуком/микрофоном)":
        ask_audio_subproblem(message)
    else:
        bot.send_message(message.chat.id, "Эта категория еще не реализована. Пожалуйста, выберите другую.")
        ask_main_problem(message)


def ask_mail_subproblem(message):
    """Спрашивает под-проблему с почтой."""
    keyboard = create_keyboard([
        "1.1. Не отправляются сообщения",
        "1.2. Не открывается почта",
        "1.3. Не хватает памяти"
    ])
    bot.send_message(message.chat.id, "Укажите, что именно не так с почтой?", reply_markup=keyboard)


@bot.message_handler(
    func=lambda message: message.text in ["1.1. Не отправляются сообщения",
                                          "1.2. Не открывается почта",
                                          "1.3. Не хватает памяти"])
def handle_mail_subproblem(message):
    """Обрабатывает выбор под-проблемы с почтой."""
    subproblem_text = message.text
    user_data[message.chat.id]['problem'] = subproblem_text

    if subproblem_text == "1.1. Не отправляются сообщения":
        bot.send_message(message.chat.id,
                         "При попытке отправить письмо, оно попадает в папку 'Исходящие'? Если да, попробуйте следующий способ:")
        bot.send_photo(message.chat.id, PHOTO_1_ID, caption="1. Проверьте подключение в Outlook.")
        bot.send_photo(message.chat.id, PHOTO_2_ID, caption="2. Если статус 'Отключен', нажмите на него.")
        bot.send_photo(message.chat.id, PHOTO_3_ID, caption="3. Попробуйте отправить письмо снова.")
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
    """Спрашивает под-проблему со звуком."""
    keyboard = create_keyboard([
        "2.1. Не работает микрофон",
        "2.2. Не слышно звук"
    ])
    bot.send_message(message.chat.id, "Что именно не работает?", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in ["2.1. Не работает микрофон", "2.2. Не слышно звук"])
def handle_audio_subproblem(message):
    """Обрабатывает выбор под-проблемы со звуком."""
    subproblem_text = message.text
    user_data[message.chat.id]['problem'] = subproblem_text
    bot.send_message(message.chat.id,
                     "Инструкция: Проверьте, что наушники/микрофон правильно подключены. Проверьте настройки звука в вашей операционной системе и в приложении, которое вы используете (например, Skype, Zoom). Ознакомьтесь с текстовым или видео-мануалом.")
    ask_solution_status(message)


def ask_solution_status(message):
    """Спрашивает, решена ли проблема."""
    keyboard = create_keyboard(["Да, решил", "Нет, не решил"])
    msg = bot.send_message(message.chat.id, "Я решил вашу проблему?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, handle_solution_status)


def handle_solution_status(message):
    """Обрабатывает ответ о решении проблемы."""
    response = message.text
    if response == "Да, решил":
        bot.send_message(message.chat.id, "Отлично! Рад был помочь. Если возникнут еще проблемы, обращайтесь.",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        del user_data[message.chat.id]
    elif response == "Нет, не решил":
        user_info = user_data.get(message.chat.id, {})

        name = user_info.get('name', 'Не указано')
        internal_number = user_info.get('internal_number', 'Не указан')
        workplace = user_info.get('workplace', 'Не указано')
        problem = user_info.get('problem', 'Не указана')

        department = user_info.get('department')
        if department == "Входящая Линия":  # Используем "Входящая Линия" вместо "Да"
            support_message = (
                f"Новая заявка на помощь от Входящей Линии:\n"
                f"Имя сотрудника: {name}\n"
                f"Внутренний номер: {internal_number}\n"
                f"Рабочее место: {workplace}\n"
                f"Проблема: {problem}"
            )
        else:
            support_message = (
                f"Новая заявка на помощь:\n"
                f"Отдел: {department}\n"
                f"Имя сотрудника: {name}\n"
                f"Рабочее место: {workplace}\n"
                f"Проблема: {problem}"
            )

        bot.send_message(TECH_SUPPORT_CHAT_ID, support_message)

        bot.send_message(message.chat.id,
                         "Заявка на помощь отправлена специалистам. Ожидайте, они скоро к вам подойдут.",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        del user_data[message.chat.id]
    else:
        ask_solution_status(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)