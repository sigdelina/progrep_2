from flask import Flask
from flask import url_for, render_template, request
import json

app = Flask(__name__)


# создаем файл цсв для дальнейшей записи
def create():
    row = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'
    with open('results.csv', 'w', encoding='utf-8') as file:
        file.write(row % ("имя", "возраст", "родной язык", 'родной город',
                          "пол", "уровень образования", "вопрос 1",
                          "ворпос 2", "ворпос 3"))
    return


create()


@app.route('/')  # главная страница с опросом
def general():
    urls = {'Главная страница с опросом': url_for('general'),
            'Все ответы в формате json': url_for('jsonel'),
            'Статистика': url_for('stat'),
            'Поиск': url_for('searching')}
    if request.args:
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
        #  записываем данные в цсв-файл
        with open('results.csv', 'a+', encoding='utf-8') as file:
            file.write(row % (name, age, lang, city, gender, study,
                       quest_1, quest_2, quest_3))
        return render_template('answer.html', name=name, age=age,
                               lang=lang, city=city, gender=gender,
                               study=study, quest_1=quest_1, quest_2=quest_2,
                               quest_3=quest_3, urls=urls)
    return render_template('question.html')


@app.route('/json')  # создаем json-строку
def jsonel():
    fin = []
    with open("results.csv", 'r', encoding='utf-8') as f_obj:
        for line in f_obj:
            line = line.split('\t')
            d = {"name": line[0], 'age': line[1], "lang": line[2],
                 "city": line[3], "gender": line[4],
                 'study': line[5], 'quest_1': line[6],
                 'quest_2': line[7], "quest_3": line[8].replace('\n', '')}
            fin.append(d)
    json_string = json.dumps(fin[1:], ensure_ascii=False, indent=4)
    json_date = json.loads(json_string)
    # записываем json-строки в спец файл
    with open('json_info.json', 'w', encoding='utf-8') as f:
        json.dump(json_date, f, ensure_ascii=False, indent=4)
    # на страницу передеается json type(list)
    return render_template('json.html', json_date=json_date)


@app.route('/search')  # поиск
def searching():
    search_list = []
    serc_st = ''
    urls = {'Главная страница с опросом': url_for('general'),
            'Все ответы в формате json': url_for('jsonel'),
            'Статистика': url_for('stat'),
            'Результаты вышего поиска': url_for('resultin')}
    if request.args:
        studying = request.args['studying']
        word = request.args['word']
        # делаем словарь из цсв файла
        with open("results.csv", 'r', encoding='utf-8') as f_obj:
            for line in f_obj:
                line = line.split('\t')
                d = {"name": line[0], 'age': line[1], "lang": line[2],
                     "city": line[3], "gender": line[4],
                     'study': line[5], 'quest_1': line[6],
                     'quest_2': line[7], "quest_3": line[8].replace('\n', '')}
                search_list.append(d)
        # выводм информацию
        with open("search.txt", 'w', encoding='utf-8') as f:
            for el in search_list:
                if word in str(el) and studying in str(el):
                    serc_st += str(el).replace('{', '').replace('}', '') + "\n"
            f.write(serc_st)
        return render_template('resulting.html', studying=studying,
                               word=word, urls=urls)
    return render_template('items search.html', urls=urls)


@app.route('/results')  # создаем страницу с результатами поиска
def resultin():
    files = []
    urls = {'Главная страница с опросом': url_for('general'),
            'Все ответы в формате json': url_for('jsonel'),
            'Статистика': url_for('stat'),
            'Поиск': url_for('searching')}
    with open("search.txt", 'r', encoding='utf-8') as f_obj:
        for line in f_obj:
            files.append(line)
    return render_template('final.html', files=files, urls=urls)


@app.route('/stats')  # страница со статистикой
def stat():
    urls = {'Главная страница с опросом': url_for('general'),
            'Все ответы в формате json': url_for('jsonel'),
            'Поиск': url_for('searching')}
    # cписки для языка
    rus_ked = []
    nrus_ked = []
    rus_keda = []
    nrus_keda = []
    rus_krvk = []
    nrus_krvk = []
    rus_krvka = []
    nrus_krvka = []
    rus_tpk = []
    nrus_tpk = []
    rus_tpka = []
    nrus_tpka = []
    # списки для города
    ms_ked = []
    nms_ked = []
    ms_keda = []
    nms_keda = []
    ms_krvk = []
    nms_krvk = []
    ms_krvka = []
    nms_krvka = []
    ms_tpk = []
    nms_tpk = []
    ms_tpka = []
    nms_tpka = []
    # cписки для пола
    fe_ked = []
    ma_ked = []
    fe_keda = []
    ma_keda = []
    fe_krvk = []
    ma_krvk = []
    fe_krvka = []
    ma_krvka = []
    fe_tpk = []
    ma_tpk = []
    fe_tpka = []
    ma_tpka = []
    # cписки для возраста
    und18_ked = []
    f18t30_ked = []
    und18_keda = []
    f18t30_keda = []
    und18_krvk = []
    f18t30_krvk = []
    und18_krvka = []
    f18t30_krvka = []
    und18_tpk = []
    f18t30_tpk = []
    und18_tpka = []
    f18t30_tpka = []
    f31t50_ked = []
    mo50_ked = []
    f31t50_keda = []
    mo50_keda = []
    f31t50_krvk = []
    mo50_krvk = []
    f31t50_krvka = []
    mo50_krvka = []
    f31t50_tpk = []
    mo50_tpk = []
    f31t50_tpka = []
    mo50_tpka = []
    # списки для образования
    hig_ked = []
    lo_ked = []
    hig_keda = []
    lo_keda = []
    hig_krvk = []
    lo_krvk = []
    hig_krvka = []
    lo_krvka = []
    hig_tpk = []
    lo_tpk = []
    hig_tpka = []
    lo_tpka = []
    with open('results.csv', 'r', encoding="utf-8") as f_obj:
        for row in f_obj:
            row = row.split('\t')
            if row[2] == 'русский' and row[6] == 'кед: м.р.':
                rus_ked.append(row[6])
            if row[2] == 'русский' and row[6] == 'кеда: ж.р.':
                rus_keda.append(row[6])
            if row[2] == 'не русский' and row[6] == 'кед: м.р.':
                nrus_ked.append(row[6])
            if row[2] == 'не русский' and row[6] == 'кеда: ж.р.':
                nrus_keda.append(row[6])
            if row[2] == 'русский' and row[7] == 'кроссовок: м.р.':
                rus_krvk.append(row[7])
            if row[2] == 'русский' and row[7] == 'кроссовка: ж.р.':
                rus_krvka.append(row[7])
            if row[2] == 'не русский' and row[7] == 'кроссовок: м.р.':
                nrus_krvk.append(row[7])
            if row[2] == 'не русский' and row[7] == 'кроссовка: ж.р.':
                nrus_krvka.append(row[7])
            if row[2] == 'русский' and row[8] == 'тапок: м.р.\n':
                rus_tpk.append(row[8])
            if row[2] == 'русский' and row[8] == 'тапка: ж.р.\n':
                rus_tpka.append(row[8])
            if row[2] == 'не русский' and row[8] == 'тапок: м.р.\n':
                nrus_tpk.append(row[8])
            if row[2] == 'не русский' and row[8] == 'тапка: ж.р.\n':
                nrus_tpka.append(row[8])
            if row[3] == 'Москва и МО' and row[6] == 'кед: м.р.':
                ms_ked.append(row[6])
            if row[3] == 'Москва и МО' and row[6] == 'кеда: ж.р.':
                ms_keda.append(row[6])
            if row[3] == 'Не Москва и МО' and row[6] == 'кед: м.р.':
                nms_ked.append(row[6])
            if row[3] == 'Не Москва и МО' and row[6] == 'кеда: ж.р.':
                nms_keda.append(row[6])
            if row[3] == 'Москва и МО' and row[7] == 'кроссовок: м.р.':
                ms_krvk.append(row[7])
            if row[3] == 'Москва и МО' and row[7] == 'кроссовка: ж.р.':
                ms_krvka.append(row[7])
            if row[3] == 'Не Москва и МО' and row[7] == 'кроссовок: м.р.':
                nms_krvk.append(row[7])
            if row[3] == 'Не Москва и МО' and row[7] == 'кроссовка: ж.р.':
                ms_krvka.append(row[7])
            if row[3] == 'Москва и МО' and row[8] == 'тапок: м.р.\n':
                ms_tpk.append(row[8])
            if row[3] == 'Москва и МО' and row[8] == 'тапка: ж.р.\n':
                ms_tpka.append(row[8])
            if row[3] == 'Не Москва и МО' and row[8] == 'тапок: м.р.\n':
                nms_tpk.append(row[8])
            if row[3] == 'Не Москва и МО' and row[8] == 'тапка: ж.р.\n':
                nms_tpka.append(row[8])
            if row[4] == 'женский' and row[6] == 'кед: м.р.':
                fe_ked.append(row[6])
            if row[4] == 'женский' and row[6] == 'кеда: ж.р.':
                fe_keda.append(row[6])
            if row[4] == 'мужской' and row[6] == 'кед: м.р.':
                ma_ked.append(row[6])
            if row[4] == 'мужской' and row[6] == 'кеда: ж.р.':
                ma_keda.append(row[6])
            if row[4] == 'женский' and row[7] == 'кроссовок: м.р.':
                fe_krvk.append(row[7])
            if row[4] == 'женский' and row[7] == 'кроссовка: ж.р.':
                fe_krvka.append(row[7])
            if row[4] == 'мужской' and row[7] == 'кроссовок: м.р.':
                ma_krvk.append(row[7])
            if row[4] == 'мужской' and row[7] == 'кроссовка: ж.р.':
                ma_krvka.append(row[7])
            if row[4] == 'женский' and row[8] == 'тапок: м.р.\n':
                fe_tpk.append(row[8])
            if row[4] == 'женский' and row[8] == 'тапка: ж.р.\n':
                fe_tpka.append(row[8])
            if row[4] == 'мужской' and row[8] == 'тапок: м.р.\n':
                ma_tpk.append(row[8])
            if row[4] == 'мужской' and row[8] == 'тапка: ж.р.\n':
                ma_tpka.append(row[8])
            if row[1] == 'меньше 18' and row[6] == 'кед: м.р.':
                und18_ked.append(row[6])
            if row[1] == 'меньше 18' and row[6] == 'кеда: ж.р.':
                und18_keda.append(row[6])
            if row[1] == 'от 19 до 30' and row[6] == 'кед: м.р.':
                f18t30_ked.append(row[6])
            if row[1] == 'от 19 до 30' and row[6] == 'кеда: ж.р.':
                f18t30_keda.append(row[6])
            if row[1] == 'меньше 18' and row[7] == 'кроссовок: м.р.':
                und18_krvk.append(row[7])
            if row[1] == 'меньше 18' and row[7] == 'кроссовка: ж.р.':
                und18_krvka.append(row[7])
            if row[1] == 'от 19 до 30' and row[7] == 'кроссовок: м.р.':
                f18t30_krvk.append(row[7])
            if row[1] == 'от 19 до 30' and row[7] == 'кроссовка: ж.р.':
                f18t30_krvka.append(row[7])
            if row[1] == 'меньше 18' and row[8] == 'тапок: м.р.\n':
                und18_tpk.append(row[8])
            if row[1] == 'меньше 18' and row[8] == 'тапка: ж.р.\n':
                und18_tpka.append(row[8])
            if row[1] == 'от 19 до 30' and row[8] == 'тапок: м.р.\n':
                f18t30_tpk.append(row[8])
            if row[1] == 'от 19 до 30' and row[8] == 'тапка: ж.р.\n':
                f18t30_tpka.append(row[8])
            if row[1] == 'от 31 до 50' and row[6] == 'кед: м.р.':
                f31t50_ked.append(row[6])
            if row[1] == 'от 31 до 50' and row[6] == 'кеда: ж.р.':
                f31t50_keda.append(row[6])
            if row[1] == 'больше 51' and row[6] == 'кед: м.р.':
                mo50_ked.append(row[6])
            if row[1] == 'больше 51' and row[6] == 'кеда: ж.р.':
                mo50_keda.append(row[6])
            if row[1] == 'от 31 до 50' and row[7] == 'кроссовок: м.р.':
                f31t50_krvk.append(row[7])
            if row[1] == 'от 31 до 50' and row[7] == 'кроссовка: ж.р.':
                f31t50_krvka.append(row[7])
            if row[1] == 'больше 51' and row[7] == 'кроссовок: м.р.':
                mo50_krvk.append(row[7])
            if row[1] == 'больше 51' and row[7] == 'кроссовка: ж.р.':
                mo50_krvka.append(row[7])
            if row[1] == 'от 31 до 50' and row[8] == 'тапок: м.р.\n':
                f31t50_tpk.append(row[8])
            if row[1] == 'от 31 до 50' and row[8] == 'тапка: ж.р.\n':
                f31t50_tpka.append(row[8])
            if row[1] == 'больше 51' and row[8] == 'тапок: м.р.\n':
                mo50_tpk.append(row[8])
            if row[1] == 'больше 51' and row[8] == 'тапка: ж.р.\n':
                mo50_tpka.append(row[8])
            if row[5] == 'с высшим' and row[6] == 'кед: м.р.':
                hig_ked.append(row[6])
            if row[5] == 'с высшим' and row[6] == 'кеда: ж.р.':
                hig_keda.append(row[6])
            if row[5] == 'без высшего' and row[6] == 'кед: м.р.':
                lo_ked.append(row[6])
            if row[5] == 'без высшего' and row[6] == 'кеда: ж.р.':
                lo_keda.append(row[6])
            if row[5] == 'с высшим' and row[7] == 'кроссовок: м.р.':
                hig_krvk.append(row[7])
            if row[5] == 'с высшим' and row[7] == 'кроссовка: ж.р.':
                hig_krvka.append(row[7])
            if row[5] == 'без высшего' and row[7] == 'кроссовок: м.р.':
                lo_krvk.append(row[7])
            if row[5] == 'без высшего' and row[7] == 'кроссовка: ж.р.':
                lo_krvka.append(row[7])
            if row[5] == 'с высшим' and row[8] == 'тапок: м.р.\n':
                hig_tpk.append(row[8])
            if row[5] == 'с высшим' and row[8] == 'тапка: ж.р.\n':
                hig_tpka.append(row[8])
            if row[5] == 'без высшего' and row[8] == 'тапок: м.р.\n':
                lo_tpk.append(row[8])
            if row[5] == 'без высшего' and row[8] == 'тапка: ж.р.\n':
                lo_tpka.append(row[8])
    # длина для языка
    rus_km = len(rus_ked)
    rus_kf = len(rus_keda)
    nrus_km = len(nrus_ked)
    nrus_kf = len(nrus_keda)
    rus_krm = len(rus_krvk)
    rus_krf = len(rus_krvka)
    nrus_krm = len(nrus_krvk)
    nrus_krf = len(nrus_krvka)
    rus_tm = len(rus_tpk)
    rus_tf = len(rus_tpka)
    nrus_tm = len(nrus_tpk)
    nrus_tf = len(nrus_tpka)
    # длина для города
    m_km = len(ms_ked)
    m_kf = len(ms_keda)
    nm_km = len(nms_ked)
    nm_kf = len(nms_keda)
    m_krm = len(ms_krvk)
    m_krf = len(ms_krvka)
    nm_krm = len(nms_krvk)
    nm_krf = len(nms_krvka)
    m_tm = len(ms_tpk)
    m_tf = len(ms_tpka)
    nm_tm = len(nms_tpk)
    nm_tf = len(nms_tpka)
    # длина для пола
    male_km = len(ma_ked)
    male_kf = len(ma_keda)
    fe_km = len(fe_ked)
    fe_kf = len(fe_keda)
    male_krm = len(ma_krvk)
    male_krf = len(ma_krvka)
    fe_krm = len(fe_krvk)
    fe_krf = len(fe_krvka)
    male_tm = len(ma_tpk)
    male_tf = len(ma_tpka)
    fe_tm = len(fe_tpk)
    fe_tf = len(fe_tpka)
    # длина для возраста
    l18_km = len(und18_ked)
    le18_kf = len(und18_keda)
    from18_km = len(f18t30_ked)
    from18_kf = len(f18t30_keda)
    le18_krm = len(und18_krvk)
    le18_krf = len(und18_krvka)
    from18_krm = len(f18t30_krvk)
    from18_krf = len(f18t30_krvka)
    le18_tm = len(und18_tpk)
    le18_tf = len(und18_tpka)
    from18_tm = len(f18t30_tpk)
    from18_tf = len(f18t30_tpka)
    from30_km = len(f31t50_ked)
    from30_kf = len(f31t50_keda)
    fr50_km = len(mo50_ked)
    fr50_kf = len(mo50_keda)
    from30_krm = len(f31t50_krvk)
    from30_krf = len(f31t50_krvka)
    fr50_krm = len(mo50_krvk)
    fr50_krf = len(mo50_krvka)
    from30_tm = len(f31t50_tpk)
    from30_tf = len(f31t50_tpka)
    fr50_tm = len(mo50_tpk)
    fr50_tf = len(mo50_tpka)
    # длина для образования
    high_km = len(hig_ked)
    high_kf = len(hig_keda)
    low_km = len(lo_ked)
    low_kf = len(lo_keda)
    high_krm = len(hig_krvk)
    high_krf = len(hig_krvka)
    low_krm = len(lo_krvk)
    low_krf = len(lo_krvka)
    high_tm = len(hig_tpk)
    high_tf = len(hig_tpka)
    low_tm = len(lo_tpk)
    low_tf = len(lo_tpka)
    return render_template('statistic.html', rus_km=rus_km, rus_kf=rus_kf,
                           nrus_km=nrus_km, nrus_kf=nrus_kf, rus_krm=rus_krm,
                           rus_krf=rus_krf, nrus_krm=nrus_krm,
                           nrus_krf=nrus_krf, rus_tm=rus_tm, rus_tf=rus_tf,
                           nrus_tm=nrus_tm, nrus_tf=nrus_tf, m_km=m_km,
                           m_kf=m_kf, nm_km=nm_km, nm_kf=nm_kf, m_krm=m_krm,
                           m_krf=m_krf, nm_krm=nm_krm, nm_krf=nm_krf,
                           m_tm=m_tm, m_tf=m_tf, nm_tm=nm_tm, nm_tf=nm_tf,
                           male_km=male_km, male_kf=male_kf, fe_km=fe_km,
                           fe_kf=fe_kf, male_krm=male_krm, male_krf=male_krf,
                           fe_krm=fe_krm, fe_krf=fe_krf, male_tm=male_tm,
                           male_tf=male_tf, fe_tm=fe_tm, fe_tf=fe_tf,
                           l18_km=l18_km, le18_kf=le18_kf, from18_km=from18_km,
                           from18_kf=from18_kf, le18_krm=le18_krm,
                           le18_krf=le18_krf, from18_krm=from18_krm,
                           from18_krf=from18_krf, le18_tm=le18_tm,
                           le18_tf=le18_tf, from18_tm=from18_tm,
                           from18_tf=from18_tf, from30_km=from30_km,
                           from30_kf=from30_kf, fr50_km=fr50_km,
                           fr50_kf=fr50_kf, from30_krm=from30_krm,
                           from30_krf=from30_krf, fr50_krm=fr50_krm,
                           fr50_krf=fr50_krf, from30_tm=from30_tm,
                           from30_tf=from30_tf, fr50_tm=fr50_tm,
                           fr50_tf=fr50_tf, high_km=high_km, high_kf=high_kf,
                           low_km=low_km, low_kf=low_kf, high_krm=high_krm,
                           high_krf=high_krf, low_krm=low_krm, low_krf=low_krf,
                           high_tm=high_tm, high_tf=high_tf, low_tm=low_tm,
                           low_tf=low_tf, urls=urls)


if __name__ == '__main__':
    app.run(debug=True)

#
