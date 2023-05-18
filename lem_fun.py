r"""Функции и крткое описание:

append_zero - добовление в начале ИНН и ОКПО нуля

connect_table - сбор одинаковых таблиц в одну большую

snils_zero - добавление нуля в начале в СНИЛСе

inn_int - столбец ИНН приводится к формату INT, доступен вызов функции append_zero

bins_label_for_data - разделение таблицы на группы (аналог функции ПРОСМОТР в Excel)

"""



# Необходимые бибилиотеки

import pandas as pd
import os
import datetime
import numpy as np
import string

pd.options.mode.chained_assignment = None # отключу предупреждения.


# Функция добавления нулей в начало инн и окпо

def append_zero(data_frame, inn, okpo = 0):
    r""" Описание:
        
Функция добоволения нуля в начале ИНН и ОКПО, чтобы соответствовать принятому формату написания.

data_frame - таблице, в которой нужно проверить ИНН

inn - столбец с ИНН

okpo - столбец с ОКПО, по умолчянию равен 0

data_frame - таблица с данными

Пример:

import pandas as pd

df = pd.read_excel или read_csv(r'') - открыть данные в зависимости от формата excel или csv

append_zero(data_frame = df, inn = 'ИНН', okpo = 'ОКПО')
  
"""
    
    if okpo != 0:
    
# Кол-во посчитаем кол-во символов
    
        data_frame[okpo] = (data_frame[okpo].replace("", np.nan, regex=True)
                       .fillna(0)
                       .astype('int64')
                      )

        data_frame[inn] = data_frame[inn].astype('str')
        data_frame[okpo] = data_frame[okpo].astype('str')#|S

        data_frame['inn_len'] = data_frame[inn].str.len()
        data_frame['okpo_len'] = data_frame[okpo].str.len()


# првидем ИНН и ОКПО к нужному кол-ву символов

        data_frame.loc[data_frame['inn_len'] == 9, inn] = '0' + data_frame[inn]
        data_frame.loc[data_frame['inn_len'] == 11, inn] = '0' + data_frame[inn]
        
        data_frame.loc[data_frame['okpo_len'] == 4, okpo] = '0000' + data_frame[okpo]
        data_frame.loc[data_frame['okpo_len'] == 5, okpo] = '000' + data_frame[okpo]
        data_frame.loc[data_frame['okpo_len'] == 6, okpo] = '00' + data_frame[okpo]
        data_frame.loc[data_frame['okpo_len'] == 7, okpo] = '0' + data_frame[okpo]
        data_frame.loc[data_frame['okpo_len'] == 9, okpo] = '0' + data_frame[okpo]

        data_frame = data_frame.drop(columns=['okpo_len', 'inn_len'], inplace=True)
    
    else:
        
# Кол-во посчитаем кол-во символов
        
        data_frame[inn] = data_frame[inn].astype('str')
        data_frame['inn_len'] = data_frame[inn].str.len()
        
# првидем ИНН и ОКПО к нужному кол-ву символов
        
        data_frame.loc[data_frame['inn_len'] == 9, inn] = '0' + data_frame[inn]
        data_frame.loc[data_frame['inn_len'] == 11, inn] = '0' + data_frame[inn]
        
        data_frame = data_frame.drop(columns=['inn_len'], inplace = True)
        
        
# функция соединения таблиц
       
def connect_table():
    
    r""" Описание:
        
Функция сбора одинаковых таблиц из разных файлов в одну большую. В функцию нужно 
ввести все данные которые она запросит. Есть возможность сразу сохранить файл.

Функция возвращает две переменных, таблицу и список ошибок. В списке ошибок путь
к файлам, которые не добавился в таблицу.

Пример:
    
import pandas as pd

connect_table() 

или

df, err = connect_table()
  
"""
    now = datetime.datetime.now().strftime('%d-%m-%Y')
    
    print('Введите путь к файлам:')
    way = r'{}'.format(input())
    
    print()
    print('Введите номер строки шапки таблицы')
    print('Для файлов спарка это 3, остальные как правило 0')
    head = int(input())
    
    print()
    print('Сохарнить файл после объединения?')
    save_t = input('Введите да или нет:  ')
    
    if save_t == 'да':
        
        print()
        print('Введите куда сохранить')
        save = r'{}'.format(input())
    
        print()
    
        print('Введите имя сохраняемого файла:')
        nme = r'\{}_{}.xlsx'.format(input(),now)
        print()
        save = save + nme
    
    
    df = pd.DataFrame() # создаём пустую таблицу

    now = datetime.datetime.now().strftime('%d-%m-%Y')
    
    # Созадем переменную куда сложим путь к файлам 
    name_files = []
    
    for root, dirs, files in os.walk(way):
        for name in files:
            name_files.append(os.path.join(root, name))
            
    # Откроем все файла и объединим их в одну таблицу
    err = []

    for fs in range(len(name_files)):
        try:
            df = pd.concat([df, (pd.read_excel(name_files[fs], header=head))])
        
        except Exception as exc:
            err.append(name_files[fs])
            print(exc)
            
            
    # Удалим столбцы с пустыми значениями. (Если это данные спарка) 
    
    try:
        df['Наименование'] = df['Наименование'].replace(r'', np.nan, regex=True)
        df['Наименование'] = df['Наименование'].fillna(0)
        df = df.query('Наименование != 0')
        df = df.drop_duplicates(subset = 'Код налогоплательщика')
    except:
        print('Файлы не спарк')
        
     
    # выведем наличие ошибок
    print()
    print('------------------------------------------------------------------------')
    print()
    print('Наличие ошибок объединения таблиц:')
    
    if len(err) > 0:
        print()
        print('\t ВНИМАНИЕ ЕСТЬ ОШИБКИ ПРИ СОЕДИНЕНИИ ТАБЛИЦ')
    else:
        print()
        print('\t ОШИБОК НЕТ.')
    
    df = df.reset_index(drop=True) #обнулим индексы
    
    # Сохраним получившуюся таблицу
    
    if save_t == 'да':
                
        df.to_excel(save, index=False)
        print()
        print('Объединённый файл в формате xlsx сохранён')
    
    return df, err



# Функция добавления нуля к снилсу

def snils_zero(data_frame, snils):
    
    r""" Описание:
        
Функция добавлеяет к СНИЛСу в начале ноль

data_frame - таблица с данными

snils - столбец с номером СНИЛС 

Пример:
    
import pandas as pd

df = pd.read_excel или read_csv(r'') - открыть данные в зависимости от формата excel или csv

snils_zero(data_frame = df, snils = 'СНИЛС')
  
"""
    
    # Кол-во посчитаем кол-во символов у столбца СНИЛС
        
    data_frame[snils] = data_frame[snils].replace('[{}]'.format(string.punctuation), '', regex = True)
    data_frame[snils] = data_frame[snils].astype('str')
    data_frame['snils_len'] = data_frame[snils].str.len()

    
    # првидем СНИЛС к нужному кол-ву символов
        
    data_frame.loc[data_frame['snils_len'] == 9, snils] = '00' + data_frame[snils]
    data_frame.loc[data_frame['snils_len'] == 10, snils] = '0' + data_frame[snils]
        
    data_frame = data_frame.drop(columns=['snils_len'], inplace = True)

    
# функция чистки столбца инн от постаронних симоволов и добавление 0 в начле при необходимости


def inn_int(frame, inn_c, okpo = 0, app_zero = False):
    
    r""" Описание:
       
Функция приведения столбцов ИНН и ОКПО к формату INT, возможен вызов функции 
append_zero передав в значение app_zero = True

frame - таблица с данными

inn_c - столбец с ИНН

okpo - столбец с ОКПО

app_zero - использовать или нет функцию append_zero(). По умоляанию не использовать.

Пример:
    
import pandas as pd

df = pd.read_excel или read_csv(r'') - открыть данные в зависимости от формата excel или csv

inn_int(frame = df, inn_c = 'ИНН', okpo = 'ОКПО', app_zero = True)
  
"""
    
    if okpo != 0:
        
        frame[okpo] = frame[okpo].replace('[A-я{}]'.format(string.punctuation),'',
                                                            regex = True)
        
        frame[okpo] = frame[okpo].replace('', np.nan, regex = True).fillna(0)
        frame[okpo] = frame[okpo].replace('  ', np.nan, regex = True).fillna(0) 
        frame[okpo] = frame[okpo].replace('  ', np.nan, regex = True).fillna(0)
        
        frame[okpo] = frame[okpo].astype('int64')
    
    frame[inn_c] = frame[inn_c].replace('[A-я{}]'.format(string.punctuation),'',
                                                            regex = True) #убираем не допустимые символы
    
    frame[inn_c] = frame[inn_c].replace('', np.nan, regex = True).fillna(0) #заполним пустые ячейки 0
    frame[inn_c] = frame[inn_c].replace('  ', np.nan, regex = True).fillna(0)
    frame[inn_c] = frame[inn_c].replace('  ', np.nan, regex = True).fillna(0)
    #frame[inn_c] = frame[inn_c].astype('float64')
    
    frame[inn_c] = frame[inn_c].astype('int64') #приведём к нужном типу данных столбец
    
    # добавление 0 в начле при необходимости
    
    if app_zero == True:
        
        append_zero(data_frame = frame, inn = inn_c, okpo = okpo) #вызов функции добавления 0 в начале    
        

    
    
def bins_label_for_data(data, stop_bin, step_bin, start_bin = 0, start_label = 1, step_label = 1):
    
    r""" Описание:
        
Функция разделение таблицы по группам (аналог функции ПРОСМОТР в Excel):
    
data - таблица данных

start_bin - начальный индекс по умолчанию 0

stop_bin - конечный индекс кол-во строк нужно округлить до ближашего целого числа

step_bin - шаг, сколько должно быть строк в одной группе

Пример:

import pandas as pd

df = pd.read_excel или read_csv(r'') - открыть данные в зависимости от формата excel или csv

df['label'] = bins_label_for_data(data = df, stop_bin = 100, step_bin = 10, start_bin = 0, start_label = 1, step_label = 1)
  
"""
    
    bins  = []
    
    # Цикл создания интервала
    
    for i in range(start_bin, stop_bin, step_bin):
        bins.append(i)

    label = []
    
    # Цикл создания меток интервала
    
    for i in range(start_label, len(bins), step_label):
        label.append(i)
        
    # Проверка, что значений в интервал на 1 больше чем меток 
    
    if len(bins) - len(label) == 1:
        
        data1 = data.reset_index()
        data1['lable'] = pd.cut(data1['index'], bins = bins, labels = label, include_lowest=True)
        list_label = data1['lable'].to_list()
        return list_label
    
    else:
        print('Не сосзданы списки bins и label')    
    
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




