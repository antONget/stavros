import gspread
from datetime import datetime, date
# import pandas as pd

gp = gspread.service_account(filename='stavros.json')
#Open Google spreadsheet
gsheet = gp.open("Stavros")
#Select worksheet
wsheet = gsheet.worksheet("Заявка на обратную связь")
catalog = gsheet.worksheet("Скачивание каталогов")
start = gsheet.worksheet("/start")
# получить все значения
# wsheet.get_all_values()


# добавить значения
def append_name(ID, name):
    wsheet.append_row([ID, name])

# добавить значения
def append_start(ID, user_name, data):
    start.append_row([ID, user_name, data])

# добавить значения
def append_catalog(ID, date, name_catalog):
    catalog.append_row([ID, date, name_catalog])


# поиск строки и столбца положения значения
def values_row_col(value):
    values = wsheet.get_all_values()
    res = []
    for i, r in enumerate(values):
        for j, c in enumerate(r):
            if str(value) in c:
                res.append({'row': i, 'col': j})
    return res

# добавления значения
def update_phone(message):
    ID = message.chat.id
    res = values_row_col(ID)
    row = res[-1]["row"]+1
    if message.contact != None:
        phone = message.contact.phone_number
    else:
        phone = message.text
    wsheet.update(f'C{row}', phone)

def diff_days(day):
    now = datetime.now()
    today = now.strftime("%d/%m/%Y")
    t = today.split('/')[::-1]
    t = list(map(int, t))
    d = day.split('/')[::-1]
    d = list(map(int, d))
    return abs(date(t[0], t[1], t[2]) - date(d[0], d[1], d[2])).days



def get_stat():
    c = catalog.get_all_values()
    s = start.get_all_values()

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
    res = {
        name_1: {"all": set(), "mounth": set()},
        name_2: {"all": set(), "mounth": set()},
        name_3: {"all": set(), "mounth": set()},
        name_4: {"all": set(), "mounth": set()},
        name_5: {"all": set(), "mounth": set()},
        name_6: {"all": set(), "mounth": set()},
        name_7: {"all": set(), "mounth": set()},
        name_9: {"all": set(), "mounth": set()},
        'start': {"all": set(), "mounth": set()},
    }
    # print("c: ", len(c), "s: ", len(s))
    for row_c in c[1:]:
        # print(row_c)
        for key in res.keys():
            # print(row_c[2], ' == ', key)
            if row_c[2] == key:
                # print(type(res[key]["all"]))
                res[key]["all"].add(row_c[0])
                # print('add_all')
                if diff_days(row_c[1]) < 32:
                    res[key]["mounth"].add(row_c[0])
                    # print('add_month')
    for row_s in s:
        # print(row_s)
        res['start']['all'].add(row_s[0])
        if diff_days(row_s[2]) < 32:
            res['start']['mounth'].add(row_s[0])
    print(len(res[name_1]['all']))
    return res



if __name__ == '__main__':
    get_stat()
