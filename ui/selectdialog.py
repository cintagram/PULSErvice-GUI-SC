#임포트랑 다른것들 알아서 넣으세요
#Coded by CintagramABP in PULSErvice.
#You can use freely, but dont sell this ;-;
#BCSFEGUI

class DynamicInputDialog(QDialog):
    def __init__(self):
        super(DynamicInputDialog, self).__init__() #클래스명 일치해야해요
        self.setWindowTitle("항목을 오른쪽으로 이동해주세요.")
        self.window_width, self.window_height = 120, 80
        self.setMinimumSize(self.window_width, self.window_height)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.retrunVal = None
        self.initUI()
        self.listWidgetLeft.addItem('아이템1')
        self.listWidgetLeft.addItem('아이템2')
        #아이템 추가 가능합니다
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
            self.buttons['적용'] = QPushButton('&적용')

            for k in self.buttons:
                self.buttons[k].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)

            """
            첫번째 칸
            """
            self.listWidgetLeft = QListWidget()
            subLayouts['LeftColumn'].addWidget(self.listWidgetLeft, 1, 0, 4, 4)

            subLayouts['LeftColumn'].setRowStretch(4, 1)
            subLayouts['LeftColumn'].addWidget(self.buttons['>>'], 1, 4, 1, 1, alignment=Qt.AlignTop)
            subLayouts['LeftColumn'].addWidget(self.buttons['<'], 2, 4, 1, 1, alignment=Qt.AlignTop)
            subLayouts['LeftColumn'].addWidget(self.buttons['>'], 3, 4, 1, 1, alignment=Qt.AlignTop)
            subLayouts['LeftColumn'].addWidget(self.buttons['<<'], 4, 4, 1, 1, alignment=Qt.AlignTop)


            """
            두번째 칸
            """
            self.listWidgetRight = QListWidget()

            hLayout = QHBoxLayout()
            subLayouts['RightColumn'].addLayout(hLayout)

            hLayout.addWidget(self.listWidgetRight, 4)

            vLayout = QVBoxLayout()
            hLayout.addLayout(vLayout, 1)

            vLayout.addWidget(self.buttons['적용'])
            vLayout.addStretch(1)

    def setButtonConnections(self):
        self.listWidgetLeft.itemSelectionChanged.connect(self.updateButtonStatus)
        self.listWidgetRight.itemSelectionChanged.connect(self.updateButtonStatus)

        self.buttons['>'].clicked.connect(self.buttonAddClicked)
        self.buttons['<'].clicked.connect(self.buttonRemoveClicked)
        self.buttons['>>'].clicked.connect(self.buttonAddAllClicked)
        self.buttons['<<'].clicked.connect(self.buttonRemoveAllClicked)
        self.buttons['적용'].clicked.connect(self.buttonapplyClicked)

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
        self.w = FutureTimeInputDialog()
        self.w.show()
        return self.retrunVal

    def updateButtonStatus(self):
        self.buttons['>'].setDisabled(not bool(self.listWidgetLeft.selectedItems()) or self.listWidgetLeft.count() == 0)
        self.buttons['<'].setDisabled(not bool(self.listWidgetRight.selectedItems()) or self.listWidgetRight.count() == 0)

    def exec_(self):
        super(DynamicInputDialog, self).exec_() #클래스명 일치해야해요
        self.buttons['적용'].clicked.connect(self.buttonapplyClicked) #이게 선택 끝내는 버튼
        return self.retrunVal

if __name__ == "__main__":
    dialog = DynamicInputDialog()
    execute = dialog.exec_()
    if execute: #값 유무 확인
        print("Items: {}".format(execute)) #리스트형태로 저장
        listlength = len(execute) # 리스트 갯수저장
        print("List Length: {}".format(listlength))
        i = 0
        for i in range(listlength): #항목 확인
            if "아이템1" == str(execute[i]):
                print("아이템1")
            elif "아이템2" == str(execute[i]):
                print("아이템2")
                #여러거지로 활용가능

