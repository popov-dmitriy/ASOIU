import sys

from connect_db import db_connect
from cat_table_module import *
from dev_table_module import *
from prod_table_module import *
import PyQt5.QtGui as gui
from functions import print_report_dev

# подключение к базе данных
link = db_connect("database.db")


def reset_selection(any_table):
    any_table.clearSelection()
    fill_table(table, link, dev_table, cat_table)


def sort_prod_table(logical_index):
    headers = ["id", "name", "description", "developer", "category", "price"]
    fill_table(table, link, dev_table, cat_table, " ORDER BY " + headers[logical_index])


def sort_dev_table(logical_index):
    headers = ["id", "name", "description"]
    fill_dev_table(dev_table, link, " ORDER BY " + headers[logical_index])


def sort_cat_table(logical_index):
    headers = ["id", "name", "description"]
    fill_cat_table(cat_table, link, " ORDER BY " + headers[logical_index])


if __name__ == "__main__":
    app = qt.QApplication([])
    widget = qt.QWidget()
    # widget.setStyleSheet("QWidget { background-color: #F0F0F0; }")
    # widget.setStyleSheet("background-image: url(1.jpg);")
    widget.setWindowTitle("АСОИУ ЛР №2")
    widget.resize(1920, 900)  # задать размер окна

    table = qt.QTableWidget()  # создание таблицы товаров
    dev_table = qt.QTableWidget()  # создание таблицы разработчиков
    cat_table = qt.QTableWidget()  # создание таблицы категорий

    for obj in [table, dev_table, cat_table]:
        obj.setEditTriggers(qt.QAbstractItemView.NoEditTriggers)  # запрет на редактирование данных
        obj.setSelectionBehavior(qt.QAbstractItemView.SelectRows)  # выделят вместо одной ячейки всю строку

    # привязка к функциям сортировки
    table.horizontalHeader().sectionClicked.connect(sort_prod_table)
    dev_table.horizontalHeader().sectionClicked.connect(sort_dev_table)
    cat_table.horizontalHeader().sectionClicked.connect(sort_cat_table)
    # отлов клика по вертикальному хэдеру (номер строки)
    dev_table.verticalHeader().sectionClicked.connect(lambda _: fill_table(table, link, dev_table, cat_table))
    cat_table.verticalHeader().sectionClicked.connect(lambda _: fill_table(table, link, dev_table, cat_table))
    # отлов клика по ячейке таблицы и выделение всей строки
    dev_table.clicked.connect(lambda _: fill_table(table, link, dev_table, cat_table))
    cat_table.clicked.connect(lambda _: fill_table(table, link, dev_table, cat_table))

    fill_table(table, link, dev_table, cat_table)  # заполнение таблицы товаров
    reset_selected_line_dev = qt.QPushButton("Сброс")  # кнопка сброса выделения в "разработчиках"
    reset_selected_line_dev.clicked.connect(lambda _: reset_selection(dev_table))  # привязка кнопки сброса
    reset_selected_line = qt.QPushButton("Сброс")  # кнопка сброса выделения в "товарах"
    reset_selected_line.clicked.connect(lambda _: reset_selection(table))  # привязка кнопки сброса
    reset_selected_line_cat = qt.QPushButton("Сброс")  # кнопка сброса выделения в "категориях"
    reset_selected_line_cat.clicked.connect(lambda _: reset_selection(cat_table))  # привязка кнопки сброса
    # создание кнопок под таблицей товаров и привязывание функций для отклика
    add_btn = qt.QPushButton("Добавить")
    add_btn.clicked.connect(lambda _: add_row(table, link, widget, dev_table, cat_table))
    edit_btn = qt.QPushButton("Редактировать")
    edit_btn.clicked.connect(lambda _: edit(table, link, widget, dev_table, cat_table))
    del_btn = qt.QPushButton("Удалить")
    del_btn.clicked.connect(lambda _: delete(table, link, widget, dev_table, cat_table))

    fill_dev_table(dev_table, link)  # заполнение таблицы разработчиков
    # создание кнопок под таблицей товаров и привязывание функций для отклика
    add_btn_dev = qt.QPushButton("Добавить")
    add_btn_dev.clicked.connect(lambda _: add_row_dev(dev_table, link, widget))
    edit_btn_dev = qt.QPushButton("Редактировать")
    edit_btn_dev.clicked.connect(lambda _: edit_dev(dev_table, link, widget, table, cat_table))
    del_btn_dev = qt.QPushButton("Удалить")
    del_btn_dev.clicked.connect((lambda _: delete_dev(dev_table, link, widget, table, cat_table)))

    fill_cat_table(cat_table, link)  # заполнение таблицы категорий
    # создание кнопок под таблицей товаров и привязывание функций для отклика
    add_btn_cat = qt.QPushButton("Добавить")
    add_btn_cat.clicked.connect(lambda _: add_row_cat(cat_table, link, widget))
    edit_btn_cat = qt.QPushButton("Редактировать")
    edit_btn_cat.clicked.connect(lambda _: edit_cat(cat_table, link, widget, table, dev_table))
    del_btn_cat = qt.QPushButton("Удалить")
    del_btn_cat.clicked.connect(lambda _: delete_cat(cat_table, link, widget, table, dev_table))

    # заголовки над таблицами
    dev_label = qt.QLabel("    Разработчики")
    prod_label = qt.QLabel("    Товары")
    cat_label = qt.QLabel("    Категории")
    # изменение шрифта заголовкам
    for each in [dev_label, prod_label, cat_label]:
        each.setFont(gui.QFont("Times", 14, gui.QFont.Bold))

    # кнопка печати отчёта
    print_ptn_dev = qt.QPushButton("Отчёт по разработчикам")
    print_ptn_dev.clicked.connect(lambda _: print_report_dev(link))
    print_ptn_cat = qt.QPushButton("Отчёт по категориям")
    print_ptn_cat.clicked.connect(lambda _: print_report_cat(link))

    # расположение элементов по сетке
    grid = qt.QGridLayout(widget)
    grid.setSpacing(15)  # отступы между виджетами

    grid.addWidget(dev_label, 0, 0, 1, 3)
    grid.addWidget(prod_label, 0, 3, 1, 3)
    grid.addWidget(cat_label, 0, 6, 1, 3)

    grid.addWidget(dev_table, 1, 0, 1, 3)
    grid.addWidget(add_btn_dev, 2, 0)
    grid.addWidget(edit_btn_dev, 2, 1)
    grid.addWidget(del_btn_dev, 2, 2)

    grid.addWidget(table, 1, 3, 1, 3)
    grid.addWidget(add_btn, 2, 3)
    grid.addWidget(edit_btn, 2, 4)
    grid.addWidget(del_btn, 2, 5)

    grid.addWidget(cat_table, 1, 6, 1, 3)
    grid.addWidget(add_btn_cat, 2, 6)
    grid.addWidget(edit_btn_cat, 2, 7)
    grid.addWidget(del_btn_cat, 2, 8)

    grid.addWidget(reset_selected_line_dev, 3, 0, 1, 3)
    grid.addWidget(reset_selected_line, 3, 3, 1, 3)
    grid.addWidget(reset_selected_line_cat, 3, 6, 1, 3)

    grid.addWidget(print_ptn_dev, 4, 3)
    grid.addWidget(print_ptn_cat, 4, 5)

    widget.showMaximized()

    sys.exit(app.exec_())
