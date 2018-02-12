from train import run
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
 
class Dialog(QDialog):    


    def __init__(self):
        super(Dialog, self).__init__()
        

        self.locations = ['서울', '가평', '전주']
        self.trains = ['전체', 'KTX', 'ITX']
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
        self.id = QLineEdit()
        self.id.setMaxLength(10)
        layout.addRow(QLabel("koreail ID "), self.id)

        #Departure
        self.dep = QComboBox()
        for loc in self.locations:            
            self.dep.addItem(loc)

        #Destination
        self.des = QComboBox()
        for loc in self.locations:            
            self.des.addItem(loc)        
        dest_layout = QHBoxLayout()
        dest_layout.addWidget(QLabel("출발"))
        dest_layout.addWidget(self.dep)
        dest_layout.addWidget(QLabel("도착"))
        dest_layout.addWidget(self.des)
        layout.addRow(dest_layout)


        self.train = QComboBox()
        train_layout = QHBoxLayout()
        for tr in self.trains:
            self.train.addItem(tr)        
        layout.addRow("기차", self.train)




        #Date
        self.date = QCalendarWidget(self)
        self.date.setGridVisible(True)
        layout.addRow(QLabel("날짜"), self.date)


        layout.addRow(QLabel("시간은 00시부터 24시까지로 적어야함! 2시라고 적으면 새벽두시다! 14시로 적어라!"))

        time_layout = QHBoxLayout()

        self.hour_min = QSpinBox()        
        self.hour_min.setRange(0, 23)
        self.hour_max = QSpinBox()
        self.hour_max.setRange(0, 23)
        self.min_max = QSpinBox()
        self.min_max.setRange(0, 59)

        time_layout.addWidget(self.hour_min)
        time_layout.addWidget(QLabel("시 부터"))
        time_layout.addWidget(self.hour_max)
        time_layout.addWidget(self.min_max)
        time_layout.addWidget(QLabel("분 까지"))
        
        layout.addRow(time_layout)
        
        self.formGroupBox.setLayout(layout)

    def accept(self):

        INPUT_ID = self.id.text()
        if len(INPUT_ID) < 10:
            self.warn("아이디 똑바로 쳐라! 열 자리다!")
            return

        INPUT_DEP = self.dep.currentText()
        INPUT_DES = self.des.currentText()

        if INPUT_DEP == INPUT_DES:
            message = "출발지와 도착지가 다 " +  INPUT_DEP + "(이)잖아! 다르게 설정해라!"
            self.warn(message)
            return

            
        TRAIN =  self.train.currentIndex()        
        DATE = self.date.selectedDate()
        YEAR = DATE.year()
        MONTH = DATE.month()
        DAY = DATE.day()

        HOUR_MIN = [int(self.hour_min.text()), 0]
        HOUR_MAX = [int(self.hour_max.text()), int(self.min_max.text())]        
        
        run(INPUT_ID, INPUT_DEP, INPUT_DES, TRAIN, YEAR, MONTH, DAY, HOUR_MIN, HOUR_MAX)
        return

    def warn(self, txt):
        alert = QWidget()
        QMessageBox.warning(alert, "alert", txt)
        alert.show()
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
    