from main import get_number_of_columns
from main import get_number_of_rows
from query import make_query
import PyQt5.QtWidgets as qt
from prod_table_module import fill_table


def fill_cat_table(cat_table, link, sorting=""):
    cat_table.clear()  # очистка таблицы
    col_num = get_number_of_columns(link, "category")
    row_num = get_number_of_rows(link, "category")
    cat_table.setColumnCount(col_num)  # количество столбцов
    column_widths = [35, 120, 446]  # значания для ширины столбцов
    for i in range(len(column_widths)):
        cat_table.setColumnWidth(i, column_widths[i])  # установка ширины столбцов
    cat_table.setRowCount(row_num)  # количество строк
    for i in range(row_num):
        cat_table.setRowHeight(i, 110)  # установка высоты строк

    cat_table.setHorizontalHeaderLabels(
        ["ID", "Название", "Описание"])  # заголовки столбцов

    for i in range(row_num):
        for j in range(col_num):
            res = make_query(link, "SELECT * FROM category" + sorting)
            cat_table.setItem(i, j, qt.QTableWidgetItem(str(res[i][j])))


def add_row_cat(cat_table, link, widget):
    add_win = qt.QDialog(widget)
    add_win.setModal(True)
    add_win.resize(400, 100)
    add_win.setWindowTitle("Добавление")

    lbl1 = qt.QLabel("Название:")
    inp1 = qt.QLineEdit()
    lbl2 = qt.QLabel("Описание:")
    inp2 = qt.QTextEdit()
    btn = qt.QPushButton("Добавить")

    grid = qt.QVBoxLayout(add_win)
    grid.addWidget(lbl1, 0)
    grid.addWidget(inp1, 1)
    grid.addWidget(lbl2, 2)
    grid.addWidget(inp2, 3)
    grid.addWidget(btn, 4)

    def add_to_db():
        err_msg_list = []  # список для хранения текстов об ошибках
        # проверка введенных пользователем полей
        if inp1.text() == "":
            err_msg_list.append("Необходимо ввести название!<br>")
        cat_names = make_query(link, "SELECT name FROM category")
        if inp1.text() in [each[0] for each in cat_names]:
            err_msg_list.append("Категория с таким названием уже есть!<br>")
        if inp2.toPlainText() == "":
            err_msg_list.append("Необходимо ввести описание!<br>")
        # Если были ошибки при вводе -> оповещение пользователя об этом
        if len(err_msg_list) != 0:
            err_msg = qt.QErrorMessage()
            err_msg.setWindowTitle("Ошибка!")
            err_msg.setModal(True)
            err_msg.showMessage("".join(err_msg_list))
            err_msg.exec_()
        else:
            make_query(link,
                       "INSERT INTO category (name, description) values('{}', '{}')".format(inp1.text(),
                                                                                            inp2.toPlainText()))
            fill_cat_table(cat_table, link)
            add_win.close()

    btn.clicked.connect(add_to_db)  # привязка функции к кнопке "добавить"

    add_win.exec_()


def edit_cat(cat_table, link, widget, table, dev_table):
    try:
        edit_id = cat_table.selectedItems()[0].text()  # сохранение id категории выбранной строки
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
        inp1.setText(cat_table.selectedItems()[1].text())
        lbl2 = qt.QLabel("Описание:")
        inp2 = qt.QTextEdit()
        inp2.setText(cat_table.selectedItems()[2].text())
        btn = qt.QPushButton("Сохранить")

        grid2 = qt.QVBoxLayout(edit_win)
        grid2.addWidget(lbl1, 0)
        grid2.addWidget(inp1, 1)
        grid2.addWidget(lbl2, 2)
        grid2.addWidget(inp2, 3)
        grid2.addWidget(btn, 4)

        def edit_in_db():
            err_msg_list = []  # список для хранения текстов об ошибках
            # проверка исправленных пользователем полей
            if inp1.text() == "":
                err_msg_list.append("Необходимо ввести название!<br>")
            cat_names = make_query(link, "SELECT name FROM category WHERE NOT id='{}'".format(edit_id))
            if inp1.text() in [each[0] for each in cat_names]:
                err_msg_list.append("Категория с таким названием уже есть!<br>")
            if inp2.toPlainText() == "":
                err_msg_list.append("Необходимо ввести описание!<br>")
            # Если были ошибки при вводе => оповещение пользователя об этом
            if len(err_msg_list) != 0:
                err_msg = qt.QErrorMessage()
                err_msg.setWindowTitle("Ошибка!")
                err_msg.setModal(True)
                err_msg.showMessage("".join(err_msg_list))
                err_msg.exec_()
            else:
                make_query(link,
                           "UPDATE category SET name='{}', description='{}' WHERE id='{}'".format(inp1.text(),
                                                                                                  inp2.toPlainText(),
                                                                                                  edit_id))
                selected_row = cat_table.currentRow()  # сохраниение номера ряда, который был выделен
                fill_cat_table(cat_table, link)
                cat_table.selectRow(selected_row)  # сохраняет выделение разработчика после редактирования
                fill_table(table, link, dev_table,
                           cat_table)  # table - чтобы изменились названия категорий в табице товаров
                edit_win.close()

        btn.clicked.connect(edit_in_db)  # привязка функции к кнопке "сохранить"

        edit_win.exec_()


def delete_cat(cat_table, link, widget, table, dev_table):
    try:
        del_id = cat_table.selectedItems()[0].text()  # сохранение id категории выбранной строки
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
        del_win.setText("Вы действительно хотите удалить выбранную запись?\nСвязанные элементы также будут удалены.\n\n"
                        "Yes - подтвердить\nCancel - отменить")
        del_win.setWindowTitle("Удаление")

        choice = del_win.exec_()  # сохранение выбора пользователя

        if choice == qt.QMessageBox.Yes:  # при подтверждении удаление записи
            make_query(link, "DELETE FROM category WHERE id='{}'".format(del_id))  # удаление разработчика
            make_query(link, "DELETE FROM game WHERE category='{}'".format(del_id))  # удаление товара разработчика
            fill_cat_table(cat_table, link)
            fill_table(table, link, dev_table, cat_table)  # заполнение таблицы заново
