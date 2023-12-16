import telebot
from telebot.types import InputMediaPhoto
import keyboards
from config import token_bot, admin_ids
import googleSheets
from datetime import datetime

# 11:40
bot = telebot.TeleBot(token_bot)


@bot.message_handler(commands=['start'])
def get_start_help(message):
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    googleSheets.append_start(message.chat.id, message.chat.username, date)
    keyboard = keyboards.keyboard_start()
    bot.send_message(chat_id=message.chat.id,
                     text="Вас приветствует компания Stavros – ведущий российский производитель "
                            "комплектующих и декора для мебели и интерьеров. Самый большой ассортимент на рынке.\n\n"
                            "Познакомьтесь с нашим ассортиментом, скачав каталоги и узнайте выгодное персональное "
                            "предложение для каждой категории клиентов.",
                     reply_markup=keyboard)
    

@bot.message_handler(commands=['admin'], func=lambda message: message.chat.id in admin_ids)
def get_start_help(message):
    keyboard = keyboards.keyboard_stat()
    bot.send_message(chat_id=message.chat.id,
                     text="Вы являетесь админом и вам доступен расширенный функционал",
                     reply_markup=keyboard)


@bot.message_handler(commands=['admin'])
def get_start_help(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Вы не являетесь админом и вам не доступен расширенный функционал")
    

@bot.callback_query_handler(func=lambda call: call.data == "stat")
def callback_catalog(call):
    name_1 = "Современная коллекция"
    name_2 = "Молдинги"
    name_3 = "Неоклассика"
    name_4 = "Новая коллекция"
    name_5 = "Мебельные ножки, классическая коллекция"
    name_6 = "Мебельные ножки, современная коллекция"
    name_7 = "Мебельные ручки"
    name_8 = "ЕВРОПЕЙСКИЕ МЕБЕЛЬНЫЕ РУЧКИ"
    name_9 = "Весь декор"
    name_10 = "ДЕКОР ИЗ ПОЛИУРЕТАНА"
    res = googleSheets.get_stat()
    bot.send_message(chat_id=call.message.chat.id,
                     text=f'<b>Количество скачиваний каталогов</b> \n\n (всего/за последний месяц):\n'
                          f'1.{name_1} - {len(res[name_1]["all"])}/{len(res[name_1]["mounth"])}\n'
                          f'2.{name_2} - {len(res[name_2]["all"])}/{len(res[name_2]["mounth"])}\n'
                          f'3.{name_3} - {len(res[name_3]["all"])}/{len(res[name_3]["mounth"])}\n'
                          f'4.{name_4} - {len(res[name_4]["all"])}/{len(res[name_4]["mounth"])}\n'
                          f'5.{name_5} - {len(res[name_5]["all"])}/{len(res[name_5]["mounth"])}\n'
                          f'6.{name_6} - {len(res[name_6]["all"])}/{len(res[name_6]["mounth"])}\n'
                          f'7.{name_7} - {len(res[name_7]["all"])}/{len(res[name_7]["mounth"])}\n'
                          f'8.{name_9} - {len(res[name_9]["all"])}/{len(res[name_9]["mounth"])}\n\n' 
                          f'Запуск бота\n'
                          f'(всего/за последний месяц): - {len(res["start"]["all"])}/{len(res["start"]["mounth"])}',
                     parse_mode='html')
    


# обработка отправленного контакта
@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:  # Если присланный объект <strong>contact</strong> не равен нулю
        bot.register_next_step_handler(message, googleSheets.update_phone)
        contact_finish(message)


# Отправляем пользователю file_id
@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    photo_id=message.photo[3].file_id
    file_info = bot.get_file(photo_id)
    print(photo_id) # Выводим file_id
    print(f'http://api.telegram.org/file/bot{token_bot}/{file_info.file_path}')


def send_album_with_text():
    print('send_album_with_text')
    pic1 = open("catalog_preview/1.png", "rb")
    pic1_id = "AgACAgIAAxkBAAIBcWVt-Vw_W5Q67Zw9Nuod8vIAAWFh3wAC_tExGxvbcUuUHL50snfpegEAAwIAA3kAAzME"
    pic1_linkpath = "http://api.telegram.org/file/bot6469133428:AAGNVYWtBhl8HZrFv0t4hx1dXCs0t693t1Q/photos/file_0.jpg"
    pic2 = open("catalog_preview/2.png", "rb")
    pic2_id = "AgACAgIAAxkBAAIBcmVt-e6NAAHk8q_6ToGLsn5OJ6E5fwACCdIxGxvbcUt3JkszKbw-GwEAAwIAA3gAAzME"
    pic2_linkpath = "http://api.telegram.org/file/bot6469133428:AAGNVYWtBhl8HZrFv0t4hx1dXCs0t693t1Q/photos/file_1.jpg"
    pic3 = open("catalog_preview/3.png", "rb")
    pic4 = open("catalog_preview/4.png", "rb")
    pic5 = open("catalog_preview/5.png", "rb")
    pic6 = open("catalog_preview/6.png", "rb")
    pic7 = open("catalog_preview/7.png", "rb")
    # pic8 = open("catalog_preview/8.png", "rb")
    pic9 = open("catalog_preview/9.png", "rb")
    # pic10 = open("catalog_preview/10.png", "rb")
    media = [InputMediaPhoto(pic7), InputMediaPhoto(pic6), InputMediaPhoto(pic1), InputMediaPhoto(pic5),
             InputMediaPhoto(pic9), InputMediaPhoto(pic2), InputMediaPhoto(pic4), InputMediaPhoto(pic3)]
    print('end send_album_with_text')
    return media


@bot.callback_query_handler(func=lambda call: call.data == "catalog")
def callback_catalog(call):
    print('callback_catalog')
    bot.clear_step_handler(call.message)
    bot.answer_callback_query(callback_query_id=call.id)
    media = send_album_with_text()
    bot.send_media_group(chat_id=call.message.chat.id, media=media)
    keyboard = keyboards.keyboard_catalog()
    bot.send_message(chat_id=call.message.chat.id,
                     text='Выберите каталог и скачайте, нажав на кнопку с его названием',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: 'cat_' in call.data)
def callback_catalog_download(call):
    print('callback_catalog_download')
    link_1 = "https://www.stavros.ru/upload/iblock/4ea/q1c3oa50oipjrh8pjqqt6vfoyoyi558f/Ruchki-mebelnye-STAVROS.pdf"
    link_2 = "https://www.stavros.ru/upload/iblock/ff3/hjs7o6yt86c3lpn029s76dhmes9pf4bv/Stavros_molding.pdf"
    link_3 = "https://www.stavros.ru/upload/iblock/6c4/c0l9yc8n5gd7c3o4o8szmixboazps9lh/Stavros_neoclassic.pdf"

    link_4 = "https://www.stavros.ru/upload/medialibrary/96b/vyh612s94y0ajnc6w5yibz59lzxyn7dh/Decor-collection-SUMMER-GARDEN.pdf"
    link_5 = "https://www.stavros.ru/upload/iblock/b51/pqx2p4befa1h4j0ac6ebun6ujtx39a1r/Stavros_legs_classic.pdf"
    link_6 = "https://www.stavros.ru/upload/iblock/eca/i98wupwrv4b9gl9xelxjfkpw4xhn7u6p/Stavros%20legs_temporary.pdf"
    link_7 = "https://www.stavros.ru/upload/iblock/4ea/q1c3oa50oipjrh8pjqqt6vfoyoyi558f/Ruchki-mebelnye-STAVROS.pdf"
    link_8 = "https://www.stavros.ru/upload/iblock/fba/yb3nwy7upgg9u8n59c5y6xv8w0d1bgc6/Katalog-EVROPEYSKIE-MEBELNYE-RUCHKI.pdf"
    link_9 = "https://www.stavros.ru/upload/iblock/9ef/4zlp91158b0ofuaggu3xz59xg10glhcs/Catalog-decor.pdf"
    link_10 = "https://www.stavros.ru/upload/iblock/09f/95h0n1pmjgfoofhxya0ir1llxcduez6s/Stavros_catalog-decor_PU.pdf"
    bot.answer_callback_query(callback_query_id=call.id)
    description_1 = "В современной коллекции мы объединили минималистичные модели" \
                    " декора и мебельные комплектующие для декорирования и" \
                    " персонализации интерьера в соответствии с актуальными" \
                    " дизайнерскими тенденциями. В ассортименте мебельные каркасы," \
                    " ножки, ручки, рамы для зеркал, погонажные изделия из массива и ПУ."
    description_2 = "Молдинги – простые по форме детали с большими возможностями" \
                    " для декорирования. Уникальность профилированных" \
                    " молдингов Stavros – в комплиментарности с другими элементами" \
                    " декора. В сочетании с соединительными угловыми и центральными" \
                    " накладками можно создавать множество вариантов стильных" \
                    " декоративных оформлений для стен, дверей и мебели."
    description_3 = "Встречайте новый каталог «НЕОКЛАССИКА» от Stavros.\n" \
                    "Мы собрали для Вас лучшие образцы интерьеров с применением продукции Stavros. " \
                    "Вечная классика в новом прочтении, в сочетании с последними трендами 2021 " \
                    "звучит свежо и актуально. Применяйте декор Stavros по-новому!"
    description_4 = "В 2023 году коллекция «Летний сад» в духе французского барокко " \
                    "стала очень популярной, благодаря эксклюзивному дизайну и " \
                    "вариативности комбинаций моделей.\n " \
                    "Все элементы легко сочетаются между собой, позволяя создавать " \
                    "множество стильных сюжетов для оформления мебели и интерьеров."
    description_5 = "Уже 20 лет наша фабрика производит ножки из ценных пород древесины для" \
                    " различных видов мебели. В ассортименте более 100 моделей " \
                    "классических стилей, отличающихся эталонным качеством и дизайном:" \
                    " ножки кабриоль, точеные с каннелюрами, гладкие и украшенные" \
                    " нарядной резьбой."
    description_6 = "Уже 20 лет наша фабрика производит ножки из ценных пород древесины" \
                    " для различных видов мебели. В ассортименте более 100 моделей," \
                    " отличающихся актуальным дизайном и эталонным качеством."
    description_7 = "В современной коллекции мебельных ручек Stavros стильные " \
                    "дизайнерские модели из массива бука и дуба: врезные и накладные, " \
                    "кнопки, ракушки, П-образные (скоба), ручки длиной более 1 м"
    description_8 = "Компания STAVROS предлагает ассортимент мебельных ручек " \
                    "ведущих европейских брендов из Италии, Испании, Бельгии и Польши."
    description_9 = "Сегодня Stavros – лидер в сфере производства резного декора из дерева, символизирующий эталонное качество и хороший вкус.\n\n" \
                    "В ассортименте все виды классических моделей: декоративные кронштейны, капители, розетки, погонаж, накладки и маскароны."
    description_10 = "Добавить описание - Описание каталога"
    name_1 = "Современная коллекция"
    name_2 = "Молдинги"
    name_3 = "Неоклассика"
    name_4 = "Новая коллекция"
    name_5 = "Мебельные ножки, классическая коллекция"
    name_6 = "Мебельные ножки, современная коллекция"
    name_7 = "Мебельные ручки"
    name_8 = "ЕВРОПЕЙСКИЕ МЕБЕЛЬНЫЕ РУЧКИ"
    name_9 = "Весь декор"
    name_10 = "ДЕКОР ИЗ ПОЛИУРЕТАНА"
    description = ''
    link = ''
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    print(date)
    if call.data.split('_')[1] == '1':
        print('document 1')
        link = f"<a href='{link_1}'>{name_1}</a>"
        description = description_1
        googleSheets.append_catalog(call.message.chat.id, date, name_1)
    elif call.data.split('_')[1] == '2':
        print('document 2')
        link = f"<a href='{link_2}'>{name_2}</a>"
        description = description_2
        googleSheets.append_catalog(call.message.chat.id, date, name_2)
    elif call.data.split('_')[1] == '3':
        print('document 3')
        link = f"<a href='{link_3}'>{name_3}</a>"
        description = description_3
        googleSheets.append_catalog(call.message.chat.id, date, name_3)
        print('document 3 - end')
    elif call.data.split('_')[1] == '4':
        print('document 4')
        link = f"<a href='{link_4}'>{name_4}</a>"
        description = description_4
        googleSheets.append_catalog(call.message.chat.id, date, name_4)
    elif call.data.split('_')[1] == '5':
        print('document 5')
        link = f"<a href='{link_5}'>{name_5}</a>"
        description = description_5
        googleSheets.append_catalog(call.message.chat.id, date, name_5)
    elif call.data.split('_')[1] == '6':
        print('document 6')
        link = f"<a href='{link_6}'>{name_6}</a>"
        description = description_6
        googleSheets.append_catalog(call.message.chat.id, date, name_6)
    elif call.data.split('_')[1] == '7':
        print('document 7')
        link = f"<a href='{link_7}'>{name_7}</a>"
        description = description_7
        googleSheets.append_catalog(call.message.chat.id, date, name_7)
    elif call.data.split('_')[1] == '8':
        print('document 8')
        link = f"<a href='{link_8}'>{name_8}</a>"
        description = description_8
        googleSheets.append_catalog(call.message.chat.id, date, name_8)
    elif call.data.split('_')[1] == '9':
        print('document 9')
        link = f"<a href='{link_9}'>{name_9}</a>"
        description = description_9
        googleSheets.append_catalog(call.message.chat.id, date, name_9)
    elif call.data.split('_')[1] == '10':
        print('document 10')
        link = f"<a href='{link_10}'>{name_10}</a>"
        description = description_10
        googleSheets.append_catalog(call.message.chat.id, date, name_10)

    bot.send_message(chat_id=call.message.chat.id, text='Ваш каталог: '+link+'\n\n'+description, parse_mode='HTML')
    # bot.send_message(chat_id=call.message.chat.id, text=description)
    keyboard = keyboards.keyboard_catalog_finish()
    bot.send_message(chat_id=call.message.chat.id,
                     text="Для оформления заказа ознакомьтесь с условиями или свяжитесь с менеджером",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "sale")
def callback_sale(call):
    print('callback_sale')
    bot.clear_step_handler(call.message)
    bot.answer_callback_query(callback_query_id=call.id)
    keyboard = keyboards.keyboard_sale_v1()
    bot.send_message(chat_id=call.message.chat.id,
                     text="В Stavros действуют выгодные условия для разных категорий заказчиков.\n\n"
                          "Чтобы узнать про систему скидок, напишите цифру к какой категории вы себя относите:\n\n"
                          "1. Дизайнер\n"
                          "2. Столярная мастерская/строительство\n" 
                          "3. Мебельная компания\n" 
                          "4. Крупная мебельная фабрика\n"
                          "5. Частное лицо",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "dizainer")
def callback_sale_dizainer(call):
    print('callback_sale_dizainer')
    bot.answer_callback_query(callback_query_id=call.id)
    keyboard = keyboards.keyboard_sale_finish()
    bot.send_message(chat_id=call.message.chat.id,
                     text="Вы - дизайнер, архитектор или декоратор?\n\n "
                          "Для Вас:\n\n"
                            "•   База 3D моделей и чертежи DWG\n"
                            "•   Печатные и электронные каталоги\n"
                            "•   Персональный менеджер\n"
                            "•   Шоу-румы в Москве и Петербурге\n"
                            "•   Экскурсия по производству.\n\n"
                            "👉🏻 Скидка 10% на все изделия")
    bot.send_message(chat_id=call.message.chat.id,
                     text="Если вы еще не определились с заказом откройте раздел «Скачать каталог»,"
                          " чтобы ознакомиться с нашей продукцией.\n\n" 
                          "Чтобы оформить заказ или задать вопрос нажмите «Связаться с менеджером».",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "stolyr")
def callback_sale_stolyr(call):
    print('callback_sale_stolyr')
    bot.answer_callback_query(callback_query_id=call.id)
    keyboard = keyboards.keyboard_sale_finish()
    bot.send_message(chat_id=call.message.chat.id,
                     text="У вас столярная мастерская, занимаетесь строительством, ремонтом или производством?\n\n"
                            "Для вас:\n\n"
                            "•   Отгрузка от 1 шт. по всей России\n"
                            "•   Гарантия и чёткое соблюдение сроков\n"
                            "•   Персональный менеджер\n\n"
                            "Скидки на изделия:\n\n"
                            "- 10% при заказе 15.000₽ – 29.999₽\n"
                            "- 15% при заказе 30.000₽ – 99.999₽\n"
                            "- 20% при заказе от 100.000₽\n\n"
                            "- 20% на образцы\n"
                            "- 40% на изделия из полирутена")
    bot.send_message(chat_id=call.message.chat.id,
                     text="Если вы еще не определились с заказом откройте раздел «Скачать каталог»,"
                          " чтобы ознакомиться с нашей продукцией.\n\n" 
                          "Чтобы оформить заказ или задать вопрос нажмите «Связаться с менеджером».",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "mebel")
def callback_sale_mebel(call):
    print('callback_sale_mebel')
    bot.answer_callback_query(callback_query_id=call.id)
    keyboard = keyboards.keyboard_sale_finish()
    bot.send_message(chat_id=call.message.chat.id,
                     text="Вы - крупная мебельная фабрика?\n\n"
                            "Для вас:\n\n"
                            "• Самый большой ассортимент декора и комплектующих для мебели\n"
                            "• Любой объем продукции в кратчайшие сроки с гарантией качества\n"
                            "• Шоу-румы в Москве и Санкт-Петербурге для личного знакомства\n"
                            "• Персональный менеджер\n\n"
                            "Скидки на изделия:\n\n"
                            "• 15% на все изделия\n "
                            "• 20% на образцы.\n"
                            "• 40% на изделия из полиуретана")
    bot.send_message(chat_id=call.message.chat.id,
                     text="Если вы еще не определились с заказом откройте раздел «Скачать каталог»,"
                          " чтобы ознакомиться с нашей продукцией.\n\n" 
                          "Чтобы оформить заказ или задать вопрос нажмите «Связаться с менеджером».",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "diler")
def callback_sale_diler(call):
    print('callback_sale_diler')
    bot.answer_callback_query(callback_query_id=call.id)
    keyboard = keyboards.keyboard_sale_finish()
    bot.send_message(chat_id=call.message.chat.id,
                     text="Вы - торговая организация или дилер?\n\n"
                          "Для вас:\n\n"
                          "• Самый большой ассортимент декора и мебельных комплектующих на рынке от ведущего"
                          " лидера отрасли.\n" 
                          "• Скидка на образцы продукции и экспозиционные стенды.\n" 
                          "• Отгрузка заказов от 1 шт. с доставкой по всей России.\n" 
                          "• Персональный менеджер.\n"
                          "• Шоу-румы в Москве и Санкт-Петербурге для личного знакомства.\n\n" 
                          "Скидки на продукцию, если вы работаете без НДС:\n\n"
                          "• 20% на все заказы из массива и МДФ.\n"
                          "• 20% на образцы.\n" 
                          "• 30% на деревянные ручки.\n" 
                          "• 40% на образцы ручек.\n\n" 
                          "Скидка на изделия из ПУ устанавливается индивидуально.\n\n"
                          "С НДС скидка на изделия из массива, МДФ и ПУ устанавливается индивидуально.\n"
                          "Скидка на деревянные ручки и все образцы составит 3%.")
    bot.send_message(chat_id=call.message.chat.id,
                     text="Если вы еще не определились с заказом откройте раздел «Скачать каталог»,"
                          " чтобы ознакомиться с нашей продукцией.\n\n" 
                          "Чтобы оформить заказ или задать вопрос нажмите «Связаться с менеджером».",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "chastnik")
def callback_sale_chastnik(call):
    print('callback_sale_chastnik')
    bot.answer_callback_query(callback_query_id=call.id)
    keyboard = keyboards.keyboard_sale_finish()
    bot.send_message(chat_id=call.message.chat.id,
                     text="Вы – частное лицо и присматриваете изделия для себя?\n\n"
                            "Для вас:\n\n"
                            "• Самый большой ассортимент декора для мебели и интерьера\n"
                            "• Заказ товара от 1 шт. с доставкой по всей России\n"
                            "• Экспертная консультация и помощь в подборе\n"
                            "• Шоу-румы в Москве и Санкт-Петербурге для личного знакомства\n\n"
                            "Скидки на изделия:\n\n"
                            "• 3% при заказе 30.000₽ – 99.999₽\n"
                            "• 7% при заказе от 100.000₽")
    bot.send_message(chat_id=call.message.chat.id,
                     text="Если вы еще не определились с заказом откройте раздел «Скачать каталог»,"
                          " чтобы ознакомиться с нашей продукцией.\n\n" 
                          "Чтобы оформить заказ или задать вопрос нажмите «Связаться с менеджером».",
                     reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "company")
def callback_sale_company(call):
    print('callback_sale_company')
    bot.answer_callback_query(callback_query_id=call.id)
    keyboard = keyboards.keyboard_sale_finish()
    bot.send_message(chat_id=call.message.chat.id,
                     text="У вас компания по производству мебели?\n\n"
                            "Для вас:\n\n"
                            "• Персональный менеджер.\n"
                            "• Отгрузка товара от 1 шт. по всей России\n"
                            "• Гарантия и чёткое соблюдение сроков.\n\n"
                            "Скидки на изделия:\n\n"
                            "- 10% при заказе 15.000₽ – 29.999₽\n"
                            "- 15% при заказе 30.000₽ – 99.999₽\n"
                            "- 20% при сумме заказа от 100.000₽\n\n"
                            "- 20% на образцы.\n"
                            "- 40% на изделия из полиуретана")
    bot.send_message(chat_id=call.message.chat.id,
                     text="Если вы еще не определились с заказом откройте раздел «Скачать каталог»,"
                          " чтобы ознакомиться с нашей продукцией.\n\n" 
                          "Чтобы оформить заказ или задать вопрос нажмите «Связаться с менеджером».",
                     reply_markup=keyboard)

# 14:10
@bot.callback_query_handler(func=lambda call: call.data == "connect")
def callback_connect(call):
    print('callback_connect')
    bot.clear_step_handler(call.message)
    bot.answer_callback_query(callback_query_id=call.id)
    keyboard = keyboards.keyboard_connect()
    bot.send_message(chat_id=call.message.chat.id,
                     text="У вас возникли вопросы, требуется помощь в подборе моделей декора или вы уже готовы сделать заказ?\n"
                          "Наши менеджеры рады помочь вам с пн по пт: с 09:00 до 18:00.\n"
                          "Ваше обращение, оставленное в другое время, не останется без нашего внимания."
                          " Мы ответим на него в рабочие часы.",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "call_me")
def callback_connect_call_me(call):
    print('callback_connect_call_me')
    bot.answer_callback_query(callback_query_id=call.id)
    msg = bot.send_message(chat_id=call.message.chat.id,
                     text="Укажите свое имя")
    bot.register_next_step_handler(msg, get_contact)

def get_contact(message):
    googleSheets.append_name(message.chat.id, message.text)
    keyboard = keyboards.contact_keyboard()
    msg = bot.send_message(message.chat.id, text='Укажите ваш номер телефона или поделитесь им через кнопку', reply_markup=keyboard)
    bot.register_next_step_handler(msg, contact_finish)

def contact_finish(message):
    googleSheets.update_phone(message)
    bot.send_message(message.chat.id, text='Спасибо! Наш менеджер свяжется с Вами в ближайшее время!')


if __name__ == '__main__':
    while True:
        try:
            bot.polling()
        except:
            continue
