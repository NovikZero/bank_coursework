import datetime
import sys

from PyQt5 import uic, QtWidgets
from data import db_session
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTableWidgetItem
from data.bank import Bank


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        uic.loadUi('main.ui', self)
        self.AddButton.clicked.connect(self.add)
        self.SearchButton.clicked.connect(self.search)

        header = self.BankTable.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    @staticmethod
    def data_validation(name, from_bill, to_bill, cost):
        if not (name and from_bill and to_bill and cost):
            return 'Поля не должны бить пустыми'

        if (not from_bill.isdigit()) or (not to_bill.isdigit()):
            return 'Счета должны быть натуральными числами'

        if not cost.isdigit():
            return 'Сумма должна быть натуральным числом'

        return False

    def add(self):
        name = self.NameEdit.text()
        from_bill = self.FromBillEdit.text()
        to_bill = self.ToBillEdit.text()
        cost = self.CostEdit.text()

        if self.data_validation(name, from_bill, to_bill, cost):
            self.InfoLabel.setText(self.data_validation(name, from_bill, to_bill, cost))
            return

        db_sess = db_session.create_session()
        db_sess.add(Bank(name=name, from_bill=int(from_bill), to_bill=int(to_bill), cost=int(cost)))
        db_sess.commit()
        self.InfoLabel.setText('Платёж успешно добавлен')

    def search(self):
        combo_box_text = self.SearchComboBox.currentText()

        if combo_box_text == 'Все':
            self.all()
            return

        text = self.SearchEdit.text()

        if not text:
            self.InfoLabel.setText('Введите счёт для поиска')
            return

        if not text.isdigit():
            self.InfoLabel.setText('Счёт должен быть натуральным числом')
            return

        if combo_box_text == 'По счёту отправителя':
            self.from_bill(text)

        if combo_box_text == 'По счёту получателя':
            self.to_bill(text)

    def from_bill(self, text):
        db_sess = db_session.create_session()
        bank_list = db_sess.query(Bank).filter(Bank.from_bill == int(text))

        self.BankTable.setRowCount(0)
        for i, bank in enumerate(bank_list):
            self.BankTable.setRowCount(self.BankTable.rowCount() + 1)
            self.BankTable.setItem(i, 0, QTableWidgetItem(bank.name))
            self.BankTable.setItem(i, 1, QTableWidgetItem(str(bank.from_bill)))
            self.BankTable.setItem(i, 2, QTableWidgetItem(str(bank.to_bill)))
            self.BankTable.setItem(i, 3, QTableWidgetItem(str(bank.cost)))

    def to_bill(self, text):
        db_sess = db_session.create_session()
        bank_list = db_sess.query(Bank).filter(Bank.to_bill == int(text))

        self.BankTable.setRowCount(0)
        for i, bank in enumerate(bank_list):
            self.BankTable.setRowCount(self.BankTable.rowCount() + 1)
            self.BankTable.setItem(i, 0, QTableWidgetItem(bank.name))
            self.BankTable.setItem(i, 1, QTableWidgetItem(str(bank.from_bill)))
            self.BankTable.setItem(i, 2, QTableWidgetItem(str(bank.to_bill)))
            self.BankTable.setItem(i, 3, QTableWidgetItem(str(bank.cost)))

    def all(self):
        db_sess = db_session.create_session()
        bank_list = db_sess.query(Bank).all()

        self.BankTable.setRowCount(0)
        for i, bank in enumerate(bank_list):
            print(bank.from_bill, bank.to_bill)
            self.BankTable.setRowCount(self.BankTable.rowCount() + 1)
            self.BankTable.setItem(i, 0, QTableWidgetItem(bank.name))
            self.BankTable.setItem(i, 1, QTableWidgetItem(str(bank.from_bill)))
            self.BankTable.setItem(i, 2, QTableWidgetItem(str(bank.to_bill)))
            self.BankTable.setItem(i, 3, QTableWidgetItem(str(bank.cost)))


if __name__ == '__main__':
    db_session.global_init('data/banks.sqlite')
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())