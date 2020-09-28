"""Модуль для вспомогательных функций"""
from query import make_query
from PyQt5 import Qt
import datetime


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def get_number_of_columns(link, tab):
    res = make_query(link, "pragma table_info({})".format(tab))
    return len(res)


def get_number_of_rows(link, tab, filter_str=""):
    res = make_query(link, "SELECT COUNT(*) FROM {}".format(tab) + filter_str)
    return res[0][0]  # возвращает количество записей в базе


def print_report_dev(link):
    html = "<h6 align=\"right\">{}</h6>".format(datetime.datetime.now())
    html += "<h1 align=\"center\">Отчёт по разработчикам:</h1><br><br>"
    developers = make_query(link, "SELECT name FROM developer")
    developers = [each[0] for each in developers]  # список разработчиков

    for developer in developers:
        html += "<strong>{}</strong>".format(developer)
        dev_id = make_query(link, "SELECT id FROM developer WHERE name='{}'".format(developer))
        games = make_query(link, "SELECT name FROM game WHERE developer='{}'".format(dev_id[0][0]))
        for game in games:
            html += "<pre>      {}</pre>".format(game[0])

    printer = Qt.QPrinter()

    txt = Qt.QTextEdit()
    txt.setHtml(html)

    print_dialog = Qt.QPrintDialog(printer)
    if print_dialog.exec() == Qt.QDialog.Accepted:
        txt.print(printer)


def print_report_cat(link):
    html = "<h6 align=\"right\">{}</h6>".format(datetime.datetime.now())
    html += "<h1 align=\"center\">Отчёт по категориям:</h1><br><br>"
    categories = make_query(link, "SELECT name FROM category")
    categories = [each[0] for each in categories]  # список категорий

    for category in categories:
        html += "<strong>{}</strong>".format(category)
        cat_id = make_query(link, "SELECT id FROM category WHERE name='{}'".format(category))
        games = make_query(link, "SELECT name FROM game WHERE category='{}'".format(cat_id[0][0]))
        for game in games:
            html += "<pre>      {}</pre>".format(game[0])

    printer = Qt.QPrinter()

    txt = Qt.QTextEdit()
    txt.setHtml(html)

    print_dialog = Qt.QPrintDialog(printer)
    if print_dialog.exec() == Qt.QDialog.Accepted:
        txt.print(printer)
