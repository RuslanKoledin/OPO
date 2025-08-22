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
PHOTO_4_ID = os.getenv('PHOTO_4_ID')
PHOTO_5_ID = os.getenv('PHOTO_5_ID')
PHOTO_6_ID = os.getenv('PHOTO_6_ID')
PHOTO_7_ID = os.getenv('PHOTO_7_ID')
PHOTO_8_ID = os.getenv('PHOTO_8_ID')
PHOTO_9_ID = os.getenv('PHOTO_9_ID')
PHOTO_11_ID = os.getenv('PHOTO_11_ID')
PHOTO_12_ID = os.getenv('PHOTO_12_ID')
PHOTO_13_ID = os.getenv('PHOTO_13_ID')
PHOTO_14_ID = os.getenv('PHOTO_14_ID')
PHOTO_15_ID = os.getenv('PHOTO_15_ID')
PHOTO_16_ID = os.getenv('PHOTO_16_ID')
PHOTO_17_ID = os.getenv('PHOTO_17_ID')
PHOTO_18_ID = os.getenv('PHOTO_18_ID')
PHOTO_19_ID = os.getenv('PHOTO_19_ID')

PHOTO_20_ID = os.getenv('PHOTO_20_ID')
PHOTO_21_ID = os.getenv('PHOTO_21_ID')
PHOTO_22_ID = os.getenv('PHOTO_22_ID')
PHOTO_23_ID = os.getenv('PHOTO_23_ID')
PHOTO_24_ID = os.getenv('PHOTO_24_ID')
PHOTO_25_ID = os.getenv('PHOTO_25_ID')
PHOTO_26_ID = os.getenv('PHOTO_26_ID')
PHOTO_27_ID = os.getenv('PHOTO_27_ID')
PHOTO_28_ID = os.getenv('PHOTO_28_ID')

PHOTO_29_ID = os.getenv('PHOTO_29_ID')
PHOTO_30_ID = os.getenv('PHOTO_30_ID')
PHOTO_31_ID = os.getenv('PHOTO_31_ID')
PHOTO_32_ID = os.getenv('PHOTO_32_ID')
PHOTO_33_ID = os.getenv('PHOTO_33_ID')
PHOTO_34_ID = os.getenv('PHOTO_34_ID')
PHOTO_35_ID = os.getenv('PHOTO_35_ID')
PHOTO_36_ID = os.getenv('PHOTO_36_ID')
PHOTO_37_ID = os.getenv('PHOTO_37_ID')

PHOTO_38_ID = os.getenv('PHOTO_38_ID')
PHOTO_39_ID = os.getenv('PHOTO_39_ID')
PHOTO_41_ID = os.getenv('PHOTO_41_ID')
PHOTO_42_ID = os.getenv('PHOTO_42_ID')
PHOTO_43_ID = os.getenv('PHOTO_43_ID')
PHOTO_44_ID = os.getenv('PHOTO_44_ID')
#прокси вин
PHOTO_45_ID = os.getenv('PHOTO_45_ID')
PHOTO_46_ID = os.getenv('PHOTO_46_ID')
PHOTO_47_ID = os.getenv('PHOTO_47_ID')
PHOTO_48_ID = os.getenv('PHOTO_48_ID')
PHOTO_49_ID = os.getenv('PHOTO_49_ID')
#наушники
PHOTO_50_ID = os.getenv('PHOTO_50_ID')
PHOTO_51_ID = os.getenv('PHOTO_51_ID')
PHOTO_52_ID = os.getenv('PHOTO_52_ID')
PHOTO_53_ID = os.getenv('PHOTO_53_ID')
PHOTO_54_ID = os.getenv('PHOTO_54_ID')
PHOTO_55_ID = os.getenv('PHOTO_55_ID')
PHOTO_56_ID = os.getenv('PHOTO_56_ID')
PHOTO_57_ID = os.getenv('PHOTO_57_ID')
PHOTO_58_ID = os.getenv('PHOTO_58_ID')
PHOTO_59_ID = os.getenv('PHOTO_59_ID')
PHOTO_60_ID = os.getenv('PHOTO_60_ID')
PHOTO_61_ID = os.getenv('PHOTO_61_ID')
PHOTO_62_ID = os.getenv('PHOTO_62_ID')
PHOTO_63_ID = os.getenv('PHOTO_63_ID')
PHOTO_64_ID = os.getenv('PHOTO_64_ID')
PHOTO_65_ID = os.getenv('PHOTO_65_ID')
PHOTO_66_ID = os.getenv('PHOTO_66_ID')
PHOTO_67_ID = os.getenv('PHOTO_67_ID')

PHOTO_68_ID = os.getenv('PHOTO_68_ID')
PHOTO_69_ID = os.getenv('PHOTO_69_ID')

# получение айдишек скринов
@bot.message_handler(content_types=['photo', 'document'])
def get_file_id(message):
    file_id = None
    file_type = None

    if message.photo:
        file_id = message.photo[-1].file_id
        file_type = "Photo"
    elif message.document:
        file_id = message.document.file_id
        file_type = "Document"

    if file_id:
        bot.reply_to(message, f"File ID этого файла: {file_id}\nТип файла: {file_type}")
    else:
        bot.reply_to(message, "Не удалось получить ID файла.")


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
    msg = bot.send_message(message.chat.id, "Спасибо. Теперь укажите ваше имя:")
    bot.register_next_step_handler(msg, get_user_info_other)


def get_user_info(message):
    """Получает внутренний номер и имя сотрудника Входящей Линии."""
    try:
        parts = message.text.split(' ', 1)
        if len(parts) < 2:
            raise ValueError
        user_data[message.chat.id]['internal_number'] = parts[0]
        user_data[message.chat.id]['name'] = parts[1]
        msg = bot.send_message(message.chat.id, "Теперь укажите ваше рабочее место:")
        bot.register_next_step_handler(msg, get_workplace)
    except (IndexError, ValueError):
        msg = bot.send_message(message.chat.id,
                               "Пожалуйста, введите данные в формате 'номер имя'. Например, '1234 Иван Иванов'.")
        bot.register_next_step_handler(msg, get_user_info)


def get_user_info_other(message):
    """Получает имя сотрудника другого отдела."""
    user_data[message.chat.id]['name'] = message.text
    user_data[message.chat.id]['internal_number'] = 'Не указан'
    msg = bot.send_message(message.chat.id, "Теперь укажите ваше рабочее место:")
    bot.register_next_step_handler(msg, get_workplace)


def ask_main_problem(message):
    """Спрашивает, с какой проблемой столкнулся пользователь."""
    keyboard = create_keyboard([
        "1. Проблемы с почтой",
        "2. Настройка Тонкий VISA",
        "3. Не работает наушник - звук/микрофон",
        "4. Настройка прокси Windows",  # НОВАЯ КАТЕГОРИЯ
        "5. Монитор не включается"  # НОВАЯ КАТЕГОРИЯ
    ])
    bot.send_message(message.chat.id, "С какой проблемой вы столкнулись?", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in ["1. Проблемы с почтой",
                                                           "2. Настройка Тонкий VISA",
                                                           "3. Не работает наушник - звук/микрофон",
                                                           "4. Настройка прокси Windows",  # НОВАЯ КАТЕГОРИЯ
                                                           "5. Монитор не включается"])  # НОВАЯ КАТЕГОРИЯ
def handle_main_problem(message):
    """Обрабатывает выбор основной проблемы."""
    # СБРАСЫВАЕМ ДАННЫЕ ПРИ ВЫБОРЕ НОВОЙ ПРОБЛЕМЫ
    user_data[message.chat.id] = {}

    problem_text = message.text
    if problem_text == "1. Проблемы с почтой":
        ask_mail_subproblem(message)
    elif problem_text == "2. Настройка Тонкий VISA":
        ask_visa_subproblem(message)
    elif problem_text == "4. Настройка прокси Windows":  # НОВАЯ ЛОГИКА
        ask_windows_subproblem(message)
    elif problem_text in ["3. Не работает наушник - звук/микрофон",
                          "5. Монитор не включается"]:  # НОВАЯ КАТЕГОРИЯ В ЭТОЙ ГРУППЕ
        user_data[message.chat.id]['problem'] = problem_text
        msg = bot.send_message(message.chat.id,
                               "Опишите вашу проблему максимально подробно, чтобы специалисты могли вам помочь.")
        bot.register_next_step_handler(msg, handle_other_problem)


def handle_other_problem(message):
    """Обрабатывает подробное описание проблемы и завершает заявку."""
    user_data[message.chat.id]['detailed_problem'] = message.text
    handle_solution_status(message, is_solved=False)


def ask_mail_subproblem(message):
    """Спрашивает под-проблему с почтой."""
    keyboard = create_keyboard([
        "1.1. Заполнилась память",
        "1.2. Не открывается OutLook",
        "1.3. Письма в Исходящих"
    ])
    bot.send_message(message.chat.id, "Укажите, что именно не так с почтой?", reply_markup=keyboard)


@bot.message_handler(
    func=lambda message: message.text in ["1.1. Заполнилась память",
                                          "1.2. Не открывается OutLook",
                                          "1.3. Письма в Исходящих"])
def handle_mail_subproblem(message):
    """Обрабатывает выбор под-проблемы с почтой."""
    subproblem_text = message.text
    user_data[message.chat.id]['problem'] = subproblem_text
    user_data[message.chat.id]['detailed_problem'] = subproblem_text

    if subproblem_text == "1.1. Заполнилась память":
        bot.send_message(message.chat.id,
                         "Попробуйте следующий способ:")
        bot.send_photo(message.chat.id, PHOTO_1_ID, caption="1. Открываем Outlook, далее нажимаем «Файл».")
        bot.send_photo(message.chat.id, PHOTO_2_ID,
                       caption="2. Далее нажимаем на выпадающий список «Инструменты» либо «Средства очистки»")
        bot.send_photo(message.chat.id, PHOTO_3_ID,
                       caption="3. Выбираем «Удалять старые элементы» или «Архивировать» (в старой версии «Архивация»)")
        bot.send_photo(message.chat.id, PHOTO_4_ID, caption="4. Далее выполняем следующие действия:\n"
                                                            "1) Выбираем до какого числа архивировать сообщения;\n"
                                                            "2) Выбираем, где будет хранится наш архив (желательно на диске D);\n"
                                                            "3) После того, как сделали, нажимаем на кнопку «ОК»")
        bot.send_photo(message.chat.id, PHOTO_5_ID, caption="5. Как проверить архивация идет или нет?\n"
                                                            "В главном меню, снизу будет идти загрузка \n"
                                                            "После завершения архивации перезапустите Outlook.\n")

        bot.send_message(message.chat.id,
                         "Инструкция: Проверьте, что у вас есть подключение к интернету. Попробуйте перезапустить Outlook. Если не помогает, проверьте настройки учетной записи.")
    elif subproblem_text == "1.2. Не открывается OutLook":
        bot.send_message(message.chat.id,
                         "Попробуйте следующий способ:")
        bot.send_photo(message.chat.id, PHOTO_6_ID, caption="1.Нажимаем на иконку Интернета, после чего на cbk.kg")
        bot.send_photo(message.chat.id, PHOTO_7_ID, caption="2.Далее нажимаем на ползунок и отключаем прокси-сервер")
        bot.send_photo(message.chat.id, PHOTO_8_ID,
                       caption="3.Нажимаем на “Пуск”, пишем “Панель управления” и нажимаем на него")
        bot.send_photo(message.chat.id, PHOTO_9_ID, caption="4.Нажимаем на “Категория” и выбираем “Крупные значки”")
        bot.send_photo(message.chat.id, PHOTO_11_ID, caption="5.Нажимаем на “Почта”")
        bot.send_photo(message.chat.id, PHOTO_12_ID, caption="6.Далее нажимаем на “Показать”")
        bot.send_photo(message.chat.id, PHOTO_13_ID,
                       caption="7.Нажимаем на “Удалить”, тем самым удаляем текущую конфигурацию")
        bot.send_photo(message.chat.id, PHOTO_14_ID, caption="8.Далее нажимаем на “Да”")
        bot.send_photo(message.chat.id, PHOTO_15_ID, caption="9.Добавляем новую конфигурацию.")
        bot.send_photo(message.chat.id, PHOTO_16_ID,
                       caption="10.Прописываем в поле “Имя конфигурации”: 123, 11, 1, 2 или 3. Далее нажимаем на “Ок”")
        bot.send_photo(message.chat.id, PHOTO_17_ID, caption="11.Нажимаем на “Далее”")
        bot.send_photo(message.chat.id, PHOTO_18_ID, caption="12.После чего нажимаем на “Готово”")
        bot.send_photo(message.chat.id, PHOTO_19_ID, caption="13.Далее нажимаем сперва на “Применить”, затем на “Ок”")
        bot.send_message(message.chat.id,
                         "14.Конфигурации изменены. Теперь открываем Outlook. Если выйдет окошко, нажимаем на “Подключиться”. После открытия, включаем прокси-сервер как в скрине 1 и 2, нажимаем “Сохранить” несколько раз. Готово!")
    elif subproblem_text == "1.3. Письма в Исходящих":
        bot.send_message(message.chat.id,
                         "Сначала пробуем просто закрыть Outlook и войти обратно!!! Если место в памяти еще есть, то это должно помочь.\n"
                         "Если не помогло, то меняем конфигурацию согласно мануалу ниже:")
        bot.send_photo(message.chat.id, PHOTO_6_ID, caption="1.Нажимаем на иконку Интернета, после чего на cbk.kg")
        bot.send_photo(message.chat.id, PHOTO_7_ID, caption="2.Далее нажимаем на ползунок и отключаем прокси-сервер")
        bot.send_photo(message.chat.id, PHOTO_8_ID,
                       caption="3.Нажимаем на “Пуск”, пишем “Панель управления” и нажимаем на него")
        bot.send_photo(message.chat.id, PHOTO_9_ID, caption="4.Нажимаем на “Категория” и выбираем “Крупные значки”")
        bot.send_photo(message.chat.id, PHOTO_11_ID, caption="5.Нажимаем на “Почта”")
        bot.send_photo(message.chat.id, PHOTO_12_ID, caption="6.Далее нажимаем на “Показать”")
        bot.send_photo(message.chat.id, PHOTO_13_ID,
                       caption="7.Нажимаем на “Удалить”, тем самым удаляем текущую конфигурацию")
        bot.send_photo(message.chat.id, PHOTO_14_ID, caption="8.Далее нажимаем на “Да”")
        bot.send_photo(message.chat.id, PHOTO_15_ID, caption="9.Добавляем новую конфигурацию.")
        bot.send_photo(message.chat.id, PHOTO_16_ID,
                       caption="10.Прописываем в поле “Имя конфигурации”: 123, 11, 1, 2 или 3. Далее нажимаем на “Ок”")
        bot.send_photo(message.chat.id, PHOTO_17_ID, caption="11.Нажимаем на “Далее”")
        bot.send_photo(message.chat.id, PHOTO_18_ID, caption="12.После чего нажимаем на “Готово”")
        bot.send_photo(message.chat.id, PHOTO_19_ID, caption="13.Далее нажимаем сперва на “Применить”, затем на “Ок”")
        bot.send_message(message.chat.id,
                         "14.Конфигурации изменены. Теперь открываем Outlook. Если выйдет окошко, нажимаем на “Подключиться”. После открытия, включаем прокси-сервер как в скрине 1 и 2, нажимаем “Сохранить” несколько раз. Готово!")

    ask_solution_status(message)


def ask_visa_subproblem(message):
    """Спрашивает под-проблему с Тонким VISA."""
    keyboard = create_keyboard([
        "2.1. Тонкий на новом Firefox",
        "2.2. Тонкий на старом Firefox"
    ])
    bot.send_message(message.chat.id, "Какой версией Firefox вы пользуетесь?", reply_markup=keyboard)


@bot.message_handler(
    func=lambda message: message.text in ["2.1. Тонкий на новом Firefox", "2.2. Тонкий на старом Firefox"])
def handle_visa_subproblem(message):
    """Обрабатывает выбор под-проблемы с Тонким VISA."""
    subproblem_text = message.text
    user_data[message.chat.id]['problem'] = subproblem_text
    user_data[message.chat.id]['detailed_problem'] = subproblem_text

    if subproblem_text == "2.1. Тонкий на новом Firefox":
        bot.send_message(message.chat.id,
                         "Следуйте инструкции ниже: ")
        bot.send_photo(message.chat.id, PHOTO_20_ID, caption="1. Открываем браузер «MozillaFirefox».")
        bot.send_photo(message.chat.id, PHOTO_21_ID, caption="2. Нажимаем на Меню браузера.")
        bot.send_photo(message.chat.id, PHOTO_22_ID, caption="3. Нажимаем «Настройки».")
        bot.send_photo(message.chat.id, PHOTO_23_ID,
                       caption="4. Далее спускаемся в самый низ и находим кнопку «Параметры» («Settings»).")
        bot.send_photo(message.chat.id, PHOTO_24_ID, caption="5. Начинаем настройку:\n"
                                                             "1) Выбираем пункт «Настройка прокси вручную» («Manual proxy configuration»);\n"
                                                             "2) Прописываем в ячейке IP: 172.22.25.11; \n"
                                                             "3) Прописываем порт: 4545;\n"
                                                             "4) Обязательно ставим галочку в конце (иначе работать не будет);\n"
                                                             "5) Нажимаем ОК.")
        bot.send_photo(message.chat.id, PHOTO_25_ID,
                       caption="6. Затем копируем ссылку Тонкого Виза/Тонкого Элкарт и вставляем в адресную строку браузера «MozillaFirefox».\n"
                               " Если после этого выйдет следующее окно, нажимаем на «Advanced».")
        bot.send_photo(message.chat.id, PHOTO_26_ID, caption="7. После этого нажимаем «AddException…».")
        bot.send_photo(message.chat.id, PHOTO_27_ID, caption="8. Далее «Confirm Security Exception».")
        bot.send_photo(message.chat.id, PHOTO_28_ID,
                       caption="9. При нажатии на предыдущую кнопку откроется сайт «Тонкий VISA». Можете прописать логин и пароль с MWiki.")
        bot.send_message(message.chat.id, "Настройка завершена.")

    elif subproblem_text == "2.2. Тонкий на старом Firefox":
        bot.send_message(message.chat.id, "Следуйте другой инструкции для старой версии Firefox: ")
        bot.send_photo(message.chat.id, PHOTO_29_ID, caption="1. Открываем браузер MozillaFirefox. ")
        bot.send_photo(message.chat.id, PHOTO_30_ID, caption="2. Нажимаем на Меню браузера ")
        bot.send_photo(message.chat.id, PHOTO_31_ID, caption="3. Нажимаем “Настройки” ")
        bot.send_photo(message.chat.id, PHOTO_32_ID, caption="4. Далее “Дополнительные” ")
        bot.send_photo(message.chat.id, PHOTO_33_ID, caption="5. Затем нажимаем на “Сеть” и “Настроить” ")
        bot.send_photo(message.chat.id, PHOTO_34_ID,
                       caption="6. Выбираем “Ручная настрока сервиса прокси”, далее прописываем в HTTPпрокси: "
                               "172.22.25.11, в Порт: 4545, после чего ставим галочку в “Использовать этот прокси-сервер для всех протоколов” "
                               "(как на скрине)")
        bot.send_photo(message.chat.id, PHOTO_35_ID,
                       caption="7. Затем копируем ссылки Тонкого Виза/Тонкого Элкарт и вставляем в адресную строку браузера Мозилла Файрфокс."
                               " Если после этого выйдет следующее окно, нажимаем на «Я понимаю риск» и «Добавить исключение…»")
        bot.send_photo(message.chat.id, PHOTO_36_ID,
                       caption="8. После этого нажимаем «Подтвердить исключение безопасности»")
        bot.send_photo(message.chat.id, PHOTO_37_ID, caption="9. Далее откроется сайт. ")
        bot.send_message(message.chat.id, "Настройка завершена.")

    ask_solution_status(message)

def ask_head_seat_subproblem(message):
    """Спрашивает под-проблему с Тонким VISA."""
    keyboard = create_keyboard([
        "3.1. Сброс Cisco Jabber",
        "3.2. Настройка наушников"
    ])
    bot.send_message(message.chat.id, "Если нет звука попробуйте сначала сбросить Cisco Jabber, если не поможет, нужно настроить наушники: ", reply_markup=keyboard)


@bot.message_handler(
    func=lambda message: message.text in ["3.1. Сброс Cisco Jabber", "3.2. Настройка наушников"])
def handle_head_seat_subproblem(message):
    subproblem_text = message.text
    user_data[message.chat.id]['problem'] = subproblem_text
    user_data[message.chat.id]['detailed_problem'] = subproblem_text

    if subproblem_text == "3.1. Сброс Cisco Jabber":
        bot.send_photo(message.chat.id, PHOTO_67_ID, caption="Сначала заходим в Cisco Jabber, вводим логин и пароль "
                                          "от своей учетной записи смотрим на значок монитора в окошке приложения.")
        bot.send_photo(message.chat.id,PHOTO_50_ID,caption="Если значок монитора красный, то нужно совершить сброс Jabbera по следующей инструкции: ")
        bot.send_photo(message.chat.id,PHOTO_51_ID,caption="1. Откройте меню настроек. Нажмите на иконку шестеренки (⚙️) в правом верхнем углу окна Cisco Jabber.")
        bot.send_photo(message.chat.id,PHOTO_52_ID,caption="2. Выйдите из приложения. В открывшемся меню выберите пункт «Выйти». После этого вы увидите окно подтверждения.")
        bot.send_photo(message.chat.id,PHOTO_53_ID,caption="3. Выполните сброс. В окне подтверждения выхода нажмите кнопку «Сброс Jabber».")
        bot.send_photo(message.chat.id,PHOTO_54_ID,caption="4. Подтвердите действие. Система запросит подтверждение сброса")
        bot.send_photo(message.chat.id,PHOTO_55_ID,caption="-Подтверждаем \n"
                                                           "5. Введите пароль Windows. В появившемся окне введите ваш пароль для учетной записи Windows")

        bot.send_message(message.chat.id,"Готово! Теперь значок должен стать зеленым и можно проверять звук.\n"
                                                           "\nНе помогло? Тогда нужно проверить наушник по следующему мануалу:")
    elif subproblem_text == "3.2. Настройка наушников":
        bot.send_message(message.chat.id, "Чтобы настроить наушники используйте данный мануал 👇")
        bot.send_photo(message.chat.id,PHOTO_56_ID,caption="С ноги залетаем в панель управления.\n"
                                                           "Для этого в поисковике пишем – Панель управления.")
        bot.send_photo(message.chat.id,PHOTO_57_ID,caption="Жмакаем на неё.")
        bot.send_photo(message.chat.id,PHOTO_58_ID,caption="Меняем вид значков с – Категории, на – Крупные значки.")
        bot.send_photo(message.chat.id,PHOTO_59_ID,caption="И сразу бахаем в – звук")
        bot.send_message(message.chat.id,"У Вас первоначально откроется панель воспроизведения, там можно посмотреть, откуда еще может идти звук, кроме как с наушников. "
                                         "Если, у Вас монитор говорящий, то можно отключить отсюда, чтобы в CISCO каждый раз не настраивать его.")
        bot.send_photo(message.chat.id,PHOTO_60_ID,caption="Если видите, что есть картинка монитора, жмакаем правой и нажимаем на – отключить.")
        bot.send_photo(message.chat.id,PHOTO_61_ID,caption="Далее, переходим во вкладку – запись.")
        bot.send_photo(message.chat.id,PHOTO_62_ID,caption="С ноги пинаем на значок, где стоит галочка два раза.\n"
                                                           "Залетаем в - Прослушать")
        bot.send_photo(message.chat.id,PHOTO_63_ID,caption="Жмакаем на – прослушать с этого устройства.")
        bot.send_photo(message.chat.id,PHOTO_64_ID,caption="И применяем."
                                                           "\nДалее вы можете услышать себя, если будете говорить в микрофон.")
        bot.send_photo(message.chat.id,PHOTO_65_ID,caption="\nЕсли всё хорошо слышно и слышно вообще, то отключаем обратно функцию – прослушивать с данного устройства."
                                                           "\nИ применяем.")
        bot.send_message(message.chat.id,"Ну – с, теперь вы можете проверять работоспособность наушников.")
        bot.send_message(message.chat.id,"---------------------------------------------------------")
        bot.send_message(message.chat.id,"Однако в случае, если гарнитура подключена к ПК, но микрофон не работает, стоит проверить следующую настройку.")
        bot.send_photo(message.chat.id,PHOTO_66_ID,caption="Если значок такой, как на картинке, значит, микрофон выключен."
                                                           "Для его включения просто нажмите на кнопку динамика, чтобы он стал таким: 🔊. После микрофон должен заработать.")

# НОВЫЕ ФУНКЦИИ ДЛЯ ПРОБЛЕМ С WINDOWS
def ask_windows_subproblem(message):
    """Спрашивает под-проблему с прокси Windows."""
    keyboard = create_keyboard([
        "4.1. Windows 10",
        "4.2. Windows 11"
    ])
    bot.send_message(message.chat.id, "Какой версией Windows вы пользуетесь?", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in ["4.1. Windows 10", "4.2. Windows 11"])
def handle_windows_subproblem(message):
    subproblem_text = message.text
    user_data[message.chat.id]['problem'] = subproblem_text
    user_data[message.chat.id]['detailed_problem'] = subproblem_text

    if subproblem_text == "4.1. Windows 10":
        bot.send_message(message.chat.id, "Инструкция по настройке прокси для Windows 10: "
                                          "Пожалуйста, следуйте этим шагам.")
        bot.send_message(message.chat.id, "Шаг 1. Зайти в браузер «Google Chrome» или «Microsoft Edge» и открыть сайт MWiki по адресу: https://wiki.mbank.kg/.")
        bot.send_photo(message.chat.id, PHOTO_38_ID, caption="Шаг 2. После ввода логина и пароля от учетной записи, нажать на блок с заголовком «Что делать если не работают интерфейсы? Нужно прописать прокси сервер!». Возможно, придется его поискать через стрелки.")
        bot.send_message(message.chat.id, "Шаг 3. Скопировать⬇️:\n"
                                        "*Для копирования текста используйте комбинацию клавиш: Ctrl + C 👇\n "
                                        "192.168.127.53;10.20.83.3;10.100.100.114;172.22.26.3;10.20.83.3;"
                                        "www.cbk.kg;10.10.91.28;ibank.cbk.kg;10.255.0.20;10.255.0.20;10.10.91.62;mail.cbk.kg;172.22.25.29;*.cbk.kg;10.10.91.67;"
                                        "mbank-arm.cbk.kg;http://cbkportal;172.23.182.135;*crm.mbank.kg;*onboarding.mbank.kg;*edu.mbank.kg;*corporate.mbank.kg;"
                                        "*.mbank.kg;*kk.mbank.kg;*mbank.people.kg;*ednametabase.mbank.kg;*ct.cbk.kg;*wiki.mbank.kg*;mbank.kg*;wfm-app01")
        bot.send_photo(message.chat.id, PHOTO_39_ID, caption="Шаг 4. Свернуть браузер и нажать на кнопку «Пуск», далее «Параметры».")
        bot.send_photo(message.chat.id, PHOTO_41_ID, caption="Шаг 5. Выбрать раздел «Сеть и интернет».")
        bot.send_photo(message.chat.id, PHOTO_42_ID, caption="Шаг 6. Перейти в раздел «Прокси-сервер» и нажать на иконку «монитора».")
        bot.send_photo(message.chat.id, PHOTO_43_ID, caption="Шаг 7. Переключить ползунок «Использовать прокси-сервер» на «Вкл.» и прописать все, как на скриншоте. IP адрес: 172.23.182.133, порт: 3128.")
        bot.send_photo(message.chat.id, PHOTO_44_ID, caption="Шаг 8. Далее вставляем скопированный текст с MWiki в поле, как указано на скриншоте, и обязательно нажимаем на кнопку «Сохранить». ")
        bot.send_message(message.chat.id, "Готово! 👍")

    elif subproblem_text == "4.2. Windows 11":
        bot.send_message(message.chat.id, "Инструкция по настройке прокси для Windows 11: "
                                          "Пожалуйста, следуйте этим шагам.")
        bot.send_message(message.chat.id, "Шаг 1. Зайти в браузер «Google Chrome» или «Microsoft Edge» и открыть сайт MWiki по адресу: https://wiki.mbank.kg/.")
        bot.send_photo(message.chat.id, PHOTO_45_ID,
                       caption="Шаг 2. После ввода логина и пароля от учетной записи, нажать на блок с заголовком «Что делать если не работают интерфейсы? Нужно прописать прокси сервер!». Возможно, придется его поискать через стрелки.")
        bot.send_message(message.chat.id, "Шаг 3. Скопировать⬇️:\n"
                                      "*Для копирования текста используйте комбинацию клавиш: Ctrl + C 👇\n "
                                      "192.168.127.53;10.20.83.3;10.100.100.114;172.22.26.3;10.20.83.3;"
                                      "www.cbk.kg;10.10.91.28;ibank.cbk.kg;10.255.0.20;10.255.0.20;10.10.91.62;mail.cbk.kg;172.22.25.29;*.cbk.kg;10.10.91.67;"
                                      "mbank-arm.cbk.kg;http://cbkportal;172.23.182.135;*crm.mbank.kg;*onboarding.mbank.kg;*edu.mbank.kg;*corporate.mbank.kg;"
                                      "*.mbank.kg;*kk.mbank.kg;*mbank.people.kg;*ednametabase.mbank.kg;*ct.cbk.kg;*wiki.mbank.kg*;mbank.kg*;wfm-app01")
        bot.send_photo(message.chat.id, PHOTO_46_ID, caption="Шаг 4. Свернуть браузер и нажать на кнопку «Пуск», далее «Параметры».")
        bot.send_photo(message.chat.id, PHOTO_47_ID, caption="Шаг 5. Выбрать раздел «Сеть и интернет» и далее «Прокси-сервер».")
        bot.send_photo(message.chat.id, PHOTO_48_ID, caption="Шаг 6. В открывшемся разделе нажимаем кнопку «Изменить»")
        bot.send_photo(message.chat.id, PHOTO_49_ID, caption="Шаг 7. Переключить ползунок «Использовать прокси-сервер» на «Вкл.» и прописать все, как на скриншоте. "
                                                             "IP адрес: 172.23.182.133, порт: 3128.\n"
                                                             "* Для вставки текста используйте: Ctrl + V")
        bot.send_message(message.chat.id, "Готово!")

        def ask_windows_subproblem(message):
            """Спрашивает под-проблему с прокси Windows."""
            keyboard = create_keyboard([
                "5.1 Выключается монитор",
                "5.2 Другая проблема (опишите подробно)"
            ])
            bot.send_message(message.chat.id, "Что у вас с монитором? ", reply_markup=keyboard)

        @bot.message_handler(func=lambda message: message.text in ["5.1 Выключается монитор", "5.2 Другая проблема (опишите подробно)"])
        def handle_windows_subproblem(message):
            subproblem_text = message.text
            user_data[message.chat.id]['problem'] = subproblem_text
            user_data[message.chat.id]['detailed_problem'] = subproblem_text
            if subproblem_text == "5.1 Выключается монитор":
                bot.send_message(message.chat.id, "Обычно монитор перестает работать от того, что просто отошел один или два провода от него. "
                                                  "Один провод дает электрическое питание для монитора, "
                                                  "а другой связывает системный блок и выдает картинку на экран.")
                bot.send_message(message.chat.id, "Необходимо проверить оба провода с двух концов. Нужно чтобы они крепко были подключены к своим гнездам.")
                bot.send_photo(message.chat.id, PHOTO_68_ID, caption="Примеры того, как они выглядят:")
                bot.send_photo(message.chat.id,PHOTO_69_ID)
            elif subproblem_text == "5.2 Другая проблема (опишите подробно)":
                bot.send_message(message.chat.id, "")
    ask_solution_status(message)


def ask_solution_status(message):
    """Спрашивает, решена ли проблема."""
    keyboard = create_keyboard(["Да, решил", "Нет, не решил"])
    msg = bot.send_message(message.chat.id, "Я решил вашу проблему?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, handle_solution_status)


def handle_solution_status(message, is_solved=None):
    """Обрабатывает ответ о решении проблемы."""
    response = message.text
    if response == "Да, решил":
        bot.send_message(message.chat.id, "Отлично! Рад был помочь. Если возникнут еще проблемы, обращайтесь.",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        del user_data[message.chat.id]
    elif response == "Нет, не решил" or is_solved is False:
        user_info = user_data.get(message.chat.id, {})

        name = user_info.get('name', 'Не указано')
        internal_number = user_info.get('internal_number', 'Не указан')
        workplace = user_info.get('workplace', 'Не указано')

        problem_description = user_info.get('detailed_problem', user_info.get('problem', 'Не указана'))

        department = user_info.get('department')
        if department == "Входящая Линия":
            support_message = (
                f"Новая заявка на помощь от Входящей Линии:\n"
                f"Имя сотрудника: {name}\n"
                f"Внутренний номер: {internal_number}\n"
                f"Рабочее место: {workplace}\n"
                f"Проблема: {problem_description}"
            )
        else:
            support_message = (
                f"Новая заявка на помощь:\n"
                f"Отдел: {department}\n"
                f"Имя сотрудника: {name}\n"
                f"Рабочее место: {workplace}\n"
                f"Проблема: {problem_description}"
            )

        bot.send_message(TECH_SUPPORT_CHAT_ID, support_message)

        bot.send_message(message.chat.id,
                         "Заявка на помощь отправлена специалистам. Ожидайте, они скоро к вам подойдут.",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        del user_data[message.chat.id]
    else:
        ask_solution_status(message)


def get_workplace(message):
    """Получает рабочее место."""
    user_data[message.chat.id]['workplace'] = message.text
    ask_main_problem(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)