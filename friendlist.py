# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 18 14:00:49 2023

@author: Lenovo
"""

import psycopg2
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QComboBox, QCheckBox, QLineEdit, QDialog, QScrollBar, QLabel, QTableWidget
# app = QApplication([])
# label = QLabel("merhaba")
# label.show()

# app.exec()



database_name = "gamepass"
user_name = "postgres"
password = "1234"
host_ip = "127.0.0.1"
host_port = "5432"

baglanti = psycopg2.connect(database = database_name,
                             user = user_name,
                             password =password,
                             host = host_ip,
                             port = host_port)

baglanti.autocommit = True
cursor = baglanti.cursor()


from PyQt6.QtWidgets import QApplication, QWidget,QTabWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

class SearchWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Arkadaş Listesi")
        
        self.name_label = QLabel("İsim:")
        self.name_edit = QLineEdit()   
        self.surname_label = QLabel("Soyisim:")
        self.surname_edit = QLineEdit()     
        self.search_button = QPushButton("Ara")
        self.search_button.clicked.connect(self.search)     
        self.result_label = QLabel()
        
        search_layout = QVBoxLayout()
        search_layout.addWidget(self.name_label)
        search_layout.addWidget(self.name_edit)
        search_layout.addWidget(self.surname_label)
        search_layout.addWidget(self.surname_edit)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.result_label)
        
        self.search_tab = QWidget()
        self.search_tab.setLayout(search_layout)
        
        
        self.nickname_label = QLabel("Kendi kullanici adinizi giriniz.:")
        self.nickname1_edit = QLineEdit()
        self.nickname2_label = QLabel("Eklemek istediğiniz kisinin kullanici adinizi giriniz.:")
        self.nickname2_edit = QLineEdit()
        self.send_button = QPushButton("Arkadaşlık isteği gönder")
        self.send_button.clicked.connect(self.istek)
        self.result2_label = QLabel()     
        
        nickname_layout = QVBoxLayout()
        nickname_layout.addWidget(self.nickname_label)
        nickname_layout.addWidget(self.nickname1_edit)
        nickname_layout.addWidget(self.nickname2_label)
        nickname_layout.addWidget(self.nickname2_edit)
        nickname_layout.addWidget(self.send_button)
        nickname_layout.addWidget(self.result2_label)
        
        self.nickname_tab = QWidget()
        self.nickname_tab.setLayout(nickname_layout)
        
        
        self.kullanici_ad_label = QLabel("Kendi kullanici adinizi giriniz:")
        self.kullanici_ad_edit = QLineEdit()
        self.istek_gor_button = QPushButton("Arkadaşlık isteklerimi gör")
        self.istek_gor_button.clicked.connect(self.istek_gor)
        
        #self.kabul_et_button_list = []  #yeni
        #self.result3_label_list = []    #yeni
        #self.result3_label = QLabel() 
        
        istek_layout = QVBoxLayout()
        istek_layout.addWidget(self.kullanici_ad_label)
        istek_layout.addWidget(self.kullanici_ad_edit)
        istek_layout.addWidget(self.istek_gor_button)
       
        #istek_layout.addWidget(self.result3_label)
         
        
        self.istek_tab = QWidget()
        self.istek_tab.setLayout(istek_layout)
        
        
        
        self.kullanici_isim_label = QLabel("Kendi kullanici adinizi giriniz:")
        self.kullanici_isim_edit = QLineEdit()
        self.engellenecek_isim_label = QLabel("Engellemek istediğiniz kişinin kullanıcı adınızı yazınız:")
        self.kullanici_isim_engel_edit = QLineEdit()
        self.engelle_button = QPushButton("Engelle")
        self.engelle_button.clicked.connect(self.engelle)
        self.result4_label = QLabel()
   
        
        engel_layout = QVBoxLayout()
        engel_layout.addWidget(self.kullanici_isim_label)
        engel_layout.addWidget(self.kullanici_isim_edit)
        engel_layout.addWidget(self.engellenecek_isim_label)
        engel_layout.addWidget(self.kullanici_isim_engel_edit)
        engel_layout.addWidget(self.engelle_button)
        engel_layout.addWidget(self.result4_label)
        
        self.engel_tab = QWidget()
        self.engel_tab.setLayout(engel_layout)
    
    
        self.kullanici_adi_label =  QLabel("Kullanici adinizi giriniz:")
        self.kullanici_adi_edit = QLineEdit()
        self.engel_liste_button = QPushButton("Engel Listemi gör")
        self.engel_liste_button.clicked.connect(self.engel_liste)
        #self.result5_label = QLabel()
    
        engel_liste_layout = QVBoxLayout()
        engel_liste_layout.addWidget(self.kullanici_adi_label)
        engel_liste_layout.addWidget(self.kullanici_adi_edit)
        engel_liste_layout.addWidget(self.engel_liste_button)
        #engel_liste_layout.addWidget(self.result5_label)
    
        self.engel_liste_tab = QWidget()
        self.engel_liste_tab.setLayout(engel_liste_layout)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.search_tab, "Arkadaş Bul")
        self.tab_widget.addTab(self.nickname_tab, "Arkadaş Ekle")
        self.tab_widget.addTab(self.istek_tab, "İsteklerim")
        self.tab_widget.addTab(self.engel_tab, "Engelle")
        self.tab_widget.addTab(self.engel_liste_tab, "Engel Listesi")
        
        
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)

        self.setLayout(layout)        


    def search(self):
        name = self.name_edit.text()
        surname = self.surname_edit.text()
        query = "select takma_ad from kullanici where ad = %s and soyad = %s"
        params = (name, surname)
        cursor.execute(query,params)
        degerler = cursor.fetchall()
        for deger in degerler:
          result = f"Arama Sonuçları:\nİsim: {deger[0]}\n"
        self.result_label.setText(result)
    def istek(self):
        nickname1 = self.nickname1_edit.text()
        nickname2 = self.nickname2_edit.text()
        
        query = "select kullanici_id from kullanici where takma_ad = %s"
        param = (nickname1,)
        cursor.execute(query,param)
        kullanici1_id = cursor.fetchall()        
        
        query2 = "select kullanici_id from kullanici where takma_ad = %s"
        param2 = (nickname2,)
        cursor.execute(query2,param2)
        kullanici2_id = cursor.fetchall()
        
        query3 = "insert into arkadaslik (kullanici_id_1, kullanici_id_2, durum, olusturma_tarihi) values ( %s, %s, 'onay_bekliyor', CURRENT_DATE)"
        param3 = (kullanici1_id[0],kullanici2_id[0])
        cursor.execute(query3,param3)
        # text = f"gonderildi!"
        self.result2_label.setText("gonderildi!")
        

        
    def istek_gor(self):
       kullanici_ad = self.kullanici_ad_edit.text()
       query = "select kullanici_id from kullanici where takma_ad = %s"
       param = (kullanici_ad,)
       cursor.execute(query,param)
       id = cursor.fetchall()
       
       query2 = "select kullanici_id_1 from arkadaslik where kullanici_id_2 = %s and durum = 'onay_bekliyor'"
       param2 = (id[0],)
       cursor.execute(query2, param2)
       istek_gonderen_id = cursor.fetchall()
       
       gonderici_ad_list = []
       for gonderen_id in istek_gonderen_id:
          query3 = "SELECT ad,soyad FROM kullanici WHERE kullanici_id = %s"
          param3 = (gonderen_id,)
          cursor.execute(query3, param3)
          istek_gonderen_ad = cursor.fetchall()
          for gonderen_ad in istek_gonderen_ad:
            gonderici_ad_list.append(gonderen_ad[0] + " " + gonderen_ad[1])
       
       i = 0
       for gonderici_ad in gonderici_ad_list:
          self.result3_label = QLabel() 
          self.result3_label.setText(gonderici_ad) 
          self.kabul_et_button = QPushButton("kabul et")
          self.kabul_et_button.clicked.connect(lambda _, user_id=id[0], friend_id=istek_gonderen_id[i]: self.kabul_et(user_id, friend_id))
          self.layout().addWidget(self.result3_label)
          self.layout().addWidget(self.kabul_et_button)    
          #self.result3_label_list.append(self.result3_label)  #yeni
          #self.kabul_et_button_list.append(self.kabul_et_button) #yeni
          i = i + 1
       # for result3_label in self.result3_label_list:
       #        self.istek_layout.addWidget(self.result3_label)
       # for kabul_et_button in self.kabul_et_button_list:
       #        self.istek_layout.addWidget(self.kabul_et_button)
          
          #self.istek_layout.addWidget(self.result3_label)  # QLabel nesnesini istek_layout'a ekleyin
          #self.istek_layout.addWidget(self.kabul_et_button)
         
      

    
    def kabul_et(self, id, istek_gonderen_id):
       query = "update arkadaslik set durum ='arkadas' where kullanici_id_1 = %s and kullanici_id_2 = %s"
       params = (istek_gonderen_id,id)  #[0] vardı
       cursor.execute(query,params)
       self.layout().removeWidget(self.result3_label)
       self.layout().removeWidget(self.kabul_et_button)
       self.result3_label.deleteLater()
       self.kabul_et_button.deleteLater()
    
    def engelle(self):
        kullanici_isim = self.kullanici_isim_edit.text()
        engel_kullanici_isim = self.kullanici_isim_engel_edit.text()
        query = "select kullanici_id from kullanici where takma_ad = %s"
        param = (kullanici_isim,)
        cursor.execute(query,param)
        kullanici =cursor.fetchall()
        for id in kullanici:
            kullanici_id = f"{id[0]}"
        param2 = (engel_kullanici_isim,)
        cursor.execute(query, param2)
        engel_kullanici = cursor.fetchall()
        for engel_id in engel_kullanici:
            engel_kullanici_id = f"{engel_id[0]}"
        query2 = """
        DO
        $$
        BEGIN
            IF EXISTS (
                SELECT * FROM arkadaslik
                WHERE (kullanici_id_1 = %s AND kullanici_id_2 = %s)
                OR (kullanici_id_2 = %s AND kullanici_id_1 = %s)
            )
            THEN
                UPDATE arkadaslik
                SET durum = 'engelli', kullanici_id_1 = %s, kullanici_id_2 = %s 
                WHERE (kullanici_id_1 = %s AND kullanici_id_2 = %s)
                OR (kullanici_id_2 = %s AND kullanici_id_1 = %s);
            ELSE
                INSERT INTO arkadaslik (kullanici_id_1, kullanici_id_2, durum, olusturma_tarihi)
                VALUES (%s, %s, 'engelli', CURRENT_DATE);
            END IF;
        END
        $$
        """
        param3 = (kullanici_id, engel_kullanici_id,kullanici_id, engel_kullanici_id,kullanici_id, engel_kullanici_id, kullanici_id, engel_kullanici_id, kullanici_id, engel_kullanici_id,kullanici_id, engel_kullanici_id )
        cursor.execute(query2,param3)
        self.result4_label.setText("engellendi!")
    def engel_liste(self):
        kullanici_isim = self.kullanici_adi_edit.text()
        query = "select kullanici_id from kullanici where takma_ad = %s"
        param = (kullanici_isim,)
        cursor.execute(query,param)
        kullanici =cursor.fetchall()
        for id in kullanici:
            kullanici_id = f"{id[0]}"
        query2 = """
        select ad, soyad from kullanici 
        where kullanici_id in
        (select kullanici_id_2 from arkadaslik
        where durum = 'engelli' and kullanici_id_1 = %s)
        """
        param2 = (kullanici_id,)
        cursor.execute(query2,param2)
        engelli =cursor.fetchall()
        engelli_list = []
        
       
        for engelli_ad in engelli:
            engelli_list.append(engelli_ad[0] + " " + engelli_ad[1])
            #engelli_isim = f"{engelli_ad[0]}"
        for engelli_isim in engelli_list:
            self.result5_label = QLabel() 
            self.result5_label.setText(engelli_isim) 
            self.layout().addWidget(self.result5_label)
        #self.result5_label.setText(engelli_isim)



       
       
if __name__ == "__main__":
    app = QApplication([])
    search_widget = SearchWidget()
    search_widget.show()
    app.exec()


# query = "select * from kullanici"
# cursor.execute(query)
# degerler = cursor.fetchall()
# for deger in degerler:
#     print(deger)