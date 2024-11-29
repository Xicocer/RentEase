import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import database.db as db
import catalog

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("./windows/login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        email=self.email.text()
        password=self.password.text()
        print(email)
        print(password)
        result = db.auth(email, password)
        if result != "Данные введены неверно":
            widget.close()
            catalog.create_catalog()
            print("Successfully logged in with email: ", email, "and password:", password)
        else:
            self.error.setText(result)
            print(result)

    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("./windows/createacc.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        name = self.name.text()
        email = self.email.text()
        if self.password.text()==self.confirmpass.text():
            password=self.password.text()
            password_confirm = self.confirmpass.text()
            result = db.reg(str(name), str(email), str(password), str(password_confirm))
            if result == "Вы успешно зарегистрировались":
                print("Successfully created acc with email: ", email, "and password: ", password)
                login=Login()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                self.error.setText(result)
                print(result)



app=QApplication(sys.argv)
mainwindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()