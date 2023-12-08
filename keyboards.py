from telebot import types


def keyboard_start():
     # наша клавиатура
    key_catalog = types.InlineKeyboardButton(text='Скачать каталог', callback_data='catalog', color='blue')
    key_sale = types.InlineKeyboardButton(text='Скидки и акции', callback_data='sale')
    key_connect = types.InlineKeyboardButton(text='Связаться с менеджером', callback_data='connect')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(key_catalog)
    keyboard.add(key_sale, key_connect)
    return keyboard


def keyboard_catalog():
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_1 = types.InlineKeyboardButton(text='Современный декор', callback_data='cat_1')
    key_2 = types.InlineKeyboardButton(text='Молдинги', callback_data='cat_2')
    key_3 = types.InlineKeyboardButton(text='Неоклассика', callback_data='cat_3')
    key_4 = types.InlineKeyboardButton(text='Новая коллекция', callback_data='cat_4')
    key_5 = types.InlineKeyboardButton(text='Классические ножки', callback_data='cat_5')
    key_6 = types.InlineKeyboardButton(text='Современные ножки', callback_data='cat_6')
    key_7 = types.InlineKeyboardButton(text='Мебельные ручки', callback_data='cat_7')
    # key_8 = types.InlineKeyboardButton(text='Европейские мебельные ручки', callback_data='cat_8')
    key_9 = types.InlineKeyboardButton(text='Весь декор', callback_data='cat_9')
    # key_10 = types.InlineKeyboardButton(text='Декор из полиуретана', callback_data='cat_10')
    keyboard.add(key_7, key_6)
    keyboard.add(key_1, key_5)
    keyboard.add(key_9, key_2)
    keyboard.add(key_4, key_3)
    # keyboard.add(key_9, key_10)
    return keyboard


def keyboard_catalog_finish():
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_sale = types.InlineKeyboardButton(text='Скидка для вас', callback_data='sale')
    key_connect = types.InlineKeyboardButton(text='Связаться с менеджером', callback_data='connect')
    keyboard.add(key_sale, key_connect)
    return keyboard

def keyboard_sale():
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_dizainer = types.InlineKeyboardButton(text='Дизайнер', callback_data='dizainer')
    key_stolyr = types.InlineKeyboardButton(text='Столярная мастерская/строительство', callback_data='stolyr')
    key_cpmpany = types.InlineKeyboardButton(text='Мебельная компания', callback_data='company')
    key_mebel = types.InlineKeyboardButton(text='Крупная мебельная фабрика', callback_data='mebel')
    key_diler = types.InlineKeyboardButton(text='Торгующая организация/дилер', callback_data='diler')
    key_chastnik = types.InlineKeyboardButton(text='Частное лицо', callback_data='chastnik')
    keyboard.add(key_dizainer)
    keyboard.add(key_stolyr)
    keyboard.add(key_cpmpany)
    keyboard.add(key_mebel)
    # keyboard.add(key_diler)
    keyboard.add(key_chastnik)
    return keyboard


def keyboard_sale_finish():
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_catalog = types.InlineKeyboardButton(text='Скачать каталог', callback_data='catalog')
    key_connect = types.InlineKeyboardButton(text='Связаться с менеджером', callback_data='connect')
    keyboard.add(key_catalog, key_connect)
    return keyboard


def keyboard_connect():
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_catalog = types.InlineKeyboardButton(text='Написать в телеграм', url='https://t.me/stsavros')
    key_sale = types.InlineKeyboardButton(text='Написать в whatsapp', url='https://wa.me/79215791235?'
                                                                          'text=%D0%9F%D0%B8%D1%88%D1%83%20%D0%B2%D0%B0%D0%BC%20%D0%B8%D0%B7%20%D0%B1%D0%BE%D1%82%D0%B0%20stavros!')
    key_connect = types.InlineKeyboardButton(text='Заказать обратный звонок', callback_data='call_me')
    keyboard.add(key_catalog)
    keyboard.add(key_sale, key_connect)
    return keyboard


def contact_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) #Подключаем клавиатуру
    button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True) #Указываем название кнопки, которая появится у пользователя
    keyboard.add(button_phone) #Добавляем эту кнопку
    return keyboard