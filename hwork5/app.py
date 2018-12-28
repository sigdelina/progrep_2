from flask import Flask
from flask import url_for, render_template, request
import os
import sqlite3
import re
from pymystem3 import Mystem
from itertools import groupby

# создание базы данных
def new_Datebase():
    con = sqlite3.connect("4search.db.sqlite")
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS alldata(link text, title text, ordinary text, lemma text, morph text)")
    # пути для обхода дерева папок
    start_path = './newspaper/plain/'
    start_path2 = './newspaper/mystem_lem/'
    start_path3 = './newspaper/mystem_plain/'
    # обход дерева папок, сравнение файлов
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if ".txt" in file:
                file_1 = file
                final = os.path.join(root, file_1)
                with open(final, 'r', encoding='utf-8') as filee:
                    data = filee.read()
                    title = re.search(r'@ti (.*)', data)
                    link = re.search(r'@url (.*)', data)
                    f_link = str(link.group(1))
                    f_title = str(title.group(1))
                    result_ncl = re.sub(r'@.*', '', data)
                    nneed = re.compile(r"[\n\t\r]", re.DOTALL)
                    result = nneed.sub(' ', result_ncl)
                    result = re.sub('  ', ' ', result)
                # сравнение названий файлов в папке 2 с папкой 1
                for root2, dirs2, files2 in os.walk(start_path2):
                    for file2 in files2:
                        if ".txt" in file2:
                            file_2 = file2
                            final2 = os.path.join(root2, file_2)
                            if file_2 == file_1:
                                with open(final2, 'r', encoding='utf-8') as fi:
                                    lemma_extra = fi.read()
                                    ex = re.compile(r"[,.?()!\":;«»^{}></|%$]", re.DOTALL)
                                    lemma_clean = ex.sub(' ', lemma_extra)
                                    lemma = re.sub('  ', ' ', lemma_clean)
                # сравнение названий файлов в папке 3 с папкой 1
                for root3, dirs3, files3 in os.walk(start_path3):
                    for file3 in files3:
                        if ".txt" in file3:
                            file_3 = file3
                            final3 = os.path.join(root3, file_3)
                            if file_3 == file_1:
                                with open(final3, 'r', encoding='utf-8') as fin:
                                    morfo = fin.read()
                                    cur.execute("INSERT INTO alldata VALUES (?, ?, ?, ?, ?)", (
                                                f_link, f_title,
                                                result.replace('\t', '').replace('\n', ''),
                                                lemma.replace('\t', '').replace('\n', ''),
                                                morfo))
    con.commit()
    con.close()  #закрываем БД
    return


new_Datebase()


app = Flask(__name__)


@app.route('/')  # главная страница
def general():
    if request.args:  # для введенного запроса
        search = request.args['search']
        search1 = str(search)
        # лемматизируем введенный запрос
        m = Mystem()
        lemmas = m.lemmatize(search)
        search = ''.join(lemmas)
        # открываем базу данных
        connection = sqlite3.connect('4search.db.sqlite')
        cursor = connection.cursor()
        # результат поиска в лемматизированном виде для поиска по БД
        res = "% " + str(search).replace('\n', '') + " %"
        result_cort = []
        phrase_1 = lemmas[0]
        the_end = []
        # поиск по БД
        for row in cursor.execute("SELECT link, title, ordinary, lemma FROM alldata WHERE lemma LIKE ?",(res,)):
            # заносим все строки в список
            result_cort.append(row)
            # список слов в лемматизированных текстах
            words = row[3].split()
            # список слов в обычных текстах
            part = row[2].split()
            for word in words:
                # для слова: <= 2 т. к. в lemmas есть '\n'
                if len(lemmas) <= 2:
                    if word == phrase_1:
                        # номер элемента в списке
                        num = words.index(word)
                        # новый срез списка
                        if num - 35 <= 0 and len(part) >= num + 35:
                            new = part[0:num+35]
                        elif num - 35 <= 0 and len(part) < 35:
                            new = part[0:len(part)]
                        elif num - 35 > 0 and len(part) >= num + 35:
                            new = part[num-35:num+35]
                        elif num - 35 > 0 and len(part) < num + 35:
                            new = part[num-35:len(part)]
                        # строка для красивого вывода
                        fin = ''
                        for wlines in new:
                            fin += wlines + ' '
                        result = ''.join(fin)
                        end = (row[0], row[1], result)
                        # чтобы не повторялись элменты в списке
                        # делаем красивый вывод (как в Яндексе)
                        # т.е. 1 сслыка - несолько значений
                        the_end.append(end)
                        the_end = [good for good, _ in groupby(the_end)]
                # для фразы нет вывода по +- 35 слов,
                # т. к. не получилось аналогично искать по спискам
                else:
                    the_end = result_cort
        #  закрываем БД
        connection.close()
        return render_template('results.html', search1=search1, the_end=the_end)
    return render_template('general.html')


if __name__ == '__main__':
    app.run(debug=True)
