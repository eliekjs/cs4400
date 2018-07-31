#!/usr/bin/env python3

import pymysql
import sys
from PyQt5.QtWidgets import (
    QTextEdit,
    QInputDialog,
    QApplication,
    QWidget,
    QPushButton,
    QDialog,
    QGroupBox,
    QVBoxLayout,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QLabel,
    qApp,
    QAction,
    QSplitter,
    QAbstractItemView,
    QListWidget,
    QListView,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)
from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem
)
import pymysql

global user_dict
user_dict={}
global user_list
user_list=[]

global attr_dict
attr_dict={}
global attr_list
attr_list=[]

global givenemail
givenemail =''


class viewprofile(QDialog):
    def __init__(self,parent=None):
        super(viewprofile,self).__init__()

        self.email=QLineEdit(user_dict['email'])
        self.password=QLineEdit(user_dict['password'])
        self.fname=QLineEdit(user_dict['First Name'])
        self.lname=QLineEdit(user_dict['Last Name'])
        self.street=QLineEdit(user_dict['Street'])
        self.city=QLineEdit(user_dict['City'])
        self.state=QLineEdit(user_dict['State'])
        self.pcode=QLineEdit(user_dict['Postal Code'])
        self.country=QLineEdit(user_dict['Country'])
        self.ccnum=QLineEdit(user_dict['CC Number'])
        self.expiry=QLineEdit(user_dict['Expiry'])
        self.birthdate=QLineEdit(user_dict['Birthdate'])
        self.cvv = QLineEdit(user_dict["CVV"])

        form_group_box8=QGroupBox('Profile Information')
        layout=QFormLayout()
        layout.addRow(QLabel('Email'),self.email)
        layout.addRow(QLabel('Password'),self.password)
        layout.addRow(QLabel('First Name'),self.fname)
        layout.addRow(QLabel('Last Name'),self.lname)
        layout.addRow(QLabel('Street'),self.street)
        layout.addRow(QLabel('City'),self.city)
        layout.addRow(QLabel('State'),self.state)
        layout.addRow(QLabel('Postal Code'),self.pcode)
        layout.addRow(QLabel('Country'),self.country)
        layout.addRow(QLabel('Credit Card Number'),self.ccnum)
        layout.addRow(QLabel('Expiry'),self.expiry)
        layout.addRow(QLabel('Birthdate'),self.birthdate)
        layout.addRow(QLabel("CVV"),self.cvv)
        form_group_box8.setLayout(layout)

        vbox_layout=QVBoxLayout()
        vbox_layout.addWidget(form_group_box8)
        self.setLayout(vbox_layout)


class TableDialog(QDialog):
    def __init__(self, column_headers, rows):
        super(TableDialog, self).__init__()
        self.setModal(True)
        self.setWindowTitle("")

        table = QTableWidget(len(rows), len(rows[0]), self)
        table.setHorizontalHeaderLabels(column_headers)
        for i, row in enumerate(rows):
            for j, field in enumerate(row):
                item = QTableWidgetItem(field)
                table.setItem(i, j, item)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(table)
        vbox_layout.addWidget(buttons)
        self.setLayout(vbox_layout)


class MainWindow(QWidget):

    def __init__(self, db):
        super(MainWindow, self).__init__()
        self.setWindowTitle("MySQL Browser")
        cursor = connection.cursor()
        cursor.execute("show tables")
        vbox_layout = QVBoxLayout()
        for row in cursor:
            table = row[f"Tables_in_{db}"]
            vbox_layout.addWidget(self.make_button(db, table))
        adminpagebtn=QPushButton('Write a Review',self)
        adminpagebtn.clicked.connect(self.on_pushButton_clicked)
        #profilebtn=QPushButton('View Profile',self)
        #profilebtn.clicked.connect(self.on_pushButton_clicked2)

        #adminpagebtn.setStyleSheet("background-color: lightskyblue");
        vbox_layout.addWidget(adminpagebtn)
        #vbox_layout.addWidget(profilebtn)
        #registerbtn.clicked.connect(self.close)
        self.dialog=reviewpage(self)
        #self.dialog2=viewprofile(self)
        self.setLayout(vbox_layout)

    def make_button(self, db, table):

        button = QPushButton(table, self)
        button.clicked.connect(lambda: self.display(db, table))
        return button

    def display(self, db, table):
        curs = connection.cursor()
        query = f"select * from {table}"
        curs.execute(query)
        rows = []
        first_row = curs.fetchone()
        column_headers = [str(k).strip() for k, v in first_row.items()]
        rows.append([str(v).strip() for k, v in first_row.items()])
        for row in curs:
            rows.append([str(v).strip() for k, v in row.items()])

        dlg = TableDialog(column_headers, rows)
        dlg.exec()


    def on_pushButton_clicked(self):
        self.dialog.show()

    def on_pushButton_clicked2(self):
        #self.dialog.show()
        text, okPressed = QInputDialog.getText(self, "Email","Enter Email:", QLineEdit.Normal, "")
        self.dialog2.show()

class DbRegistrationDialog(QDialog):
    def __init__(self,db):
        super(DbRegistrationDialog,self).__init__
        self.setModal(True)
        self.setWindowTitle('Registration Credentials')
        sel

class DbLoginDialog(QDialog):
    def __init__(self,db):
        super(DbLoginDialog, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Login to MySQL Server")

        self.host = QLineEdit("localhost")
        self.user = QLineEdit("root")
        self.password = QLineEdit()
        self.db = QLineEdit()

        form_group_box = QGroupBox("MySQL Server Login Credentials")
        layout = QFormLayout()
        layout.addRow(QLabel("Host:"), self.host)
        layout.addRow(QLabel("User:"), self.user)
        layout.addRow(QLabel("Password:"), self.password)
        layout.addRow(QLabel("Database:"), self.db)
        form_group_box.setLayout(layout)

        # Consider these 3 lines boiler plate for a standard Ok | Cancel dialog
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        registerbtn=QPushButton('Register',self)
        registerbtn.clicked.connect(self.on_pushButton_clicked)
        #registerbtn.clicked.connect(self.close)
        self.dialog=registration(self,db)


        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(form_group_box)
        vbox_layout.addWidget(buttons)
        vbox_layout.addWidget(registerbtn)
        self.setLayout(vbox_layout)
        self.password.setFocus()

    def on_pushButton_clicked(self):
        self.dialog.show()

    def registration(self):
        #self.setModal(True)
        self.setWindowTitle("Registration")

        self.email=QLineEdit()
        self.password = QLineEdit()

        form_group_box2 = QGroupBox("Registration Information")
        layout2 = QFormLayout()
        layout2.addRow(QLabel("Email:"), self.email)
        layout2.addRow(QLabel("Password:"), self.password)
        form_group_box2.setLayout(layout2)

        # Consider these 3 lines boiler plate for a standard Ok | Cancel dialog
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.show()

        vbox_layout2 = QVBoxLayout()
        vbox_layout2.addWidget(form_group_box2)
        self.setLayout(vbox_layout2)
        self.password.setFocus()

class registration(QDialog):
    def __init__(self,db, parent=None):
        super(registration, self).__init__(parent)
        self.setModal(True)
        self.email=QLineEdit()
        self.cemail=QLineEdit()
        self.password=QLineEdit()
        self.cpassword=QLineEdit()
        self.fname=QLineEdit()
        self.lname=QLineEdit()
        self.street=QLineEdit()
        self.city=QLineEdit()
        self.state=QLineEdit()
        self.pcode=QLineEdit()
        self.country=QLineEdit()
        self.ccnum=QLineEdit()
        self.expiry=QLineEdit()
        self.birthdate=QLineEdit()
        self.cvv = QLineEdit()
        self.setWindowTitle("Registration Information")

        form_group_box3= QGroupBox("Account Credentials")
        layout3=QFormLayout()
        layout3.addRow(QLabel('Email'),self.email)
        layout3.addRow(QLabel('Confirm Email'),self.cemail)
        #layout3.addRow(Qlabel('Confirm Email'),self.cemail)
        layout3.addRow(QLabel('Password'),self.password)
        layout3.addRow(QLabel('Confirm Password'),self.cpassword)
        layout3.addRow(QLabel('First Name'),self.fname)
        layout3.addRow(QLabel('Last Name'),self.lname)
        layout3.addRow(QLabel('Street'),self.street)
        layout3.addRow(QLabel('City'),self.city)
        layout3.addRow(QLabel('State'),self.state)
        layout3.addRow(QLabel('Postal Code'),self.pcode)
        layout3.addRow(QLabel('Country'),self.country)
        layout3.addRow(QLabel('Credit Card Number'),self.ccnum)
        layout3.addRow(QLabel('Expiry'),self.expiry)
        layout3.addRow(QLabel('Birthdate'),self.birthdate)
        layout3.addRow(QLabel("CVV"),self.cvv)



        form_group_box3.setLayout(layout3)

        donebutton=QPushButton('done',self)
        donebutton.clicked.connect(self.on_pushButton_clicked)
        #registerbtn.clicked.connect(self.close)

        vbox_layout3=QVBoxLayout()
        vbox_layout3.addWidget(form_group_box3)
        vbox_layout3.addWidget(donebutton)
        self.setLayout(vbox_layout3)

    def on_pushButton_clicked(self):
        email=str(self.email.text())
        user_dict['email']=email
        password=str(self.password.text())
        user_dict['password']=password
        fname=str(self.fname.text())
        user_dict['First Name']=fname
        lname=str(self.lname.text())
        user_dict['Last Name']=lname
        street=str(self.street.text())
        user_dict['Street']=street
        city=str(self.city.text())
        user_dict['City']=city
        state=str(self.state.text())
        user_dict['State']=state
        pcode=str(self.pcode.text())
        user_dict['Postal Code']=pcode
        country=str(self.country.text())
        user_dict['Country']=country
        ccnum=str(self.ccnum.text())
        user_dict['CC Number']=ccnum
        expiry=str(self.expiry.text())
        user_dict['Expiry']=expiry
        birthdate=str(self.birthdate.text())
        user_dict['Birthdate']=birthdate
        cvv = str(self.cvv.text())
        user_dict["CVV"] = cvv
        user_list.append(user_dict)
        cursor=connection.cursor()
        address_num = self.street.text().split(" ")[0]
        street_ad = self.street.text().split(" ")[1:]
        query= f"insert into address values ({address_num},{street_ad},{self.city.text()},{self.state.text()},{self.pcode.text()},{self.country.text()});"
        cursor.execute(query)
        cursor.commit()
        cursor=connection.cursor()
        query = f"select Attraction_id from address where Address_Street = {street_ad};"
        cursor.execute(query)
        for each in cursor:
            print(each)
        query = f"insert into user values ({self.email.text()},{fname} {lname}, No, Null);"
        print(user_list)
        self.close()

class adminedit(QDialog):
    def __init__(self,parent=None):
        super(adminedit,self).__init__(parent)
        self.db=QLineEdit()
        self.column=QLineEdit()
        self.oldvalue=QLineEdit()
        self.newvalue=QLineEdit()


        form_group_box4=QGroupBox("Edit Attractions")
        layout4=QFormLayout()
        layout4.addRow(QLabel('Database'),self.db)
        layout4.addRow(QLabel('Column'),self.column)
        layout4.addRow(QLabel('Old Value'),self.oldvalue)
        layout4.addRow(QLabel('New Value'),self.newvalue)
        form_group_box4.setLayout(layout4)

        vbox_layout4=QVBoxLayout()
        vbox_layout4.addWidget(form_group_box4)
        self.setLayout(vbox_layout4)

class adminpage(QDialog):
    def __init__(self,parent=None):
        super(adminpage,self).__init__(parent)
        #form_group_box5=QGroupbox("Admin Options")
        form_group_box5=QGroupBox("Admin Options")
        layout5=QFormLayout()
        admineditbtn=QPushButton('Edit Attraction',self)
        admineditbtn.clicked.connect(self.on_pushButton_clicked)
        self.dialog=adminedit2(self)
        adminupdatebtn=QPushButton('Create Attraction',self)
        adminupdatebtn.clicked.connect(self.on_pushButton_clicked2)
        self.dialog2=admincreate(self)
        admindeletebtn=QPushButton('Delete Attraction',self)
        admindeletebtn.clicked.connect(self.on_pushButton_clicked3)
        self.dialog3=admindelete(self)
        vbox_layout5=QVBoxLayout()
        vbox_layout5.addWidget(admineditbtn)
        vbox_layout5.addWidget(adminupdatebtn)
        vbox_layout5.addWidget(admindeletebtn)
        self.setLayout(vbox_layout5)

    def on_pushButton_clicked(self):
        self.dialog.show()

    def on_pushButton_clicked2(self):
        self.dialog2.show()

    def on_pushButton_clicked3(self):
        self.dialog3.show()


class admincreate(QDialog):
    def __init__(self,parent=None):
        super(admincreate,self).__init__(parent)
        self.table=QLineEdit()
        self.values=QLineEdit()

        form_group_box4=QGroupBox("Create an Attraction")
        layout4=QFormLayout()
        layout4.addRow(QLabel("Table ex(author)"),self.table)
        layout4.addRow(QLabel('values ex( (1, "Jenny","McCarthy") )'),self.values)
        form_group_box4.setLayout(layout4)

        donebutton=QPushButton('done',self)
        donebutton.clicked.connect(self.on_pushButton_clicked)

        vbox_layout4=QVBoxLayout()
        vbox_layout4.addWidget(form_group_box4)
        vbox_layout4.addWidget(donebutton)
        self.setLayout(vbox_layout4)



    def on_pushButton_clicked(self):
        table=str(self.table.text())
        values=str(self.values.text())
        cursor=connection.cursor()
        query= f"insert into {table} values {values};"
        cursor.execute(query)
        cursor.commit()
        print(query)



class admindelete(QDialog):
    def __init__(self,parent=None):
        super(admindelete,self).__init__(parent)
        self.db=QLineEdit()
        self.table=QLineEdit()
        self.expression=QLineEdit()

        form_group_box4=QGroupBox("Delete an Attraction")
        layout4=QFormLayout()
        layout4.addRow(QLabel('Database'),self.db)
        layout4.addRow(QLabel('Table (ex. author)'),self.table)
        layout4.addRow(QLabel('Expression (ex. last_name="Betty")'),self.expression)

        donebutton=QPushButton('Done',self)
        donebutton.clicked.connect(self.on_pushButton_clicked)
        self.dialog3=viewprofile(self)

        form_group_box4.setLayout(layout4)

        vbox_layout4=QVBoxLayout()
        vbox_layout4.addWidget(form_group_box4)
        vbox_layout4.addWidget(donebutton)
        self.setLayout(vbox_layout4)

    def on_pushButton_clicked(self):
        db=str(self.db.text())
        table=str(self.table.text())
        expression=str(self.expression.text())
        cursor=connection.cursor()
        query= f"delete from {table} where {expression};"
        cursor.execute(query)
        cursor.commit()
        print(query)



class OptionPage(QDialog):
    def __init__(self,parent=None):
        super(OptionPage,self).__init__(parent)
        adminbutton=QPushButton('Administrator',self)
        adminbutton.clicked.connect(self.on_pushButton_clicked)
        self.dialog=adminpage(self)
        genbutton=QPushButton('General User',self)
        genbutton.clicked.connect(self.on_pushButton_clicked2)
        self.dialog2=UserOption(login.db.text())



        vbox_layout5=QVBoxLayout()
        vbox_layout5.addWidget(adminbutton)
        vbox_layout5.addWidget(genbutton)
        self.setLayout(vbox_layout5)

    def on_pushButton_clicked(self):
        #self.dialog.show()
        text, okPressed = QInputDialog.getText(self, "Admin ID","Enter Admin ID:", QLineEdit.Normal, "")
        if okPressed and text == '4400':
            self.dialog.show()
        else:
            print('Incorrect Admin ID')
            sys.exit()

    def on_pushButton_clicked2(self):
        self.dialog2.show()

    def on_pushButton_clicked3(self):
        #self.dialog.show()
        text, okPressed = QInputDialog.getText(self, "Email","Enter Email:", QLineEdit.Normal, "")
        self.dialog3.show()

class reviewpage(QDialog):
    def __init__(self,parent=None):
        super(reviewpage,self).__init__()
        self.attractionname=QLineEdit(self)
        self.datevisited=QLineEdit(self)
        self.textbox = QTextEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(500,500)

        form_group_box6=QGroupBox()
        layout6=QFormLayout()
        layout6.addRow(QLabel('Attraction Name'),self.attractionname)
        layout6.addRow(QLabel('Date Visited'),self.datevisited)
        layout6.addRow(QLabel('Review:'),self.textbox)
        form_group_box6.setLayout(layout6)

        vbox_layout6=QVBoxLayout()
        vbox_layout6.addWidget(form_group_box6)
        self.setLayout(vbox_layout6)

class adminedit2(QDialog):
    def __init__(self,parent=None):
        super(adminedit2,self).__init__(parent)
        self.db=QLineEdit()
        self.table=QLineEdit()
        self.oldvalue=QLineEdit()
        self.newvalue=QLineEdit()


        form_group_box4=QGroupBox("Edit Attractions")
        layout4=QFormLayout()
        layout4.addRow(QLabel('Database'),self.db)
        layout4.addRow(QLabel('Table'),self.table)
        layout4.addRow(QLabel('Where ex(last_name=’McCarthy’)'),self.oldvalue)
        layout4.addRow(QLabel('New Expression ex(first_name=’John’)'),self.newvalue)
        form_group_box4.setLayout(layout4)

        donebutton=QPushButton('done',self)
        donebutton.clicked.connect(self.on_pushButton_clicked)

        vbox_layout4=QVBoxLayout()
        vbox_layout4.addWidget(form_group_box4)
        vbox_layout4.addWidget(donebutton)
        self.setLayout(vbox_layout4)


    def on_pushButton_clicked(self):
        db=str(self.db.text())
        table=str(self.table.text())
        oldvalue=str(self.oldvalue.text())
        newvalue=str(self.newvalue.text())
        cursor=connection.cursor()
        query= f"update {table} set {table}.{newvalue} where {table}.{oldvalue};"
        cursor.execute(query)
        print(query)


class UserOption(QDialog):
    def __init__(self,db):
        super(UserOption,self).__init__()
        #form_group_box5=QGroupbox("Admin Options")
        form_group_box5=QGroupBox("User Options")
        layout5=QFormLayout()
        create_tripbtn=QPushButton('Create Trip',self)
        create_tripbtn.clicked.connect(self.on_pushButton_clicked)
        tripsbtn=QPushButton('Trips',self)
        tripsbtn.clicked.connect(self.on_pushButton_clicked2)
        review_tripbtn=QPushButton('Review Trip',self)
        review_tripbtn.clicked.connect(self.on_pushButton_clicked3)
        view_profile=QPushButton('View Profile',self)
        view_profile.clicked.connect(self.on_pushButton_clicked4)
        vbox_layout5=QVBoxLayout()
        vbox_layout5.addWidget(create_tripbtn)
        vbox_layout5.addWidget(tripsbtn)
        vbox_layout5.addWidget(review_tripbtn)
        vbox_layout5.addWidget(view_profile)
        self.setLayout(vbox_layout5)

    def on_pushButton_clicked(self):
        show_at = TripMain(login.db.text())
        show_at.exec()

    def on_pushButton_clicked2(self):
        print("create trips page")
    def on_pushButton_clicked3(self):
        show_at = reviewpage(login.db.text())
        show_at.exec()
    def on_pushButton_clicked4(self):
        show_at = viewprofile(login.db.text())
        show_at.exec()

class TripMain(QDialog):
    def __init__(self,db):
            super(TripMain, self).__init__()
            self.setWindowTitle("User Window")

            self.list_view = QListView()
            self.list_model = QStandardItemModel(self.list_view)
            self.list_view.setModel(self.list_model)
            self.list_view.setSelectionMode(QAbstractItemView.SingleSelection)
            curs = connection.cursor()
            query = f"select Address_City,Address_Country from address join attraction using(Address_id)"
            curs.execute(query)
            first_row = curs.fetchone()
            rows = []
            rows.append([str(v).strip() for k, v in first_row.items()])
            for row in curs:
                    rows.append([str(v).strip() for k,v in row.items()])
            city_list = []
            for city,country in rows:
                    if (city,country) not in city_list:
                            city_list.append((city,country))
            city_list = [f"{city}, {country}" for city,country in city_list]


            self.line_edit = QLineEdit()
            self.exit_button = QPushButton("Exit")
            self.exit_button.setEnabled(True)

            self.exit_button.clicked.connect(self.close_application)

            self.show_at_button = QPushButton("Show Attractions ...")
            self.show_at_button.clicked.connect(self.show_attractions)
            self.show_at_button.setEnabled(False)
            self.list_view.clicked.connect(self.enable_show_at_button)
            self.start_date=QLineEdit(self)
            self.end_date=QLineEdit(self)
            vbox = QVBoxLayout()
            vbox.addWidget(self.list_view)
            vbox.addWidget(self.exit_button)
            vbox.addWidget(self.show_at_button)
            vbox.addWidget(self.start_date)
            vbox.addWidget(self.end_date)
            self.setLayout(vbox)

            for each in city_list:
                    list_item = QStandardItem(each)
                    self.list_model.appendRow(list_item)
                    self.line_edit.setText('')
                    self.line_edit.setFocus()

    def close_application(self):
            sys.exit()

    def show_attractions(self):
            current_index = self.list_view.currentIndex().row()
            selected_item = self.list_model.item(current_index).text()
            show_at = AttractionsInCity(login.db.text(),selected_item)
            show_at.exec()

    def enable_show_at_button(self):
            if self.list_view.currentIndex() == -1:
                self.show_at_button.setEnabled(False)
            else:
                self.show_at_button.setEnabled(True)
class AttractionsInCity(QDialog):
    def __init__(self,db,place):
            super(AttractionsInCity, self).__init__()
            self.place = place
            self.setWindowTitle("Attractions")
            message = f"Showing options for attractions for your\n trip to {place}. Choose an attraction\n below and click show attraction to \nget more information and to add the \n attraction to your trip."
            explanation = QTextEdit(message)
            explanation.setReadOnly(True)

            font = explanation.font()
            font.setFamily("Courier")
            font.setPointSize(10)
            self.list_view = QListView()
            self.list_model = QStandardItemModel(self.list_view)
            self.list_view.setModel(self.list_model)
            self.list_view.setSelectionMode(QAbstractItemView.SingleSelection)
            curs = connection.cursor()
            city = place.split(",")[0]
            country = place.split(",")[1]
            query = f"select * from attraction join address using(Address_id)"
            curs.execute(query)
            first_row = curs.fetchone()
            rows = []
            rows.append([str(v).strip() for k, v in first_row.items()])
            for row in curs:
                    rows.append([str(v).strip() for k,v in row.items()])
            at_list = []
            for row in rows:
                if row[8] == city:
                    at_list.append(row[2])
            self.line_edit = QLineEdit()
            self.ok_button = QPushButton("OK")
            self.ok_button.setEnabled(True)

            self.ok_button.clicked.connect(self.return_screen)

            self.show_at_button = QPushButton("Show Attraction ...")
            self.show_at_button.clicked.connect(self.show_attraction)
            self.show_at_button.setEnabled(False)
            self.list_view.clicked.connect(self.enable_show_at_button)

            vbox = QVBoxLayout()
            vbox.addWidget(explanation)
            vbox.addWidget(self.list_view)
            vbox.addWidget(self.ok_button)
            vbox.addWidget(self.show_at_button)
            self.setLayout(vbox)
            for each in at_list:
                list_item = QStandardItem(each)
                self.list_model.appendRow(list_item)
                self.line_edit.setText('')
                self.line_edit.setFocus()
    def return_screen(self):
            self.close()

    def enable_show_at_button(self):
            if self.list_view.currentIndex() == -1:
                self.show_at_button.setEnabled(False)
            else:
                self.show_at_button.setEnabled(True)
    def show_attraction(self):
            current_index = self.list_view.currentIndex().row()
            selected_item = self.list_model.item(current_index).text()
            show_at = Attraction(login.db.text(),selected_item,self.place)
            show_at.exec()
class Attraction(QDialog):
    def __init__(self,db,attraction,place):
            super(Attraction, self).__init__()
            self.setWindowTitle("Attraction Details")
            self.setWindowTitle("Attractions")
            message = f"Showing details for {attraction} for your\n trip to {place}. Click 'Add Attraction' \nto add {attraction} to your trip."
            explanation = QTextEdit(message)
            explanation.setReadOnly(True)

            font = explanation.font()
            font.setFamily("Courier")
            font.setPointSize(10)
            self.list_view = QListView()
            self.list_model = QStandardItemModel(self.list_view)
            self.list_view.setModel(self.list_model)
            self.list_view.setSelectionMode(QAbstractItemView.SingleSelection)
            curs = connection.cursor()
            query = f"select * from address join attraction using(Address_id)"
            curs.execute(query)
            first_row = curs.fetchone()
            rows = []
            rows.append([str(v).strip() for k, v in first_row.items()])
            for row in curs:
                    rows.append([str(v).strip() for k,v in row.items()])
            at_desc = ""
            for row in rows:
                if row[8] == attraction:
                        name,des,num,street,zip_code,city,country = row[8],row[9],row[1],row[2],row[5],row[3],row[6]
                        at_desc = f"{name} is located at {num} {street} {city}, {country} {zip_code} and has the following description: {des}"

            self.line_edit = QLineEdit()
            self.ok_button = QPushButton("OK")
            self.ok_button.setEnabled(True)

            self.ok_button.clicked.connect(self.return_screen)

            self.add_attraction = QPushButton("Add Attraction ...")
            self.add_attraction.clicked.connect(self.add_att)
            self.add_attraction.setEnabled(False)
            self.list_view.clicked.connect(self.enable_show_at_button)

            vbox = QVBoxLayout()
            vbox.addWidget(explanation)
            vbox.addWidget(self.list_view)
            vbox.addWidget(self.ok_button)
            vbox.addWidget(self.add_attraction)
            self.setLayout(vbox)
            list_item = QStandardItem(at_desc)
            self.list_model.appendRow(list_item)
            self.line_edit.setText('')
            self.line_edit.setFocus()
    def return_screen(self):
            self.close()

    def enable_show_at_button(self):
            if self.list_view.currentIndex() == -1:
                self.add_attraction.setEnabled(False)
            else:
                self.add_attraction.setEnabled(True)
    def add_att(self):
            current_index = self.list_view.currentIndex().row()
            selected_item = self.list_model.item(current_index).text()
            cursor=connection.cursor()
            query= f"insert into trip values ();"
            cursor.execute(query)
            cursor.commit()
            show_at = AttractionsInCity(login.db.text(),selected_item)
            show_at.exec()
class TripsPage(QDialog):
    def __init__(self,db):
            super(TripsPage, self).__init__()
            self.setWindowTitle("Your Trips")

            self.list_view = QListView()
            self.list_model = QStandardItemModel(self.list_view)
            self.list_view.setModel(self.list_model)
            self.list_view.setSelectionMode(QAbstractItemView.SingleSelection)
            curs = connection.cursor()
            query = f"select * from {db}"
            curs.execute(query)
            first_row = curs.fetchone()
            rows = []
            rows.append([str(v).strip() for k, v in first_row.items()])
            for row in curs:
                    rows.append([str(v).strip() for k,v in row.items()])
            at_desc = ""
            for row in rows:
                    if row[1] == attraction:
                            name,des,num,street,zip_code,city,country = row[1],row[2],row[3],row[4],row[5],row[6],row[7]
                            at_desc = f"{name} is a {des} located at {num} {street} {city}, {country} {zip_code}"

            self.line_edit = QLineEdit()
            self.ok_button = QPushButton("OK")
            self.ok_button.setEnabled(True)

            self.ok_button.clicked.connect(self.return_screen)

            self.trip_details = QPushButton("See Trip Details ...")
            self.trip_details.clicked.connect(self.each_trip)
            self.trip_details.setEnabled(False)
            self.list_view.clicked.connect(self.enable_show_at_button)

            vbox = QVBoxLayout()
            vbox.addWidget(self.list_view)
            vbox.addWidget(self.ok_button)
            vbox.addWidget(self.trip_details)
            self.setLayout(vbox)
            list_item = QStandardItem(at_desc)
            self.list_model.appendRow(list_item)
            self.line_edit.setText('')
            self.line_edit.setFocus()
    def return_screen(self):
            self.close()

    def enable_show_at_button(self):
            if self.list_view.currentIndex() == -1:
                self.add_attraction.setEnabled(False)
            else:
                self.add_attraction.setEnabled(True)
    def each_trip(self):
            current_index = self.list_view.currentIndex().row()
            selected_item = self.list_model.item(current_index).text()
            show_at = EachTrip(login.db.text(),selected_item)
            show_at.exec()

class EachTrip(QDialog):
    def __init__(self,db,trip):
            super(EachTrip, self).__init__()
            self.setWindowTitle(f"{trip} Trip")

            self.list_view = QListView()
            self.list_model = QStandardItemModel(self.list_view)
            self.list_view.setModel(self.list_model)
            self.list_view.setSelectionMode(QAbstractItemView.SingleSelection)
            curs = connection.cursor()
            query = f"select * from {db}"
            curs.execute(query)
            first_row = curs.fetchone()
            rows = []
            rows.append([str(v).strip() for k, v in first_row.items()])
            for row in curs:
                    rows.append([str(v).strip() for k,v in row.items()])
            at_desc = ""
            for row in rows:
                    if row[1] == attraction:
                            name,des,num,street,zip_code,city,country = row[1],row[2],row[3],row[4],row[5],row[6],row[7]
                            at_desc = f"{name} is a {des} located at {num} {street} {city}, {country} {zip_code}"

            self.line_edit = QLineEdit()
            self.ok_button = QPushButton("OK")
            self.ok_button.setEnabled(True)

            self.ok_button.clicked.connect(self.return_screen)

            self.attraction_details = QPushButton("See Attraction Details ...")
            self.attraction_details.clicked.connect(self.attraction_dealts)
            self.attraction_details.setEnabled(False)
            self.list_view.clicked.connect(self.enable_show_at_button)

            vbox = QVBoxLayout()
            vbox.addWidget(self.list_view)
            vbox.addWidget(self.ok_button)
            vbox.addWidget(self.attraction_details)
            self.setLayout(vbox)
            list_item = QStandardItem(at_desc)
            self.list_model.appendRow(list_item)
            self.line_edit.setText('')
            self.line_edit.setFocus()
    def return_screen(self):
            self.close()

    def enable_show_at_button(self):
            if self.list_view.currentIndex() == -1:
                self.add_attraction.setEnabled(False)
            else:
                self.add_attraction.setEnabled(True)
    def attraction_dealts(self):
            current_index = self.list_view.currentIndex().row()
            selected_item = self.list_model.item(current_index).text()
            show_at = AttractionPt2(login.db.text(),selected_item)
            show_at.exec()
class AttractionPt2(QDialog):
    def __init__(self,db,attraction):
        super(Attraction, self).__init__()
        self.setWindowTitle("Attraction Details")

        self.list_view = QListView()
        self.list_model = QStandardItemModel(self.list_view)
        self.list_view.setModel(self.list_model)
        self.list_view.setSelectionMode(QAbstractItemView.SingleSelection)
        curs = connection.cursor()
        query = f"select * from {db}"
        curs.execute(query)
        first_row = curs.fetchone()
        rows = []
        rows.append([str(v).strip() for k, v in first_row.items()])
        for row in curs:
                rows.append([str(v).strip() for k,v in row.items()])
        at_desc = ""
        for row in rows:
                if row[1] == attraction:
                        name,des,num,street,zip_code,city,country = row[1],row[2],row[3],row[4],row[5],row[6],row[7]
                        at_desc = f"{name} is a {des} located at {num} {street} {city}, {country} {zip_code}"

        self.line_edit = QLineEdit()
        self.ok_button = QPushButton("OK")
        self.ok_button.setEnabled(True)

        self.ok_button.clicked.connect(self.return_screen)

        vbox = QVBoxLayout()
        vbox.addWidget(self.list_view)
        vbox.addWidget(self.ok_button)
        self.setLayout(vbox)
        list_item = QStandardItem(at_desc)
        self.list_model.appendRow(list_item)
        self.line_edit.setText('')
        self.line_edit.setFocus()
    def return_screen(self):
            self.close()



if __name__=='__main__':
    app = QApplication(sys.argv)


    login = DbLoginDialog()

    # This is how you check which button the user used to dismiss the dialog.
    if login.exec() == QDialog.Accepted:
        # connection is global so we can use it in any class, function, or method
        # defined in this module
        global connection
        try:
            connection = pymysql.connect(host=login.host.text(),
                                         user=login.user.text(),
                                         password=login.password.text(),
                                         db=login.db.text(),
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            print(f"Couldn't log {login.user.text()} in to MySQL server on {login.host.text()}")
            print(e)
            qApp.quit()
            sys.exit()
        optionpage= OptionPage()
        optionpage.show()
        #main = MainWindow(login.db.text())
        #main.show()
        sys.exit(app.exec_())
    else:
        qApp.quit()
