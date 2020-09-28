from functions import *
from query import make_query
import PyQt5.QtWidgets as qt


def fill_table(table, link, dev_table, cat_table, sorting=""):
    table.clear()  # очистка таблицы
    # для фильрации товара при выбранном разработчике или категории
    filter_str = ""
    if len(dev_table.selectedItems()) != 0 and len(cat_table.selectedItems()) != 0:
        filter_str += " WHERE developer='{}' AND category='{}'".format(dev_table.selectedItems()[0].text(),
                                                                       cat_table.selectedItems()[0].text())
    elif len(cat_table.selectedItems()) != 0:
        filter_str += " WHERE category='{}'".format(cat_table.selectedItems()[0].text())
    elif len(dev_table.selectedItems()) != 0:
        filter_str += " WHERE developer='{}'".format(dev_table.selectedItems()[0].text())

    col_num = get_number_of_columns(link, "game")
    row_num = get_number_of_rows(link, "game", filter_str)
    table.setColumnCount(col_num)  # количество столбцов
    column_widths = [35, 73, 275, 90, 80, 47]  # значания для ширины столбцов
    for i in range(len(column_widths)):
        table.setColumnWidth(i, column_widths[i])  # установка ширины столбцов
    table.setRowCount(row_num)  # количество строк
    for i in range(row_num):
        table.setRowHeight(i, 110)  # установка высоты строк

    table.setHorizontalHeaderLabels(
        ["ID", "Название", "Описание", "Разработчик", "Категория", "Цена"])  # заголовки столбцов

    for i in range(row_num):
        for j in range(col_num):
            res = make_query(link, "SELECT * FROM game" + filter_str + sorting)
            if j == 3:  # подмена id разраба на название при выводе в таблицу
                dev_name = make_query(link, "SELECT name FROM developer WHERE id='{}'".format(res[i][j]))
                table.setItem(i, j, qt.QTableWidgetItem(dev_name[0][0]))
            elif j == 4:  # подмена id категории на название при выводе в таблицу
                dev_name = make_query(link, "SELECT name FROM category WHERE id='{}'".format(res[i][j]))
                table.setItem(i, j, qt.QTableWidgetItem(dev_name[0][0]))
            elif j == 5:  # вывод цены с припиской "руб."
                table.setItem(i, j, qt.QTableWidgetItem(str(float(res[i][j])) + " руб."))
            else:
                table.setItem(i, j, qt.QTableWidgetItem(str(res[i][j])))


def add_row(table, link, widget, dev_table, cat_table):
    add_win = qt.QDialog(widget)
    add_win.setModal(True)
    add_win.resize(400, 100)
    add_win.setWindowTitle("Добавление")

    lbl1 = qt.QLabel("Название:")
    inp1 = qt.QLineEdit()
    lbl2 = qt.QLabel("Описание:")
    inp2 = qt.QTextEdit()
    lbl3 = qt.QLabel("Разработчик:")
    inp3 = qt.QComboBox()  # выпадающий список для разработчика
    developers = make_query(link, "SELECT name FROM developer")
    inp3.addItem("")  # пустое значение, чтобы пользователю обязательно надо было выбрать разработчика
    inp3.addItems([each[0] for each in developers])  # достать из "разработчиков" их названия
    lbl4 = qt.QLabel("Категория:")
    inp4 = qt.QComboBox()  # выпадающий список для категории
    categories = make_query(link, "SELECT name FROM category")
    inp4.addItem("")  # пустое значение, чтобы пользователю обязательно надо было выбрать категорию
    inp4.addItems(each[0] for each in categories)  # достать из "категорий" их названия
    lbl5 = qt.QLabel("Цена:")
    inp5 = qt.QLineEdit()
    btn = qt.QPushButton("Добавить")

    grid2 = qt.QVBoxLayout(add_win)
    grid2.addWidget(lbl1, 0)
    grid2.addWidget(inp1, 1)
    grid2.addWidget(lbl2, 2)
    grid2.addWidget(inp2, 3)
    grid2.addWidget(lbl3, 4)
    grid2.addWidget(inp3, 5)
    grid2.addWidget(lbl4, 6)
    grid2.addWidget(inp4, 7)
    grid2.addWidget(lbl5, 8)
    grid2.addWidget(inp5, 9)
    grid2.addWidget(btn, 10)

    def add_to_db():
        err_msg_list = []  # список для хранения текстов об ошибках
        # проверка введенных пользователем полей
        if inp1.text() == "":
            err_msg_list.append("Необходимо ввести название!<br>")
        game_names = make_query(link, "SELECT name FROM game")
        if inp1.text() in [each[0] for each in game_names]:
            err_msg_list.append("Игра с таким названием уже есть!<br>")
        if inp2.toPlainText() == "":
            err_msg_list.append("Необходимо ввести описание!<br>")
        if inp3.currentText() == "":
            err_msg_list.append("Необходимо выбрать разработчика!<br>")
        if inp4.currentText() == "":
            err_msg_list.append("Необходимо выбрать категорию!<br>")
        if inp5.text() == "":
            err_msg_list.append("Необходимо указать цену!<br>")
        elif not is_float(inp5.text()):
            err_msg_list.append("Цена должна быть числовой!<br>")
        # Если были ошибки при вводе -> оповещение пользователя об этом
        if len(err_msg_list) != 0:
            err_msg = qt.QErrorMessage()
            err_msg.setWindowTitle("Ошибка!")
            err_msg.setModal(True)
            err_msg.showMessage("".join(err_msg_list))
            err_msg.exec_()
        else:
            id_dev = make_query(link, "SELECT id FROM developer WHERE name='{}'".format(inp3.currentText()))
            id_cat = make_query(link, "SELECT id FROM category WHERE name='{}'".format(inp4.currentText()))
            make_query(link,
                       "INSERT INTO game (name, description, developer, category, price) values('{}', '{}', '{}', '{}', '{}')".format(
                           inp1.text(), inp2.toPlainText(), id_dev[0][0], id_cat[0][0], inp5.text()))
            fill_table(table, link, dev_table, cat_table)
            add_win.close()

    btn.clicked.connect(add_to_db)  # привязка функции к кнопке "добавить"

    add_win.exec_()


def edit(table, link, widget, dev_table, cat_table):
    try:
        edit_id = table.selectedItems()[0].text()  # сохранение id товара выбранной строки
    except IndexError:
        err_msg = qt.QErrorMessage()
        err_msg.setWindowTitle("Ошибка!")
        err_msg.setModal(True)
        err_msg.showMessage("Необходимо выбрать строку для редактирования!")
        err_msg.exec_()
    else:
        edit_win = qt.QDialog(widget)
        edit_win.setModal(True)
        edit_win.resize(400, 100)
        edit_win.setWindowTitle("Редактирование")

        lbl1 = qt.QLabel("Название:")
        inp1 = qt.QLineEdit()
        inp1.setText(table.selectedItems()[1].text())
        lbl2 = qt.QLabel("Описание:")
        inp2 = qt.QTextEdit()
        inp2.setText(table.selectedItems()[2].text())
        lbl3 = qt.QLabel("Разработчик:")
        inp3 = qt.QComboBox()
        developers = make_query(link, "SELECT name FROM developer")
        developers = [each[0] for each in developers]  # список разработчиков
        inp3.addItems(developers)  # достать из "разработчиков" их названия
        inp3.setCurrentIndex(developers.index(table.selectedItems()[3].text()))
        lbl4 = qt.QLabel("Категория:")
        inp4 = qt.QComboBox()
        categories = make_query(link, "SELECT name FROM category")
        categories = [each[0] for each in categories]  # список категорий
        inp4.addItems(categories)  # достать из "категорий" их названия
        inp4.setCurrentIndex(categories.index(table.selectedItems()[4].text()))
        lbl5 = qt.QLabel("Цена:")
        inp5 = qt.QLineEdit()
        inp5.setText(table.selectedItems()[5].text()[:-5])  # обрезка " руб." в конце цены
        btn = qt.QPushButton("Сохранить")

        grid2 = qt.QVBoxLayout(edit_win)
        grid2.addWidget(lbl1, 0)
        grid2.addWidget(inp1, 1)
        grid2.addWidget(lbl2, 2)
        grid2.addWidget(inp2, 3)
        grid2.addWidget(lbl3, 4)
        grid2.addWidget(inp3, 5)
        grid2.addWidget(lbl4, 6)
        grid2.addWidget(inp4, 7)
        grid2.addWidget(lbl5, 8)
        grid2.addWidget(inp5, 9)
        grid2.addWidget(btn, 10)

        def edit_in_db():
            err_msg_list = []  # список для хранения текстов об ошибках
            # проверка исправленных пользователем полей
            if inp1.text() == "":
                err_msg_list.append("Необходимо ввести название!<br>")
            game_names = make_query(link, "SELECT name FROM game WHERE NOT id='{}'".format(edit_id))
            if inp1.text() in [each[0] for each in game_names]:
                err_msg_list.append("Игра с таким названием уже есть!<br>")
            if inp2.toPlainText() == "":
                err_msg_list.append("Необходимо ввести описание!<br>")
            if inp3.currentText() == "":
                err_msg_list.append("Необходимо выбрать разработчика!<br>")
            if inp4.currentText() == "":
                err_msg_list.append("Необходимо выбрать категорию!<br>")
            if inp5.text() == "":
                err_msg_list.append("Необходимо указать цену!<br>")
            elif not is_float(inp5.text()):
                err_msg_list.append("Цена должна быть числовой!<br>")
            # Если были ошибки при вводе => оповещение пользователя об этом
            if len(err_msg_list) != 0:
                err_msg = qt.QErrorMessage()
                err_msg.setWindowTitle("Ошибка!")
                err_msg.setModal(True)
                err_msg.showMessage("".join(err_msg_list))
                err_msg.exec_()
            else:
                id_dev = make_query(link, "SELECT id FROM developer WHERE name='{}'".format(inp3.currentText()))
                id_cat = make_query(link, "SELECT id FROM category WHERE name='{}'".format(inp4.currentText()))
                make_query(link,
                           "UPDATE game SET name='{}', description='{}', developer='{}', category='{}', price='{}' WHERE id='{}'".format(
                               inp1.text(), inp2.toPlainText(), id_dev[0][0], id_cat[0][0], inp5.text(),
                               edit_id))
                fill_table(table, link, dev_table, cat_table)
                edit_win.close()

        btn.clicked.connect(edit_in_db)  # привязка функции к кнопке "сохранить"

        edit_win.exec_()


def delete(table, link, widget, dev_table, cat_table):
    try:
        del_id = table.selectedItems()[0].text()  # сохранение id товара выбранной строки
    except IndexError:
        err_msg = qt.QErrorMessage()
        err_msg.setWindowTitle("Ошибка!")
        err_msg.setModal(True)
        err_msg.showMessage("Необходимо выбрать строку для удаления!")
        err_msg.exec_()
    else:
        del_win = qt.QMessageBox(widget)  # создается окно подтверждения
        del_win.setModal(True)
        del_win.setStandardButtons(qt.QMessageBox.Yes | qt.QMessageBox.Cancel)  # 2 стандартные кнопки
        del_win.setText("Вы действительно хотите удалить выбранную запись?\n\nYes - подтвердить\nCancel - отменить")
        del_win.setWindowTitle("Удаление")

        choice = del_win.exec_()  # сохранение выбора пользователя

        if choice == qt.QMessageBox.Yes:  # при подтверждении удаление записи
            make_query(link, "DELETE FROM game WHERE id='{}'".format(del_id))
            fill_table(table, link, dev_table, cat_table)  # заполнение таблицы заново
