import sys
from PyQt5.QtWidgets import *
from BCSFE_Python_Discord import *
import BCSFE_Python_Discord as BCSFE_Python
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import datetime
import os
from license_key import *
import traceback
from threading import Thread
import hashlib
from Crypto.Cipher import AES
import base64
#pip install colored tk python-dateutil requests pyyaml

form_class = uic.loadUiType("uicore.ui")[0]
form_class2 = uic.loadUiType("firstmenu.ui")[0]

BS = 16
pad = (lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode())
unpad = (lambda s: s[:-ord(s[len(s)-1:])])

class TreasuresInputDialog(QDialog):
    def __init__(self):
        super(TreasuresInputDialog, self).__init__()

        self.setWindowTitle("Move Treasures to the Right")
        self.window_width, self.window_height = 120, 80
        self.setMinimumSize(self.window_width, self.window_height)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.retrunVal = None
        self.initUI()


        self.listWidgetLeft.addItem('1. Empire of Cats 1')
        self.listWidgetLeft.addItem('2. Empire of Cats 2')
        self.listWidgetLeft.addItem('3. Empire of Cats 3')
        self.listWidgetLeft.addItem('4. Into the Future 1')
        self.listWidgetLeft.addItem('5. Into the Future 2')
        self.listWidgetLeft.addItem('6. Into the Future 3')
        self.listWidgetLeft.addItem('7. Cats of the Cosmos 1')
        self.listWidgetLeft.addItem('8. Cats of the Cosmos 2')
        self.listWidgetLeft.addItem('9. Cats of the Cosmos 3')

        self.updateButtonStatus()
        self.setButtonConnections()
        
        



    def initUI(self):
        
            subLayouts = {}

            subLayouts['LeftColumn'] = QGridLayout()
            subLayouts['RightColumn'] = QVBoxLayout()
            self.layout.addLayout(subLayouts['LeftColumn'], 1)
            self.layout.addLayout(subLayouts['RightColumn'], 1)

            self.buttons = {}
            self.buttons['>>'] = QPushButton('&>>')
            self.buttons['>'] = QPushButton('>')
            self.buttons['<'] = QPushButton('<')
            self.buttons['<<'] = QPushButton('&<<')
            self.buttons['Setup'] = QPushButton('&Setup')
            #self.buttons['Down'] = QPushButton('&Down')

            for k in self.buttons:
                self.buttons[k].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)

            """
            First Column
            """
            self.listWidgetLeft = QListWidget()
            subLayouts['LeftColumn'].addWidget(self.listWidgetLeft, 1, 0, 4, 4)

            subLayouts['LeftColumn'].setRowStretch(4, 1)
            subLayouts['LeftColumn'].addWidget(self.buttons['>>'], 1, 4, 1, 1, alignment=Qt.AlignTop)
            subLayouts['LeftColumn'].addWidget(self.buttons['<'], 2, 4, 1, 1, alignment=Qt.AlignTop)
            subLayouts['LeftColumn'].addWidget(self.buttons['>'], 3, 4, 1, 1, alignment=Qt.AlignTop)
            subLayouts['LeftColumn'].addWidget(self.buttons['<<'], 4, 4, 1, 1, alignment=Qt.AlignTop)


            """
            Second Column
            """
            self.listWidgetRight = QListWidget()

            hLayout = QHBoxLayout()
            subLayouts['RightColumn'].addLayout(hLayout)

            hLayout.addWidget(self.listWidgetRight, 4)

            vLayout = QVBoxLayout()
            hLayout.addLayout(vLayout, 1)

            vLayout.addWidget(self.buttons['Setup'])
            #vLayout.addWidget(self.buttons['Down'])
            vLayout.addStretch(1)

    def setButtonConnections(self):
        self.listWidgetLeft.itemSelectionChanged.connect(self.updateButtonStatus)
        self.listWidgetRight.itemSelectionChanged.connect(self.updateButtonStatus)

        self.buttons['>'].clicked.connect(self.buttonAddClicked)
        self.buttons['<'].clicked.connect(self.buttonRemoveClicked)
        self.buttons['>>'].clicked.connect(self.buttonAddAllClicked)
        self.buttons['<<'].clicked.connect(self.buttonRemoveAllClicked)

        self.buttons['Setup'].clicked.connect(self.buttonapplyClicked)
        #self.buttons['Down'].clicked.connect(self.buttonDownClicked)

    def buttonAddClicked(self):
        row = self.listWidgetLeft.currentRow()
        rowItem = self.listWidgetLeft.takeItem(row)
        self.listWidgetRight.addItem(rowItem)

    def buttonRemoveClicked(self):
        row = self.listWidgetRight.currentRow()
        rowItem = self.listWidgetRight.takeItem(row)
        self.listWidgetLeft.addItem(rowItem)

    def buttonAddAllClicked(self):
        for i in range(self.listWidgetLeft.count()):
            self.listWidgetRight.addItem(self.listWidgetLeft.takeItem(0))

    def buttonRemoveAllClicked(self):
        for i in range(self.listWidgetRight.count()):
            self.listWidgetLeft.addItem(self.listWidgetRight.takeItem(0))

    def buttonapplyClicked(self):
        items = []
        for i in range(self.listWidgetRight.count()):
            items.append(self.listWidgetRight.item(i).text())
        self.retrunVal = items
        self.close()
        self.w = TreasuresInputDialog()
        self.w.show()
        return self.retrunVal
        

    
        

    def updateButtonStatus(self):
        #self.buttons['Setup'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == 0)
        #self.buttons['Down'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == self.listWidgetRight.count() - 1)
        self.buttons['>'].setDisabled(not bool(self.listWidgetLeft.selectedItems()) or self.listWidgetLeft.count() == 0)
        self.buttons['<'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.count() == 0)

    def exec_(self):
        super(TreasuresInputDialog, self).exec_()
        self.buttons['Setup'].clicked.connect(self.buttonapplyClicked)
        return self.retrunVal

class MainLevelInputDialog(QDialog):
    def __init__(self):
        super(MainLevelInputDialog, self).__init__()

        self.setWindowTitle("Move Levels to the Right")
        self.window_width, self.window_height = 120, 80
        self.setMinimumSize(self.window_width, self.window_height)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.retrunVal = None
        self.initUI()


        self.listWidgetLeft.addItem('1. Empire of Cats 1')
        self.listWidgetLeft.addItem('2. Empire of Cats 2')
        self.listWidgetLeft.addItem('3. Empire of Cats 3')
        self.listWidgetLeft.addItem('4. Into the Future 1')
        self.listWidgetLeft.addItem('5. Into the Future 2')
        self.listWidgetLeft.addItem('6. Into the Future 3')
        self.listWidgetLeft.addItem('7. Cats of the Cosmos 1')
        self.listWidgetLeft.addItem('8. Cats of the Cosmos 2')
        self.listWidgetLeft.addItem('9. Cats of the Cosmos 3')

        self.updateButtonStatus()
        self.setButtonConnections()
        
        



    def initUI(self):
        
            subLayouts = {}

            subLayouts['LeftColumn'] = QGridLayout()
            subLayouts['RightColumn'] = QVBoxLayout()
            self.layout.addLayout(subLayouts['LeftColumn'], 1)
            self.layout.addLayout(subLayouts['RightColumn'], 1)

            self.buttons = {}
            self.buttons['>>'] = QPushButton('&>>')
            self.buttons['>'] = QPushButton('>')
            self.buttons['<'] = QPushButton('<')
            self.buttons['<<'] = QPushButton('&<<')
            self.buttons['Setup'] = QPushButton('&Setup')
            
            #self.buttons['Down'] = QPushButton('&Down')

            for k in self.buttons:
                self.buttons[k].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)

            """
            First Column
            """
            self.listWidgetLeft = QListWidget()
            subLayouts['LeftColumn'].addWidget(self.listWidgetLeft, 1, 0, 4, 4)

            subLayouts['LeftColumn'].setRowStretch(4, 1)
            subLayouts['LeftColumn'].addWidget(self.buttons['>>'], 1, 4, 1, 1, alignment=Qt.AlignTop)
            subLayouts['LeftColumn'].addWidget(self.buttons['<'], 2, 4, 1, 1, alignment=Qt.AlignTop)
            subLayouts['LeftColumn'].addWidget(self.buttons['>'], 3, 4, 1, 1, alignment=Qt.AlignTop)
            subLayouts['LeftColumn'].addWidget(self.buttons['<<'], 4, 4, 1, 1, alignment=Qt.AlignTop)


            """
            Second Column
            """
            self.listWidgetRight = QListWidget()

            hLayout = QHBoxLayout()
            subLayouts['RightColumn'].addLayout(hLayout)

            hLayout.addWidget(self.listWidgetRight, 4)

            vLayout = QVBoxLayout()
            hLayout.addLayout(vLayout, 1)

            vLayout.addWidget(self.buttons['Setup'])
            #vLayout.addWidget(self.buttons['Down'])
            vLayout.addStretch(1)

    def setButtonConnections(self):
        self.listWidgetLeft.itemSelectionChanged.connect(self.updateButtonStatus)
        self.listWidgetRight.itemSelectionChanged.connect(self.updateButtonStatus)

        self.buttons['>'].clicked.connect(self.buttonAddClicked)
        self.buttons['<'].clicked.connect(self.buttonRemoveClicked)
        self.buttons['>>'].clicked.connect(self.buttonAddAllClicked)
        self.buttons['<<'].clicked.connect(self.buttonRemoveAllClicked)

        self.buttons['Setup'].clicked.connect(self.buttonapplyClicked)
        #self.buttons['Down'].clicked.connect(self.buttonDownClicked)

    def buttonAddClicked(self):
        row = self.listWidgetLeft.currentRow()
        rowItem = self.listWidgetLeft.takeItem(row)
        self.listWidgetRight.addItem(rowItem)

    def buttonRemoveClicked(self):
        row = self.listWidgetRight.currentRow()
        rowItem = self.listWidgetRight.takeItem(row)
        self.listWidgetLeft.addItem(rowItem)

    def buttonAddAllClicked(self):
        for i in range(self.listWidgetLeft.count()):
            self.listWidgetRight.addItem(self.listWidgetLeft.takeItem(0))

    def buttonRemoveAllClicked(self):
        for i in range(self.listWidgetRight.count()):
            self.listWidgetLeft.addItem(self.listWidgetRight.takeItem(0))

    def buttonapplyClicked(self):
        items = []
        for i in range(self.listWidgetRight.count()):
            items.append(self.listWidgetRight.item(i).text())
        self.retrunVal = items
        self.close()
        self.w = MainLevelInputDialog()
        self.w.show()
        return self.retrunVal
        

    
        

    def updateButtonStatus(self):
        #self.buttons['Setup'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == 0)
        #self.buttons['Down'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == self.listWidgetRight.count() - 1)
        self.buttons['>'].setDisabled(not bool(self.listWidgetLeft.selectedItems()) or self.listWidgetLeft.count() == 0)
        self.buttons['<'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.count() == 0)

    def exec_(self):
        super(MainLevelInputDialog, self).exec_()
        self.buttons['Setup'].clicked.connect(self.buttonapplyClicked)
        return self.retrunVal




class AESCipher(object):
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()
    
    def encrypt(self, message):
        message = message.encode()
        raw = pad(message)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv().encode('utf8'))
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')
    
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv().encode('utf8'))
        dec = cipher.decrypt(enc)
        return unpad(dec).decode('utf-8')
    
    def __iv(self):
        return chr(0) * 16

class WindowClass2(QMainWindow, form_class2) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))
        
        if os.path.exists("key.pulsekey") == False:
            licensekey = QInputDialog.getText(self, 'License Confirm', 'Enter your License key:')
            with open("key.pulsekey", "wb+") as keyfile:
                
                key = licensekey[0]
                data = "Ic8ftx8c0l"

                aes = AESCipher(key)

                encrypt = aes.encrypt(data)
                keyfile.write(bytes(encrypt, 'utf-8'))
            with open("key2.pulsekey", "wb") as keyfile2:
                data = licensekey[0]
                key2 = "Pulservice"
                aes = AESCipher(key2)

                encrypt = aes.encrypt(data)
                keyfile2.write(bytes(encrypt, 'utf-8'))
            
                

                #decrypt = aes.decrypt(encrypt)
        
        encrypted = open("key2.pulsekey", "rb").read()
        aeskey = "Pulservice"
        cipher_key = AESCipher(aeskey)
        decrypted = cipher_key.decrypt(encrypted)

        encrypted = open("key.pulsekey", "rb").read()
        aeskey = decrypted
        cipher_key = AESCipher(aeskey)
        decrypted = cipher_key.decrypt(encrypted)

        final_key = requests.get("https://gist.githubusercontent.com/cintagram/544bbbc3dc3b55b6c7bee83a10d3f536/raw/fa39aa14c5b343441fd8d3fb6480d2cb587066ca/final_key.txt")
            
        if decrypted == final_key and licensekey[0] == "BSUCR-ZKWKM-Q9QMB-LU7RQ-BJ6U5":
            QMessageBox.critical(self, 'License Error', 'License Key Error.\nContact the Seller or Developer.',
                                            QMessageBox.Ok)
            sys.exit(1)
        else:
            QMessageBox.information(self, 'Information', 'Hello! Thanks for downloading!\nI just wanted to notice a few things before starting.\n\n1. This Editor is GUI version of CLI editor.\n2. You cant use some features yet:\n- Using adb\n- Editor Config\n- Talent orbs\n- Import from JSON file\n\nThats all! Happy editing! ;)',
                                        QMessageBox.Ok)
            #buttons
            self.loadfile_btn.clicked.connect(self.loadfile)
            self.download_btn.clicked.connect(self.downloadfile)
        
    def downloadfile(self):
        try:
            now = datetime.datetime.now()
            savetime = str(now).split(".")[0]
            
            path = helper.save_file(
                "Save save data",
                helper.get_save_file_filetype(),
                helper.get_save_path_home(),
            )
            BCSFE_Python.helper.set_save_path(path)
            country_code = self.versionbox.currentText()
            transfer_code = self.transfercode_input.text()
            confirmation_code = self.confirmcode_input.text()
            game_version = self.version_input_2.text()
            game_version = helper.str_to_gv(game_version)

            save_data = BCSFE_Python.server_handler.download_save(country_code, transfer_code, confirmation_code, game_version)
            self.progressBar.setValue(31)
            save_data = patcher.patch_save_data(save_data, country_code)
            self.progressBar.setValue(83)
            global save_stats
            save_stats = parse_save.start_parse(save_data, country_code)
            self.progressBar.setValue(100)
            self.close()
            self.w = WindowClass()
            self.w.show()
        except Exception as e:
            QMessageBox.critical(self, 'Error', '{}'.format(traceback.format_exc()),
                                    QMessageBox.Ok)
            self.progressBar.setValue(0)
            pass


    def loadfile(self):
        try:
            locale_manager = BCSFE_Python.locale_handler.LocalManager.from_config()
            path = helper.select_file(
                "Select Save File",
                helper.get_save_file_filetype(),
                initial_file=helper.get_save_path_home(),
            )
            BCSFE_Python.helper.set_save_path(path)
            self.progressBar.setValue(31)
            
            data = helper.load_save_file(path)
            global save_stats
            save_stats = data["save_stats"]
            save_data: bytes = data["save_data"]
            country_code = save_stats["version"]
            self.progressBar.setValue(67)
            save_data = patcher.patch_save_data(save_data, country_code)
            self.progressBar.setValue(78)
            save_stats = parse_save.start_parse(save_data, country_code)
            self.progressBar.setValue(100)
            
            myWindow.close()
            self.w = WindowClass()
            self.w.show()
            
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', '{}'.format(traceback.format_exc()),
                                    QMessageBox.Ok)
            self.progressBar.setValue(0)
            pass
            



class WindowClass(QMainWindow, form_class):
    def __init__(self) :
        super().__init__()
        #global save_stats
        
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))
        self.item_menu_combobox_2.setEnabled(False)
        
        self.applybutton.clicked.connect(self.edit_item)
        self.applybutton_2.clicked.connect(self.edit_cats)
        self.applybutton_3.clicked.connect(self.savefile)
        self.applybutton_4.clicked.connect(self.upload_data)
        self.select_main_levels_btn.clicked.connect(self.connect_main_level_dialog)
        self.item_menu_combobox.currentIndexChanged.connect(self.on_change)
        self.Treasures_btn.clicked.connect(self.connect_treasures_dialog)
        #self.item_menu_combobox_4.currentIndexChanged.connect(self.on_change2)


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    def on_change(self):
        try:
            self.item_menu_combobox_2.clear()
            selected = self.item_menu_combobox.currentText()
            disable = ["Cat Food", "XP", "NP", "Leadership"]
            if selected in disable:
                self.item_menu_combobox_2.setEnabled(False)
            else:
                if selected == "Tickets":
                    self.item_menu_combobox_2.setEnabled(True)
                    self.item_menu_combobox_2.addItem("Normal Ticket")
                    self.item_menu_combobox_2.addItem("Rare Ticket")
                    self.item_menu_combobox_2.addItem("Platinum Ticket")
                    self.item_menu_combobox_2.addItem("Legend Ticket")
                elif selected == "Battle Items":
                    self.item_menu_combobox_2.setEnabled(True)
                    self.item_menu_combobox_2.addItem("Speed Up")
                    self.item_menu_combobox_2.addItem("Treasure Radar")
                    self.item_menu_combobox_2.addItem("Rich Cat")
                    self.item_menu_combobox_2.addItem("Cat CPU")
                    self.item_menu_combobox_2.addItem("Cat Jobs")
                    self.item_menu_combobox_2.addItem("Sniper the Cat")
                elif selected == "Catseyes":
                    self.item_menu_combobox_2.setEnabled(True)
                    self.item_menu_combobox_2.addItem("Normal")
                    self.item_menu_combobox_2.addItem("EX")
                    self.item_menu_combobox_2.addItem("Rare")
                    self.item_menu_combobox_2.addItem("Super Rare")
                    self.item_menu_combobox_2.addItem("Uber Rare")
                    self.item_menu_combobox_2.addItem("Legend")
                elif selected == "Cat Fruit / Behemoth Stones":
                    self.item_menu_combobox_2.setEnabled(True)
                    self.item_menu_combobox_2.addItem("Select All")
                    self.item_menu_combobox_2.addItem("Purple Catfruit Seed")
                    self.item_menu_combobox_2.addItem("Red Catfruit Seed")
                    self.item_menu_combobox_2.addItem("Blue Catfruit Seed")
                    self.item_menu_combobox_2.addItem("Green Catfruit Seed")
                    self.item_menu_combobox_2.addItem("Yellow Catfruit Seed")
                    self.item_menu_combobox_2.addItem("Purple Catfruit")
                    self.item_menu_combobox_2.addItem("Red Catfruit")
                    self.item_menu_combobox_2.addItem("Blue Catfruit")
                    self.item_menu_combobox_2.addItem("Green Catfruit")
                    self.item_menu_combobox_2.addItem("Yellow Catfruit")
                    self.item_menu_combobox_2.addItem("Epic Catfruit")
                    self.item_menu_combobox_2.addItem("Elder Catfruit Seed")
                    self.item_menu_combobox_2.addItem("Elder Catfruit")
                    self.item_menu_combobox_2.addItem("Epic Catfruit Seed")
                    self.item_menu_combobox_2.addItem("Gold Catfruit")
                    self.item_menu_combobox_2.addItem("Aku Catfruit Seed")
                    self.item_menu_combobox_2.addItem("Aku Catfruit")
                    self.item_menu_combobox_2.addItem("Gold Catfruit Seed")
                    self.item_menu_combobox_2.addItem("Purple B. Stone")
                    self.item_menu_combobox_2.addItem("Red B. Stone")
                    self.item_menu_combobox_2.addItem("Blue B. Stone")
                    self.item_menu_combobox_2.addItem("Green B. Stone")
                    self.item_menu_combobox_2.addItem("Yellow B. Stone")
                    self.item_menu_combobox_2.addItem("Purple B. Gem")
                    self.item_menu_combobox_2.addItem("Red B. Gem")
                    self.item_menu_combobox_2.addItem("Blue B. Gem")
                    self.item_menu_combobox_2.addItem("Green B. Gem")
                    self.item_menu_combobox_2.addItem("Yellow B. Gem")
                    self.item_menu_combobox_2.addItem("Epic B. Stone")
                    
                elif selected == "Catamins":
                    self.item_menu_combobox_2.setEnabled(True)
                    self.item_menu_combobox_2.addItem("Select All")
                    self.item_menu_combobox_2.addItem("A")
                    self.item_menu_combobox_2.addItem("B")
                    self.item_menu_combobox_2.addItem("C")

            





        except Exception as e:
            QMessageBox.critical(self, 'Error', '{}'.format(traceback.format_exc()),
                                    QMessageBox.Ok)
            self.progressbar.setValue(0)
            pass
    
    def connect_treasures_dialog(self):
        dialog = TreasuresInputDialog()
        stages = dialog.exec_()
        if stages:
            print("Stages: {}".format(stages))
            listlength = len(stages)
            print("List Length: {}".format(listlength))
            i = 0
            level_string = ""
            for i in range(listlength):
                if "1. Empire of Cats 1" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "2. Empire of Cats 2" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "3. Empire of Cats 3" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "4. Into the Future 1" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "5. Into the Future 2" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "6. Into the Future 3" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "7. Cats of the Cosmos 1" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "8. Cats of the Cosmos 2" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "9. Cats of the Cosmos 3" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                level_string += str(str(numbers)+" ")
                i += 1
            level_list = list(level_string.split(" "))
            level_list = list(filter(None, level_list))
            level_list = [eval(i) for i in level_list]
            tre_id = QInputDialog.getText(self, 'Select Treasure', 'Enter Treasure ID\n\n3 = Superior\n2 = Normal\n1 = Inferior\n0 = None')
            if tre_id == None:
                QMessageBox.critical(self, 'Error', 'Treasure IDs must not be empty.',
                                            QMessageBox.Ok)
            else:
                edits.levels.treasures.specific_stages_all_chapters(save_stats, level_list, tre_id)
                self.progressbar.setValue(100)
                QMessageBox.information(self, 'Success', 'Successfully Set Treasures in Selected Levels',
                                                QMessageBox.Ok)
                self.progressbar.setValue(0)

    def connect_main_level_dialog(self):
        dialog = MainLevelInputDialog()
        stages = dialog.exec_()
        if stages:
            print("Stages: {}".format(stages))
            listlength = len(stages)
            print("List Length: {}".format(listlength))
            i = 0
            level_string = ""
            for i in range(listlength):
                if "1. Empire of Cats 1" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "2. Empire of Cats 2" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "3. Empire of Cats 3" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "4. Into the Future 1" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "5. Into the Future 2" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "6. Into the Future 3" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "7. Cats of the Cosmos 1" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "8. Cats of the Cosmos 2" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                elif "9. Cats of the Cosmos 3" in str(stages[i]):
                    numbers = int(str(stages[i]).split(".")[0]) - 1
                level_string += str(str(numbers)+" ")
                i += 1
            level_list = list(level_string.split(" "))
            level_list = list(filter(None, level_list))
            level_list = [eval(i) for i in level_list]
            edits.levels.main_story.clear_all(save_stats, level_list)
            self.progressbar.setValue(100)
            QMessageBox.information(self, 'Success', 'Successfully Cleared Selected Levels',
                                            QMessageBox.Ok)
            self.progressbar.setValue(0)



            
                


        

        

        
    def upload_data(self):
        try:
            edits.save_management.save.save_save(save_stats)
            save_data = BCSFE_Python.serialise_save.start_serialize(save_stats)
            self.progressbar.setValue(31)
            save_data = BCSFE_Python.helper.write_save_data(
                save_data, save_stats["version"], helper.get_save_path(), False
            )
            self.progressbar.setValue(78)
            upload_data = BCSFE_Python.server_handler.upload_handler(save_stats, helper.get_save_path())
            transfer_code = upload_data['transferCode']
            confirmation_code = upload_data['pin']
            self.progressbar.setValue(99)
            desktop = os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "account_code.txt") 
            with open(desktop, "w+", encoding="utf-8") as file:
                file.write("Transfer Code: {}\nConfirmation Code: {}".format(transfer_code, confirmation_code))
            self.progressbar.setValue(100)
            QMessageBox.information(self, 'Success', 'Successfully uploaded data and write code to: [Desktop\\account_code.txt]',
                                        QMessageBox.Ok)
            self.progressbar.setValue(0)
        except Exception as e:
            QMessageBox.critical(self, 'Error', '{}'.format(traceback.format_exc()),
                                    QMessageBox.Ok)
            self.progressbar.setValue(0)
            pass
    def savefile(self):
        try:
            edits.save_management.save.save_save(save_stats)
            QMessageBox.information(self, 'Success', 'Successfully saved data',
                                        QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, 'Error', '{}'.format(traceback.format_exc()),
                                    QMessageBox.Ok)
            self.progressbar.setValue(0)
            pass
    
    def edit_cats(self):
        #global save_stats
        try:
            self.progressbar.setValue(100)
            selected = self.item_menu_combobox_4.currentText()
            if selected == "Add Cats with Levels":
                id = str(self.amountinput_2.text())
                if id == "all" or id == "All":
                    cat_id = edits.cats.cat_id_selector.filter_obtainable_cats(save_stats, edits.cats.cat_id_selector.get_all_cats(save_stats))
                    ids = helper.check_cat_ids(cat_id, save_stats)
                    levels = str(self.amountinput_3.text())
                    cats = save_stats["cats"]

                    for cat_id in ids:
                        cats[cat_id] = 1

                    save_stats["cats"] = cats
                    save_stats["menu_unlocks"][2] = 1
                    save_stats["cat_upgrades"] = edits.cats.upgrade_cats.upgrade_handler(
                        data=save_stats["cat_upgrades"],
                        ids=ids,
                        level=levels,
                        item_name="cat",
                        save_stats=save_stats,
                    )
                    edits.cats.upgrade_cats.set_user_popups(save_stats)
                    edits.cats.upgrade_cats.set_level_caps(save_stats)
						

                    QMessageBox.information(self, 'Success', 'Successfully added [All] Cats with [{}] level'.format(levels),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
                else:
                    ids = user_input_handler.get_range(
                        id,
                        length=len(save_stats["cats"]),
                    )
                    ids = helper.check_cat_ids(ids, save_stats)
                    levels = str(self.amountinput_3.text())
                    cats = save_stats["cats"]

                    for cat_id in ids:
                        cats[cat_id] = 1
                    
                    
                    save_stats["cats"] = cats
                    save_stats["menu_unlocks"][2] = 1
                    save_stats["cat_upgrades"] = edits.cats.upgrade_cats.upgrade_handler(
                        data=save_stats["cat_upgrades"],
                        ids=ids,
                        level=levels,
                        item_name="cat",
                        save_stats=save_stats,
                    )
                    edits.cats.upgrade_cats.set_user_popups(save_stats)
                    edits.cats.upgrade_cats.set_level_caps(save_stats)
                    QMessageBox.information(self, 'Success', 'Successfully added [{}] Cats with [{}] level'.format(id, levels),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
            elif selected == "Delete Cats":
                id = str(self.amountinput_2.text())
                if id == "all" or id == "All":
                    cat_id = edits.cats.cat_id_selector.filter_obtainable_cats(save_stats, edits.cats.cat_id_selector.get_all_cats(save_stats))
                    ids = helper.check_cat_ids(cat_id, save_stats)
                    levels = str(self.amountinput_3.text())
                    cats = save_stats["cats"]

                    for cat_id in ids:
                        cats[cat_id] = 0

                    save_stats["cats"] = cats
                    save_stats["menu_unlocks"][2] = 1
                    save_stats["cat_upgrades"] = edits.cats.upgrade_cats.upgrade_handler(
                        data=save_stats["cat_upgrades"],
                        ids=ids,
                        level=levels,
                        item_name="cat",
                        save_stats=save_stats,
                    )
                    edits.cats.upgrade_cats.set_user_popups(save_stats)
                    edits.cats.upgrade_cats.set_level_caps(save_stats)
						

                    QMessageBox.information(self, 'Success', 'Successfully added [All] Cats with [{}] level'.format(levels),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
                else:
                    ids = user_input_handler.get_range(
                        id,
                        length=len(save_stats["cats"]),
                    )
                    ids = helper.check_cat_ids(ids, save_stats)
                    levels = str(self.amountinput_3.text())
                    cats = save_stats["cats"]

                    for cat_id in ids:
                        cats[cat_id] = 0
                    
                    
                    save_stats["cats"] = cats
                    save_stats["menu_unlocks"][2] = 1
                    save_stats["cat_upgrades"] = edits.cats.upgrade_cats.upgrade_handler(
                        data=save_stats["cat_upgrades"],
                        ids=ids,
                        level=levels,
                        item_name="cat",
                        save_stats=save_stats,
                    )
                    edits.cats.upgrade_cats.set_user_popups(save_stats)
                    edits.cats.upgrade_cats.set_level_caps(save_stats)
                    QMessageBox.information(self, 'Success', 'Successfully added [{}] Cats with [{}] level'.format(id, levels),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
            elif selected == "Upgrade Cats":
                id = str(self.amountinput_2.text())
                if id == "all" or id == "All":
                    cat_id = edits.cats.cat_id_selector.filter_obtainable_cats(save_stats, edits.cats.cat_id_selector.get_all_cats(save_stats))
                    ids = helper.check_cat_ids(cat_id, save_stats)
                    levels = str(self.amountinput_3.text())
                    save_stats["cat_upgrades"] = edits.cats.upgrade_cats.upgrade_handler(
							data=save_stats["cat_upgrades"],
							ids=ids,
							level=levels,
							item_name="cat",
							save_stats=save_stats,
						)
                    edits.cats.upgrade_cats.set_user_popups(save_stats)
                    edits.cats.upgrade_cats.set_level_caps(save_stats)
                    QMessageBox.information(self, 'Success', 'Successfully set [{}] Cats with [{}] level'.format(id, levels),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
                else:
                    ids = user_input_handler.get_range(
                        id,
                        length=len(save_stats["cats"]),
                    )
                    ids = helper.check_cat_ids(ids, save_stats)
                    levels = str(self.amountinput_3.text())
                    save_stats["cat_upgrades"] = edits.cats.upgrade_cats.upgrade_handler(
                        data=save_stats["cat_upgrades"],
                        ids=ids,
                        level=levels,
                        item_name="cat",
                        save_stats=save_stats,
                    )
                    edits.cats.upgrade_cats.set_user_popups(save_stats)
                    edits.cats.upgrade_cats.set_level_caps(save_stats)
                    QMessageBox.information(self, 'Success', 'Successfully set [{}] Cats with [{}] level'.format(id, levels),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
            elif selected == "True Form Cats":
                id = str(self.amountinput_2.text())
                if id == "all" or id == "All":
                    ids = edits.cats.cat_id_selector.filter_obtainable_cats(save_stats, edits.cats.cat_id_selector.get_all_cats(save_stats))
                    edits.cats.evolve_cats.evolve_handler_ids(
                        save_stats=save_stats,
                        val=2,
                        string="set",
                        ids=ids,
                        forced=False,
                    )
                    QMessageBox.information(self, 'Success', 'Successfully set [{}] Cats evolved'.format(id),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
                else:
                    ids = user_input_handler.get_range(
							str(id),
							length=len(save_stats["cats"]),
                    )
                    edits.cats.evolve_cats.evolve_handler_ids(
                        save_stats=save_stats,
                        val=2,
                        string="set",
                        ids=ids,
                        forced=False,
                    )
                    QMessageBox.information(self, 'Success', 'Successfully set [{}] Cats evolved'.format(id),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
                

        except Exception as e:
            QMessageBox.critical(self, 'Error', '{}'.format(traceback.format_exc()),
                                    QMessageBox.Ok)
            self.progressbar.setValue(0)
            pass

    def edit_item(self):
        try:
            self.progressbar.setValue(100)
            selected = self.item_menu_combobox.currentText()
            if selected == "Cat Food":
                amount = int(self.amountinput.text())
                intamount = int(amount)
                if intamount >= 45001:
                    QMessageBox.warning(self, 'Warning', 'Max value for [Cat Food] is 45000',
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
                else:
                    try:
                        save_stats["cat_food"]["Value"] = intamount
                        edits.save_management.save.save_save(save_stats)
                        self.progressbar.setValue(100)
                        QMessageBox.information(self, 'Success', 'Successfully changed [Cat Food] value to {}'.format(intamount),
                                        QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    except Exception as e:
                        QMessageBox.critical(self, 'Error', '{}'.format(traceback.format_exc()),
                                                QMessageBox.Ok)
                        self.progressbar.setValue(0)
                        pass
            elif selected == "XP":
                amount = int(self.amountinput.text())
                intamount = int(amount)
                if intamount >= 100000000:
                    QMessageBox.warning(self, 'Warning', 'Max value for [XP] is 99999999',
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
                else:
                    try:
                        save_stats["xp"]["Value"] = intamount
                        edits.save_management.save.save_save(save_stats)
                        self.progressbar.setValue(100)
                        QMessageBox.information(self, 'Success', 'Successfully changed [XP] value to {}'.format(intamount),
                                        QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    except Exception as e:
                        QMessageBox.critical(self, 'Error', '{}'.format(traceback.format_exc()),
                                                QMessageBox.Ok)
                        self.progressbar.setValue(0)
                        pass
            elif selected == "Tickets":
                ticket_type = self.item_menu_combobox_2.currentText()
                amount = int(self.amountinput.text())
                if ticket_type == "Normal Ticket":
                    max = 3000
                    if amount >= max:
                        QMessageBox.warning(self, 'Warning', 'Max value for [Normal Ticket] is {}'.format(max-1),
                                        QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    else:
                        save_stats["normal_tickets"]["Value"] = amount
                        QMessageBox.information(self, 'Success', 'Successfully changed [Normal Ticket] value to {}'.format(amount),
                                        QMessageBox.Ok)
                        self.progressbar.setValue(0)
                elif ticket_type == "Rare Ticket":
                    max = 300
                    if amount >= max:
                        QMessageBox.warning(self, 'Warning', 'Max value for [Rare Ticket] is {}'.format(max-1),
                                        QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    else:
                        save_stats["rare_tickets"]["Value"] = amount
                        QMessageBox.information(self, 'Success', 'Successfully changed [Rare Ticket] value to {}'.format(amount),
                                        QMessageBox.Ok)
                        self.progressbar.setValue(0)
                elif ticket_type == "Platinum Ticket":
                    max = 10
                    if amount >= max:
                        QMessageBox.warning(self, 'Warning', 'Max value for [Platinum Ticket] is {}'.format(max-1),
                                        QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    else:
                        save_stats["platinum_tickets"]["Value"] = amount
                        QMessageBox.information(self, 'Success', 'Successfully changed [Platinum Ticket] value to {}'.format(amount),
                                        QMessageBox.Ok)
                        self.progressbar.setValue(0)
                elif ticket_type == "Legend Ticket":
                    max = 5
                    if amount >= max:
                        QMessageBox.warning(self, 'Warning', 'Max value for [Legend Ticket] is {}'.format(max-1),
                                        QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    else:
                        save_stats["legend_tickets"]["Value"] = amount
                        QMessageBox.information(self, 'Success', 'Successfully changed [Legend Ticket] value to {}'.format(amount),
                                        QMessageBox.Ok)
                        self.progressbar.setValue(0)
                else:
                    QMessageBox.warning(self, 'Warning', 'Invalid ticket type',
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
            elif selected == "NP":
                amount = int(self.amountinput.text())
                max = 10000
                if amount >= max:
                    QMessageBox.warning(self, 'Warning', 'Max value for [NP] is {}'.format(max-1),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
                else:
                    save_stats["np"]["Value"] = amount
                    QMessageBox.information(self, 'Success', 'Successfully changed [NP] value to {}'.format(amount),
                                            QMessageBox.Ok)
                    self.progressbar.setValue(0)
            elif selected == "Leadership":
                amount = int(self.amountinput.text())
                max = 10000
                if amount >= max:
                    QMessageBox.warning(self, 'Warning', 'Max value for [Leadership] is {}'.format(max-1),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
                else:
                    save_stats["leadership"]["Value"] = amount
                    QMessageBox.information(self, 'Success', 'Successfully changed [Leadership] value to {}'.format(amount),
                                            QMessageBox.Ok)
                    self.progressbar.setValue(0)
            elif selected == "Battle Items":
                amount = int(self.amountinput.text())
                max = 10000
                if amount >= max:
                    QMessageBox.warning(self, 'Warning', 'Max value for [Battle Items] is {}'.format(max-1),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
                else:
                    item_type = self.item_menu_combobox_2.currentText()
                    if item_type == "Speed Up":
                        save_stats["battle_items"][0] = amount
                        QMessageBox.information(self, 'Success', 'Successfully changed [Speed Up] value to {}'.format(amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Treasure Radar":
                        save_stats["battle_items"][1] = amount
                        QMessageBox.information(self, 'Success', 'Successfully changed [Treasure Radar] value to {}'.format(amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Rich Cat":
                        save_stats["battle_items"][2] = amount
                        QMessageBox.information(self, 'Success', 'Successfully changed [Rich Cat] value to {}'.format(amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Cat CPU":
                        save_stats["battle_items"][3] = amount
                        QMessageBox.information(self, 'Success', 'Successfully changed [Cat CPU] value to {}'.format(amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Cat Jobs":
                        save_stats["battle_items"][4] = amount
                        QMessageBox.information(self, 'Success', 'Successfully changed [Cat Jobs] value to {}'.format(amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Sniper the Cat":
                        save_stats["battle_items"][5] = amount
                        QMessageBox.information(self, 'Success', 'Successfully changed [Sniper the Cat] value to {}'.format(amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    else:
                        QMessageBox.warning(self, 'Warning', 'Invalid item type',
                                        QMessageBox.Ok)
                        self.progressbar.setValue(0)
            elif selected == "Cat Fruit / Behemoth Stones":
                amount = int(self.amountinput.text())
                item_type = self.item_menu_combobox_2.currentText()
                max = 10000
                if amount >= max:
                    QMessageBox.warning(self, 'Warning', 'Max value for [Cat Fruit / Behemoth Stones] is {}'.format(max-1),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
                else:
                    value = amount
                    if item_type == "Select All":
                        
                        save_stats["cat_fruit"][0] = value
                        save_stats["cat_fruit"][1] = value
                        save_stats["cat_fruit"][2] = value
                        save_stats["cat_fruit"][3] = value
                        save_stats["cat_fruit"][4] = value
                        save_stats["cat_fruit"][5] = value
                        save_stats["cat_fruit"][6] = value
                        save_stats["cat_fruit"][7] = value
                        save_stats["cat_fruit"][8] = value
                        save_stats["cat_fruit"][9] = value
                        save_stats["cat_fruit"][10] = value
                        save_stats["cat_fruit"][11] = value
                        save_stats["cat_fruit"][12] = value
                        save_stats["cat_fruit"][13] = value
                        save_stats["cat_fruit"][14] = value
                        save_stats["cat_fruit"][15] = value
                        save_stats["cat_fruit"][16] = value
                        save_stats["cat_fruit"][17] = value
                        save_stats["cat_fruit"][18] = value
                        save_stats["cat_fruit"][19] = value
                        save_stats["cat_fruit"][20] = value
                        save_stats["cat_fruit"][21] = value
                        save_stats["cat_fruit"][22] = value
                        save_stats["cat_fruit"][23] = value
                        save_stats["cat_fruit"][24] = value
                        save_stats["cat_fruit"][25] = value
                        save_stats["cat_fruit"][26] = value
                        save_stats["cat_fruit"][27] = value
                        save_stats["cat_fruit"][28] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(selected, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Purple Catfruit Seed":
                        save_stats["cat_fruit"][0] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Red Catfruit Seed":
                        save_stats["cat_fruit"][1] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Blue Catfruit Seed":
                        save_stats["cat_fruit"][2] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Green Catfruit Seed":
                        save_stats["cat_fruit"][3] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Yellow Catfruit Seed":
                        save_stats["cat_fruit"][4] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Purple Catfruit":
                        save_stats["cat_fruit"][5] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Red Catfruit":
                        save_stats["cat_fruit"][6] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Blue Catfruit":
                        save_stats["cat_fruit"][7] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Green Catfruit":
                        save_stats["cat_fruit"][8] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Yellow Catfruit":
                        save_stats["cat_fruit"][9] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Epic Catfruit":
                        save_stats["cat_fruit"][10] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Elder Catfruit Seed":
                        save_stats["cat_fruit"][11] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Elder Catfruit":
                        save_stats["cat_fruit"][12] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Epic Catfruit Seed":
                        save_stats["cat_fruit"][13] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Gold Catfruit":
                        save_stats["cat_fruit"][14] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Aku Catfruit Seed":
                        save_stats["cat_fruit"][15] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Aku Catfruit":
                        save_stats["cat_fruit"][16] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Gold Catfruit Seed":
                        save_stats["cat_fruit"][17] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Purple B. Stone":
                        save_stats["cat_fruit"][18] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Red B. Stone":
                        save_stats["cat_fruit"][19] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Blue B. Stone":
                        save_stats["cat_fruit"][20] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Green B. Stone":
                        save_stats["cat_fruit"][21] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Yellow B. Stone":
                        save_stats["cat_fruit"][22] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Purple B. Gem":
                        save_stats["cat_fruit"][23] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Red B. Gem":
                        save_stats["cat_fruit"][24] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Blue B. Gem":
                        save_stats["cat_fruit"][25] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Green B. Gem":
                        save_stats["cat_fruit"][26] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Yellow B. Gem":
                        save_stats["cat_fruit"][27] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Epic B. Stone":
                        save_stats["cat_fruit"][28] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    else:
                        QMessageBox.warning(self, 'Warning', 'Invalid item type',
                                        QMessageBox.Ok)
                        self.progressbar.setValue(0)
            elif selected == "Catseyes":
                amount = int(self.amountinput.text())
                item_type = self.item_menu_combobox_2.currentText()
                max = 10000
                value = amount
                if amount >= max:
                    QMessageBox.warning(self, 'Warning', 'Max value for [Cat Fruit / Behemoth Stones] is {}'.format(max-1),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
                else:
                    if item_type == "Normal":
                        save_stats["catseyes"][0] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "EX":
                        save_stats["catseyes"][1] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Rare":
                        save_stats["catseyes"][2] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Super Rare":
                        save_stats["catseyes"][3] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Uber Rare":
                        save_stats["catseyes"][4] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Legend":
                        save_stats["catseyes"][5] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    else:
                        QMessageBox.warning(self, 'Warning', 'Invalid item type',
                                        QMessageBox.Ok)
                        self.progressbar.setValue(0)
            elif selected == "Catamins":
                amount = int(self.amountinput.text())
                item_type = self.item_menu_combobox_2.currentText()
                max = 10000
                if amount >= max:
                    QMessageBox.warning(self, 'Warning', 'Max value for [Catamins] is {}'.format(max-1),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
                else:
                    value = amount
                    if item_type == "A":
                        save_stats["catamins"][0] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "B":
                        save_stats["catamins"][1] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "C":
                        save_stats["catamins"][2] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Select All":
                        save_stats["catamins"][0] = value
                        save_stats["catamins"][1] = value
                        save_stats["catamins"][2] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(selected, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    else:
                        QMessageBox.warning(self, 'Warning', 'Invalid item type',
                                        QMessageBox.Ok)
                        self.progressbar.setValue(0)

            else:
                QMessageBox.warning(self, 'Warning', 'Invalid item type',
                                        QMessageBox.Ok)
                self.progressbar.setValue(0)
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', '{}'.format(traceback.format_exc()),
                                    QMessageBox.Ok)
            self.progressbar.setValue(0)
            pass
        

        



if __name__ == "__main__":
   
        app = QApplication(sys.argv) 
        myWindow = WindowClass2() 
        myWindow.show()
        app.exec_()
