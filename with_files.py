import csv
from datetime import datetime, timedelta


#  регистрация новах пользователей в файл
def start_registration(message, name):
    make_start_time = datetime.now()
    make_start_time += timedelta(hours=3)  # Перевод в Московское время
    make_start_time = make_start_time.strftime('%d.%m.%Y-%H:%M')
    with open('Data/MainFiles/list_registration.txt', 'a', encoding='utf-8') as f1:
        print(message.from_user.id, name, make_start_time, sep=';', file=f1)


# Принимает имя csv файла - возвращает вложенный список
def open_csv(file_name, delimiter=';', encoding='utf-8', heading=False):
    with open(file_name) as csv_file:
        rows = csv.reader(csv_file, delimiter=delimiter)
        lst = []
        for row in rows:
            lst.append(row)
        if not heading:
            lst = lst[1:]
        return lst


# Принимает № вопроса, № темы, src картинок и дозаписывает данные в файл
def record_data(number_question, number_topic, src_question, src_answer, course=3):
    with open(f'Data/Images_data/course_{course}_topic_{number_topic}', 'a') as f1:
        print(number_question, number_topic, src_question, src_answer, sep=';', file=f1)


# Возвращает список глав в формате [номер курса, номер главы, название главы]
def get_list_topic():
    with open('Data/MainFiles/topic_list.txt') as f1:
        cont = f1.read().split('\n')
    return [x.split(';') for x in cont if x]


# Возвращает список номеров глав в файле Пользователя
def get_user_topic(user_id):
    try:
        with open(f'Data/UserFiles/topic_user_{user_id}') as f1:
            return f1.read().split('\n')
    except FileNotFoundError:
        return []


# Записывает в файл src карточки с текущем временем занесения
def add_user_topic(user_id, number_topic, course=3):
    with open(f'Data/UserFiles/topic_user_{user_id}', 'a') as f1:
        f1.write(number_topic)
    with open(f'Data/Images_data/course_{course}_topic_{number_topic}', 'r') as f2:
        cont = f2.read().split()
        images_list = [(x.split(';')[2], x.split(';')[3]) for x in cont]  # [(src_question, src_answer), ...]
    current_time = datetime.now()
    with open(f'Data/UserFiles/cards_user_{user_id}', 'a') as f3:
        for el in images_list:
            print(current_time, el[0], el[1], '0', sep=';', file=f3)


# Принимает  user_id - возвращает  user_name
def get_name(user_id):
    with open('Data/MainFiles/list_registration.txt', 'r', encoding='utf-8') as f1:
        cont = f1.readlines()
        cont = list(filter(lambda x: len(x.split(';')) == 3, cont))
        print(cont)
    return list(filter(lambda x: x.split(';')[0] == user_id, cont))[-1].split(';')[1]


# Считывает файл со стеком - возвращает первый элемент - остаток перезаписывает в файл
def get_card_from_stack(user_id):
    try:
        with open(f'Data/UserFiles/stack_user_{user_id}', 'r') as f1:
            cont = f1.read().split('\n')
        cont_list = [x for x in cont if x]
        row = cont_list.pop(0)
        with open(f'Data/UserFiles/stack_user_{user_id}', 'w') as f1:
            print(*cont_list, sep='\n', file=f1)
        return row
    except (FileNotFoundError, IndexError):
        get_card_for_stack(user_id)
        return get_card_from_stack(user_id)


# Считывае файл <<cards_user_{user_id}>> разделяет по критерию: 1я колонка >< текущего времени
def get_card_for_stack(user_id):
    pattern = '%Y-%m-%d %H:%M:%S.%f'
    print('user_id= ', user_id)
    with open(f'Data/UserFiles/cards_user_{user_id}', 'r') as f2:
        cont = f2.read().split('\n')
    to_stack, back_to_file = [], []
    current_time = datetime.now()
    with open(f'Data/UserFiles/stack_user_{user_id}', 'a') as f_stack, \
            open(f'Data/UserFiles/cards_user_{user_id}', 'w') as f_back:
        for el in cont:
            lst = el.split(';')
            if len(lst) in (3, 4):
                try:
                    lst_3 = lst[3]
                except IndexError:
                    lst_3 = 0
                dtime = datetime.strptime(lst[0], pattern)
                if current_time >= dtime:
                    print(lst[1], lst[2], lst_3, sep=';', file=f_stack)
                else:
                    back_to_file.append(el)
        print(*back_to_file, sep='\n', file=f_back)


# Дозаписывает карточку в файл со стеком
def return_card_to_stack(the_card, user_id):
    with open(f'Data/UserFiles/stack_user_{user_id}', 'a') as f_stack:
        f_stack.write(the_card)


# Дозаписывает карточку в файл с карточками изменяя дату от балов
def return_card_to_file(the_card_list, user_id):
    ball = int(the_card_list[2])
    ball += 1
    dtime = datetime.now() + timedelta(days=ball)
    with open(f'Data/UserFiles/cards_user_{user_id}', 'a') as f3:
        print(dtime, the_card_list[0], the_card_list[1], ball, sep=';', file=f3)
