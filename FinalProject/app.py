# импортируем модули
from flask import Flask
from flask import url_for, render_template, request
import os
import sqlite3
import re
import json
from itertools import groupby
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import seaborn as sns
import random
from wordcloud import WordCloud


app = Flask(__name__)


def stop():  # cписок стоп-слов
    stop_file = './rus_stop.txt'
    with open(stop_file, 'r', encoding='utf-8') as fi:
        st_text = fi.read()
    stop_words = st_text.split()  # список
    return stop_words


# делаем облака слов
def clouds(stop_words):
    text_tv1 = ''
    text_tv = ''
    text_media1 = ''
    text_media = ''
    text_relations1 = ''
    text_relations = ''
    con = sqlite3.connect("posts.db")  # открываем базу данных
    c = con.cursor()
    # делаем строку из слова постов и комментов для телевидения
    for row in c.execute("SELECT * FROM tv"):
        text_tv1 += row[1] + " "
    for row in c.execute("SELECT * FROM comments_tv"):
        text_tv1 += row[1] + " "
    # удаляем стоп-слова
    just_words = re.findall(r'[а-я]+', text_tv1.lower())
    for word in just_words:
        if word not in stop_words:
            text_tv += word + ' '
    # делаем строку из слова постов и комментов для сми
    for row in c.execute("SELECT * FROM mass_media"):
        text_media1 += row[1] + " "
    for row in c.execute("SELECT * FROM comments_media"):
        text_media1 += row[1] + " "
    # удаляем стоп-слова
    just_words2 = re.findall(r'[а-я]+', text_media1.lower())
    for word in just_words2:
        if word not in stop_words:
            text_media += word + ' '
    # делаем строку из слова постов и комментов для отношений
    for row in c.execute("SELECT * FROM gender_relations"):
        text_relations1 += row[1] + " "
    for row in c.execute("SELECT * FROM comments_relations"):
        text_relations1 += row[1] + " "
    # удаляем стоп-слова
    just_words3 = re.findall(r'[а-я]+', text_relations1.lower())
    for word in just_words3:
        if word not in stop_words:
            text_relations += word + ' '
    con.close()
    #  облака слов
    cloud = WordCloud(background_color="white", max_words=60)
    # генерируем
    cloud.generate(text_tv)
    # визуализируем
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig("static/cloudwords1.png", dpi=200, fromat='png',
                bbox_inches='tight')
    cloud_2 = WordCloud(background_color="white", max_words=60)
    # генерируем
    cloud_2.generate(text_media)
    # визуализируем
    plt.imshow(cloud_2, interpolation='bilinear')
    plt.axis("off")
    plt.savefig("static/cloudwords2.png", dpi=200, fromat='png',
                bbox_inches='tight')

    cloud_3 = WordCloud(background_color="white", max_words=60)
    # генерируем
    cloud_3.generate(text_relations)
    # визуализируем
    plt.imshow(cloud_3, interpolation='bilinear')
    plt.axis("off")
    plt.savefig("static/cloudwords3.png", dpi=200, fromat='png',
                bbox_inches='tight')


# создаем облака
def for_Cloud():
    stopping = stop()
    cloud = clouds(stopping)


for_Cloud()


# приложение. Стартовая страница
@app.route('/')
def questionnaire():
    posts_id_1 = []
    posts_id_2 = []
    posts_id_3 = []
    con = sqlite3.connect("posts.db")  # открываем базу данных
    c = con.cursor()
    # достаем из бд нужные посты
    for row in c.execute("SELECT post_id, text_post,"
                         " lenght_post FROM mass_media"):
        if row[2] > 50:
            posts_id_3.append(row[1])
    for row in c.execute("SELECT post_id, text_post, lenght_post FROM tv"):
        if row[2] > 20:
            posts_id_2.append(row[1])
    for row in c.execute("SELECT post_id, text_post,"
                         " lenght_post FROM gender_relations"):
        if row[2] > 60 and row[2] < 100:
            posts_id_1.append(row[1])
    con.commit()
    con.close()
    # выбираем рандомный пост по критериям
    ques_1 = random.choice(posts_id_1)
    ques_2 = random.choice(posts_id_2)
    ques_3 = random.choice(posts_id_3)
    if request.args:
        con_2 = sqlite3.connect("answers.db")  # создаем базу данных
        c_2 = con_2.cursor()
        c_2.execute('CREATE TABLE IF NOT EXISTS answer'
                    '(name, age, language, city, gender,'
                    'education, question_1, question_2,'
                    'question_3)')
        name = request.args['name']
        age = request.args['age']
        lang = request.args['lang']
        gender = request.args['gender']
        city = request.args['city']
        study = request.args['study']
        quest_1 = request.args['quest_1']
        quest_2 = request.args['quest_2']
        quest_3 = request.args['quest_3']
        row = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'
        #  записываем данные в бд
        c_2.execute("INSERT INTO answer VALUES (?, ?, ?, ?, ?,"
                    "?, ?, ?, ?)", (name, age, lang, city, gender, study,
                                    quest_1, quest_2, quest_3))
        con_2.commit()
        con_2.close()
        # считаем проценты
        counter_an = 0
        if quest_1 == "отношения полов":
            counter_an += 1
        if quest_2 == "телеканал":
            counter_an += 1
        if quest_3 == "интернет-СМИ":
            counter_an += 1
        print(counter_an)
        if counter_an == 0:
            result_an = "Увы, Вы плохо разбираетесь в тематике сообществ ВК!"
        if counter_an == 1:
            result_an = "Вы разбираетесь в тематике сообществ, но не идеально!"
        if counter_an == 2:
            result_an = "Практически идеально!"
        if counter_an == 3:
            result_an = "Вы эксперт в определении тематики сообществ ВК!"
        return render_template('answer.html', name=name, age=age,
                               lang=lang, city=city, gender=gender,
                               study=study, quest_1=quest_1,
                               quest_2=quest_2, quest_3=quest_3,
                               result_an=result_an)
    return render_template('questions.html', ques_1=ques_1,
                           ques_2=ques_2, ques_3=ques_3)


@app.route('/json')  # создаем json-строку
def json_Res():
    fin = []
    con = sqlite3.connect("answers.db")  # открываем базу данных
    c = con.cursor()
    for row in c.execute("SELECT * FROM answer"):
        d = {"name": row[0], 'age': row[1], "lang": row[2],
             "city": row[3], "gender": row[4],
             'study': row[5], 'quest_1': row[6],
             'quest_2': row[7], "quest_3": row[8]}
        fin.append(d)
    con.close()
    json_string = json.dumps(fin[0:], ensure_ascii=False, indent=4)
    json_date = json.loads(json_string)
    # записываем json-строки в спец файл
    with open('json_info.json', 'w', encoding='utf-8') as f:
        json.dump(json_date, f, ensure_ascii=False, indent=4)
    # на страницу передеается json type(list)
    return render_template('json.html', json_date=json_date)


@app.route('/wordcloud')  # создаем страницу с облаками
def beautcloud():
    return render_template('clouds.html')


@app.route('/stats')  # страница со статистикой
def stat():
    con = sqlite3.connect("answers.db")  # открываем базу данных
    c = con.cursor()
    sex_list = ['женский', 'мужской']
    sex_1 = {}
    sex_2 = {}
    study = {}
    years = {}
    lang = 0
    city = 0
    mid = 0
    for per in sex_list:  # вытаскиваем людей по полу
        c.execute('SELECT * FROM answer WHERE gender=?', (str(per),))
        for_sex = c.fetchall()  # cписок из всех людей по одному полу
        for person in for_sex:  # пополняем длину комментария
            mid += 1
            if person[4] == "женский":
                if person[6] == "отношения полов":
                    if person[6] in sex_1:
                        sex_1[person[6]] += 1
                    else:
                        sex_1[person[6]] = 1
                if person[7] == "телеканал":
                    if person[7] in sex_1:
                        sex_1[person[7]] += 1
                    else:
                        sex_1[person[7]] = 1
                if person[8] == "интернет-СМИ":
                    if person[8] in sex_1:
                        sex_1[person[8]] += 1
                    else:
                        sex_1[person[8]] = 1
            else:
                if person[6] == "отношения полов":
                    if person[6] in sex_2:
                        sex_2[person[6]] += 1
                    else:
                        sex_2[person[6]] = 1
                if person[7] == "телеканал":
                    if person[7] in sex_2:
                        sex_2[person[7]] += 1
                    else:
                        sex_2[person[7]] = 1
                if person[8] == "интернет-СМИ":
                    if person[8] in sex_2:
                        sex_2[person[8]] += 1
                    else:
                        sex_2[person[8]] = 1
            if person[2] == "русский":
                lang += 1
            if person[3] == "Москва и МО":
                city += 1
    for row in c.execute("SELECT * FROM answer"):  # добавляем параметры
        if row[5] in study:
            study[row[5]] += 1
        else:
            study[row[5]] = 1
        if row[1] in years:
            years[row[1]] += 1
        else:
            years[row[1]] = 1
    rus_lang = round((lang/mid)*100, 1)
    mos_city = round((city/mid)*100, 1)
    con.close()
    # данные по осям y и x
    style.use('ggplot')  # задаем стиль
    female_nums = [c[1] for c in sorted(sex_1.items(),
                                        key=lambda x: x[1], reverse=True)]
    female_labs = [c_1[0] for c_1 in sorted(sex_1.items(),
                                            key=lambda x: x[1], reverse=True)]
    colors = sns.color_palette('magma')  # цветовая гамма
    plt.figure(figsize=(20, 10), dpi=200)  # размер графика
    plt.bar(female_labs, female_nums, color=colors)  # график
    for a, b in zip(female_labs, female_nums):  # подписи
        if b > 0:
            plt.scatter(a, int(b), s=0)
            plt.text(a, int(b), str(b), fontsize=18)
    plt.title('\nКоличество правильных ответов среди женщин.\n', fontsize=20)
    plt.ylabel('Количество верных ответов\n', fontsize=16)
    plt.xlabel('Тематика сообществ\n', fontsize=18)
    plt.xticks(female_labs, female_labs)
    # скачиваем график
    plt.savefig("static/female_an.png", bbox_inches='tight')
    # данные по осям y и x
    style.use('ggplot')  # задаем стиль
    male_nums = [n[1] for n in sorted(sex_2.items(),
                                      key=lambda x: x[1], reverse=True)]
    male_labs = [n_1[0] for n_1 in sorted(sex_2.items(),
                                          key=lambda x: x[1], reverse=True)]
    plt.figure(figsize=(20, 10), dpi=200)  # размер графика
    plt.bar(male_labs, male_nums, color=colors)  # график
    for a, b in zip(male_labs, male_nums):  # подписи
        if b > 0:
            plt.scatter(a, int(b), s=0)
            plt.text(a, int(b), str(b), fontsize=18)
    plt.title('\nКоличество правильных ответов среди мужчин.\n', fontsize=20)
    plt.ylabel('Количество верных ответов\n', fontsize=16)
    plt.xlabel('Тематика сообществ\n', fontsize=18)
    plt.xticks(male_labs, male_labs)
    # скачиваем график
    plt.savefig("static/male_an.png",  bbox_inches='tight')

    study_nums = [ed[1] for ed in sorted(study.items(),
                                         key=lambda x: x[1], reverse=True)]
    study_labs = [ed_1[0] for ed_1 in sorted(study.items(),
                                             key=lambda x: x[1], reverse=True)]
    plt.figure(figsize=(20, 10), dpi=200)  # размер графика
    plt.bar(study_labs, study_nums, color=colors)  # график
    for a, b in zip(study_labs, study_nums):  # подписи
        if b > 0:
            plt.scatter(a, int(b), s=0)
            plt.text(a, int(b), str(b), fontsize=12)
    # легенда
    plt.title('\nУровень образования опрошенных.\n', fontsize=20)
    plt.ylabel('Количество опрошенных\n', fontsize=16)
    plt.xlabel('Уровни образования\n', fontsize=18)
    plt.xticks(study_labs, study_labs, rotation=8)
    plt.savefig("static/education_an.png", bbox_inches='tight')

    years_nums = [ye[1] for ye in sorted(years.items(),
                                         key=lambda x: x[1], reverse=True)]
    years_labs = [ye_1[0] for ye_1 in sorted(years.items(),
                                             key=lambda x: x[1], reverse=True)]
    plt.figure(figsize=(20, 10), dpi=200)  # размер графика
    plt.bar(years_labs, years_nums, color=colors)  # график
    for a, b in zip(years_labs, years_nums):  # подписи
        if b > 0:
            plt.scatter(a, int(b), s=0)
            plt.text(a, int(b), str(b), fontsize=12)
    # легенда
    plt.title('\nВозраст опрошенных.\n', fontsize=20)
    plt.ylabel('Количество опрошенных\n', fontsize=16)
    plt.xlabel('Возрасты\n', fontsize=18)
    plt.xticks(years_labs, years_labs, rotation=8)
    plt.savefig("static/years_an.png", bbox_inches='tight')

    return render_template('statistics.html', rus_lang=rus_lang,
                           mos_city=mos_city)


if __name__ == '__main__':  # запускаем. ЮХУУУ!
    app.run()
