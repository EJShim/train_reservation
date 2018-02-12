from train import run
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
 
class Dialog(QDialog):    


    def __init__(self):
        super(Dialog, self).__init__()
        






        self.locations = ['서울', '가평', '전주']
        self.createFormGroupBox()
 
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        # buttonBox.rejected.connect(self.reject)
 
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
 
        self.setWindowTitle("KORAIL AUTO")

        
 
    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("input values")
        layout = QFormLayout()

        #ID
        layout.addRow(QLabel("koreail ID "), QLineEdit())

        #Departure
        self.dep = QComboBox()

        for loc in self.locations:            
            self.dep.addItem(loc)
        # self.dep.currentIndexChanged.connect( self.onChangeIndex )
        layout.addRow(QLabel("출발"), self.dep)

        #Destination
        self.des = QComboBox()
        for loc in self.locations:            
            self.des.addItem(loc)
        layout.addRow(QLabel("도착"), self.des)

        #Date
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        layout.addRow(QLabel("날짜"), cal)

        
        layout.addRow(QLabel("시간 "), QSpinBox())
        
        self.formGroupBox.setLayout(layout)

    def accept(self):
        return
        INPUT_ID = "1670766294"    

        INPUT_DEP = "서울"
        INPUT_DES = "전주"

        YEAR = 2018
        MONTH = 2
        DATE = 14
        HOUR_MIN = [14, 00]
        HOUR_MAX = [17, 00]

        run(INPUT_ID, INPUT_DEP, INPUT_DES, YEAR, MONTH, DATE, HOUR_MIN, HOUR_MAX)
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
    