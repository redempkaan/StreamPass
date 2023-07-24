from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QComboBox, QCheckBox, QLineEdit, QDialog, QScrollBar, QLabel, QTableWidget, QListView
from PyQt6 import uic, QtWidgets
from mainwindowv12 import Ui_MainWindow
from signupv1 import Ui_SignWindow
from friendlist import SearchWidget
import psycopg2
import sys
import pandas as pd

class app(QMainWindow):
    def __init__(self):
        super(app, self).__init__()

        #Loading the UI file
        uic.loadUi("savtlogv2.ui", self)

        # Defining widgets
        self.logButton = self.findChild(QPushButton, "loginButton")
        self.passEdit = self.findChild(QLineEdit, "lineEdit_2")
        self.registerButton = self.findChild(QPushButton, "regisButton")
        self.idEdit = self.findChild(QLineEdit, "lineEdit_1")
        self.user_nick = "none"
        self.user_id = "none"
        self.activated_game = "none"

        # Adding values

        # Setting initial state of main window
        self.passEdit.setEchoMode(QLineEdit.EchoMode.Password)
        # Trigger signals
        self.logButton.clicked.connect(self.check)
        self.registerButton.clicked.connect(self.popSign)
        # Showing the app
        self.show()

    def connect_database_for_login(self):
        conn = psycopg2.connect("host=localhost dbname=gamepass user=postgres password=1234")

        # Veritabanında bir SQL sorgusu çalıştırın ve sonuçları bir değişkene atayın
        cur = conn.cursor()
        cur.execute("SELECT kullanici_id, takma_ad, email, sifre FROM kullanici WHERE email LIKE '%{}%'".format(self.idEdit.text()))
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        table = pd.DataFrame(rows, columns=colnames)
        self.dict_list = table.to_dict(orient="records")
        conn.close()

    def connect_database_for_signup(self):
        self.get_highest_id()
        conn = psycopg2.connect("host=localhost dbname=gamepass user=postgres password=1234")
        # Veritabanında bir SQL sorgusu çalıştırın ve sonuçları bir değişkene atayın
        cur = conn.cursor()
        cur.execute("INSERT INTO kullanici  VALUES ({}, 'null', 'null', '{}','01.01.2023', '{}', '{}', 'aylik');".format(self.highest_id + 1, self.registerInfos[1], self.registerInfos[0], self.registerInfos[2]));
        conn.commit()
        conn.close()

    def get_highest_id(self):
        conn = psycopg2.connect("host=localhost dbname=gamepass user=postgres password=1234")
        cur = conn.cursor()
        cur.execute("Select MAX(kullanici_id) from kullanici;")
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        table = pd.DataFrame(rows, columns=colnames)
        self.dict_list = table.to_dict(orient="records")
        conn.close()
        self.highest_id = self.dict_list[0]['max']


    def check(self):
        self.connect_database_for_login()
        print("Email : {}".format(self.dict_list[0]['email']))
        print("Password : {}".format(self.dict_list[0]['sifre']))
        if(self.passEdit.text() == self.dict_list[0]['sifre']):
            self.user_nick = self.dict_list[0]['takma_ad']
            self.user_id = self.dict_list[0]['kullanici_id']
            self.popMain()

        else:
            print("Email or password is not correct.")

    def popFriends(self):
        self.friendWindow = QtWidgets.QWidget()
        self.ui2 = SearchWidget()
        self.ui2.show()

    def popMain(self):
        self.hide()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.ui.friendButton.clicked.connect(self.popFriends)
        self.ui.playButton.clicked.connect(self.enter_game)
        self.ui.recommendButton.clicked.connect(self.recommend_game)
        self.ui.label_7.setText(self.user_nick)
        self.game_checks = [self.ui.gowCheck, self.ui.wowcCheck, self.ui.wowrCheck]
        self.game_dict = {self.ui.gowCheck : "God of War: Ragnarok", self.ui.wowcCheck : "World of Warcraft Classic", self.ui.wowrCheck : "World of Warcraft Retail"}
        self.game_data_dict = {self.ui.gowCheck : "gowragnarok", self.ui.wowcCheck : "wowclassic", self.ui.wowrCheck : "wowretail"}
        self.game_id_dict = {self.ui.gowCheck : 6, self.ui.wowcCheck : 5, self.ui.wowrCheck : 7}
        self.list_friends()
        self.window.show()


    def enter_game(self):
        for x in self.game_checks:
            if (x.isChecked()):
                self.activated_game = self.game_data_dict[x]
                self.activated_game_id = self.game_id_dict[x]
                print("Connecting database for {}.".format(self.activated_game))
                self.inc_game_time()
                print("Loading {}...".format(self.game_dict[x]))



    def inc_game_time(self):
        conn = psycopg2.connect("host=localhost dbname=gamepass user=postgres password=1234")
        cur = conn.cursor()
        cur.execute("""DO $$
BEGIN
    IF EXISTS (SELECT * FROM kullanici_oyun WHERE kullanici_id = {} AND oyun_adi = '{}') THEN
        UPDATE kullanici_oyun
        SET oynama_suresi = oynama_suresi + 1
        WHERE kullanici_id = {}  AND oyun_adi = '{}';
    ELSE
        INSERT INTO kullanici_oyun (kullanici_id, oyun_id, oyun_adi, oynama_suresi, favori_durumu)
        VALUES ({}, {}, '{}', 1, false);
   END IF;
END; $$""".format(self.user_id, self.activated_game, self.user_id, self.activated_game, self.user_id, self.activated_game_id, self.activated_game))
        conn.commit()
        conn.close()





    def recommend_game(self):
        conn = psycopg2.connect("host=localhost dbname=gamepass user=postgres password=1234")
        cur = conn.cursor()
        cur.execute("SELECT kullanici_oyun.oyun_id, oyun.kategori, oynama_suresi FROM kullanici_oyun, oyun WHERE kullanici_id = {} AND kullanici_oyun.oyun_id = oyun.oyun_id".format(self.user_id))
        colnames = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        table = pd.DataFrame(rows, columns=colnames)
        self.dict_list2 = table.to_dict(orient="records")
        print(self.dict_list2)
        self.initial_game_time = 1
        self.max_played_category = 0
        self.max_played_game_id = 0
        for x in range(len(self.dict_list2)):
            if(self.dict_list2[x]['oynama_suresi'] >= self.initial_game_time):
                self.initial_game_time = self.dict_list2[x]['oynama_suresi']
                self.max_played_category = self.dict_list2[x]['kategori']
                self.max_played_game_id = self.dict_list2[x]['oyun_id']
        conn.close()
        self.continue_recommend()

    def continue_recommend(self):
        print(self.max_played_category)
        conn = psycopg2.connect("host=localhost dbname=gamepass user=postgres password=1234")
        cur = conn.cursor()
        cur.execute("SELECT oyun_adi, oyun_id, kategori FROM oyun WHERE kategori = {} AND oyun_id != {}".format(
            self.max_played_category, self.max_played_game_id))
        colnames = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        table = pd.DataFrame(rows, columns=colnames)
        self.dict_list = table.to_dict(orient="records")
        print("Due to this user's played games, recommended game is {}.".format(self.dict_list[0]['oyun_adi']))
        conn.close()

    def list_friends(self):
        self.friend_ids = []
        conn = psycopg2.connect("host=localhost dbname=gamepass user=postgres password=1234")
        cur = conn.cursor()
        cur.execute("SELECT takma_ad, kullanici_id_2 FROM arkadaslik, kullanici WHERE kullanici_id_1 = '{}' AND arkadaslik.kullanici_id_2 = kullanici.kullanici_id".format(self.user_id))
        colnames = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        table = pd.DataFrame(rows, columns=colnames)
        self.dict_list = table.to_dict(orient="records")
        for x in range(len(self.dict_list)):
            self.ui.friendWidget.addItem(self.dict_list[x]['takma_ad'])


    def signInfos(self):
        self.registerInfos = []
        self.registerInfos.append(self.ui.lineEdit_4.text())
        self.registerInfos.append(self.ui.lineEdit_5.text())
        self.registerInfos.append(self.ui.lineEdit_6.text())
        print(self.registerInfos)
        self.connect_database_for_signup()
        self.window.hide()


    def popSign(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_SignWindow()
        self.ui.setupUi(self.window)

        #Setting initial state
        self.ui.signupButton.setEnabled(False)
        self.ui.checkBox.clicked.connect(self.activate_signup_button)
        self.ui.signupButton.clicked.connect(self.signInfos)

        self.window.show()

    def activate_signup_button(self):
        self.ui.signupButton.setEnabled(True)



main = QApplication(sys.argv)
UIWindow = app()
main.exec()




