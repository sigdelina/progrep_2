from flask import Flask
from flask import url_for, render_template, request
import os
import sqlite3
import re
from pymystem3 import Mystem


def new_Datebase():
    con = sqlite3.connect("4search.db.sqlite")
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS alldata(link text, title text, ordinary text, lemma text, morph text)")
    start_path = './newspaper/plain/'
    start_path2 = './newspaper/mystem_lem/'
    start_path3 = './newspaper/mystem_plain/'
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
                for root2, dirs2, files2 in os.walk(start_path2):
                    for file2 in files2:
                        if ".txt" in file2:
                            file_2 = file2
                            final2 = os.path.join(root2, file_2)
                            if file_2 == file_1:
                                with open(final2, 'r', encoding='utf-8') as fi:
                                    lemma_extra = fi.read()
                                    extr = re.compile(r"[,.?!\":;«»^{}></|%$]", re.DOTALL)
                                    lemma_clean = extr.sub(' ', lemma_extra)
                                    lemma = re.sub('  ', ' ', lemma_clean)
                for root3, dirs3, files3 in os.walk(start_path3):
                    for file3 in files3:
                        if ".txt" in file3:
                            file_3 = file3
                            final3 = os.path.join(root3, file_3)
                            if file_3 == file_1:
                                with open(final3, 'r', encoding='utf-8') as fin:
                                    morfo = fin.read()
                                    cur.execute("INSERT INTO alldata VALUES (?, ?, ?, ?, ?)", (
                                                f_link, f_title, result.replace('\t', '').replace('\n', ''),
                                                lemma.replace('\t', '').replace('\n', ''), morfo))
    con.commit()
    con.close()
    return

new_Datebase()

app = Flask(__name__)


@app.route('/')  # главная страница
def general():
    if request.args:
        search = request.args['search']
        search = str(search)
        m = Mystem()
        lemmas = m.lemmatize(search)
        search = ''.join(lemmas)
        connection = sqlite3.connect('4search.db.sqlite')
        cursor = connection.cursor()
        print(search)
        res = "% " + str(search).replace('\n', '') + " %"
        result_cort = []
        for row in cursor.execute("SELECT link, title, ordinary FROM alldata WHERE lemma LIKE ?",(res,)):
            print(row)
            result_cort.append(row)
        return render_template('results.html', search=search, result_cort=result_cort)
    return render_template('general.html')

if __name__ == '__main__':
    app.run(debug=True)
