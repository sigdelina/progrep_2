from flask import Flask
from flask import render_template, request
import os
import sqlite3
import re
from itertools import groupby


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
