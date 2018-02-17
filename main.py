from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from style import styleData
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import json
import datetime


class thread_reservation(QThread):
    onprogress = pyqtSignal(str)

    def __init__(self,  INPUT_ID, INPUT_DEP, INPUT_DES, TRAIN, YEAR, MONTH, DAY, HOUR_MIN, HOUR_MAX, parent=None):
        super().__init__()

        self.INPUT_ID = INPUT_ID
        self.INPUT_DEP = INPUT_DEP
        self.INPUT_DES = INPUT_DES
        self.TRAIN = TRAIN
        self.YEAR = YEAR
        self.MONTH = MONTH
        self.DAY = DAY
        self.HOUR_MIN = HOUR_MIN
        self.HOUR_MAX = HOUR_MAX

        self.attempt = 0

    def log(self, *txt):
        log = ''
        for word in txt:
            log += " " + str(word)
        self.onprogress.emit(log)

    def run(self):        
        browser = webdriver.Chrome('chromedriver')
        #Korail Login
        browser.get("http://www.letskorail.com/korail/com/login.do")

        #LOGIN
        browser.find_element_by_id("txtMember").send_keys(self.INPUT_ID)
        self.log("크롬에서 코레일 로그인을 하고 기다리세여!")
        # browser.find_element_by_id("txtPwd").send_keys(INPUT_PW)
        # browser.find_element_by_xpath("//img[@alt='확인']").click()
        # reserveButtons = browser.find_elements_by_xpath()
        WebDriverWait(browser, 180).until(EC.presence_of_element_located(("xpath", "//img[@alt='승차권예매']")))
        #Korail Homepage
        browser.get("http://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do")

        #TRAIN
        radio = browser.find_elements_by_name("selGoTrainRa")
        radio[self.TRAIN].click()

        #인원
        browser.find_element_by_xpath("//option[@value='1']").click()

        #Depart
        browser.find_element_by_id("start").clear()
        browser.find_element_by_id("start").send_keys(self.INPUT_DEP)

        #Destination
        browser.find_element_by_id("get").clear()
        browser.find_element_by_id("get").send_keys(self.INPUT_DES)

        #PUt year and hours
        yearX = "//select[@id='s_year']/option[@value='" + str(self.YEAR) +"']"
        monthX = "//select[@id='s_month']/option[@value='" + str(self.MONTH).zfill(2) +"']"
        dateX ="//select[@id='s_day']/option[@value='" + str(self.DAY).zfill(2) + "']"
        hourX = "//select[@id='s_hour']/option[@value='" + str(self.HOUR_MIN[0]).zfill(2) + "']"
        browser.find_element_by_xpath(yearX).click()
        browser.find_element_by_xpath(monthX).click()
        browser.find_element_by_xpath(dateX).click()
        browser.find_element_by_xpath(hourX).click()

        # Find Ticket
        # browser.find_element_by_xpath("//a[@href='javascript:inqSchedule()']/img").click()
        browser.execute_script("inqSchedule();")

        available = False

        while not available:
            try:
                WebDriverWait(browser, 3).until(EC.presence_of_element_located(("id", "divResult")))
            except TimeoutException:
                WebDriverWait(browser, 3).until(EC.presence_of_element_located(("xpath", "//a[@class='btn_blue_ang']")))
                browser.execute_script("history.go(-1);")
                self.log("뒤로가기")
                continue

            reserveButtons = browser.find_elements_by_xpath("//td/a/img[@alt='예약하기']")
            count = len(reserveButtons)
            self.attempt += 1

            
            self.log("attempt ", self.attempt, ", total available tickets : ", count)
            if count == 0:
                #다시 조회
                try: browser.execute_script("inqSchedule();")
                except Exception as e:
                    WebDriverWait(browser, 3).until(EC.presence_of_element_located(("xpath", "//a[@class='btn_blue_ang']")))
                    browser.execute_script("history.go(-1);")
                    self.log("History", e)
                    continue

            else:
                
                earlyTime = reserveButtons[0].find_element_by_xpath("../../../td[3]").text.encode('utf-8')
                
                earlyTime = str(earlyTime).split('\\n')
                earlyMin = earlyTime[1].split(':')[1]
                earlyMin = earlyMin[:2]
                earlyTime = earlyTime[1].split(':')[0]        

                if int(earlyTime) < self.HOUR_MAX[0]:
                    self.log("Ticket Available : ", earlyTime, earlyMin)
                    # reserveButtons[0].click()
                    script = str(reserveButtons[0].find_element_by_xpath("..").get_attribute("href")).split(':')[1]
                    browser.execute_script(script)

                    available = True
                elif int(earlyTime) == self.HOUR_MAX[0] and int(earlyMin) < self.HOUR_MAX[1]:
                    self.log("Ticket Available : ", earlyTime, earlyMin)
                    # reserveButtons[0].click()
                    script = str(reserveButtons[0].find_element_by_xpath("..").get_attribute("href")).split(':')[1]
                    browser.execute_script(script)

                    available = True
                else:
                    browser.execute_script("inqSchedule();")

        #Handle Alert
        try:
            wait = WebDriverWait(browser, 3).until(EC.alert_is_present())
            alert = browser.switch_to.alert
            alert.accept()
            self.log("Alert Handle")
        except TimeoutException:
            self.log("no alert")

        try:
            wait = WebDriverWait(browser, 3).until(EC.alert_is_present())
            alert = browser.switch_to.alert
            alert.accept()
            self.log("Alert Handle")
        except TimeoutException:
            self.log("no alert")

        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located(("xpath", "//a[@class='btn_blue_ang']")))
            browser.execute_script("f_close();")
        except TimeoutException:
            self.log("asdfasdf")
            
        

class Dialog(QDialog):    
    def __init__(self):
        super(Dialog, self).__init__()
        
        try:
            with open('tmp_data', 'r') as data:
                self.data = json.load(data)
        except:
            self.data = {
                'id': '',
                'departure':0,
                'destination':1,
                'train':1
            }

        self.locations = ['서울', '청량리', '가평', '전주', '광명', '익산']
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
        self.formGroupBox = QGroupBox()
        layout = QFormLayout()

        #ID
        self.id = QLineEdit()        
        self.id.setMaxLength(10)
        self.id.setText(self.data['id'])
        layout.addRow(QLabel("koreail ID "), self.id)

        #Departure
        self.dep = QComboBox()
        for loc in self.locations:            
            self.dep.addItem(loc)
        self.dep.setCurrentIndex(self.data['departure'])

        #Destination
        self.des = QComboBox()
        for loc in self.locations:            
            self.des.addItem(loc)
        self.des.setCurrentIndex(self.data['destination'])
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
        self.train.setCurrentIndex(self.data['train'])
        layout.addRow("기차", self.train)

        #Date
        self.date = QCalendarWidget(self)
        self.date.setGridVisible(True)
        layout.addRow(QLabel("날짜"), self.date)


        layout.addRow(QLabel("시간은 00시부터 24시까지로 적어야함! 2시라고 적으면 새벽두시다! 14시로 적어라!"))

        time_layout = QHBoxLayout()
        now = datetime.datetime.now()        
        self.hour_min = QSpinBox()        
        self.hour_min.setRange(0, 23)
        self.hour_min.setValue(now.hour)

        self.hour_max = QSpinBox()
        self.hour_max.setRange(0, 23)
        self.hour_max.setValue(self.hour_min.value()+1)
        self.min_max = QSpinBox()
        self.min_max.setRange(0, 59)

        time_layout.addWidget(self.hour_min)
        time_layout.addWidget(QLabel("시 부터"))
        time_layout.addWidget(self.hour_max)
        time_layout.addWidget(self.min_max)
        time_layout.addWidget(QLabel("분 까지"))
        
        layout.addRow(time_layout)


        self.message_log = QTextEdit()
        self.message_log.setEnabled(False)
        layout.addRow(self.message_log)
        
        self.formGroupBox.setLayout(layout)

    def accept(self):

        INPUT_ID = self.id.text()
        if len(INPUT_ID) < 10:
            self.warn("아이디 똑바로 쳐라! 열 자리다!")
            return
        self.data['id'] = INPUT_ID

        INPUT_DEP = self.dep.currentText()
        INPUT_DES = self.des.currentText()

        self.data['departure'] = self.dep.currentIndex()
        self.data['destination'] = self.des.currentIndex()

        if INPUT_DEP == INPUT_DES:
            message = "출발지와 도착지가 다 " +  INPUT_DEP + "(이)잖아! 다르게 설정해라!"
            self.warn(message)
            return

            
        TRAIN =  self.train.currentIndex()
        self.data['train'] = TRAIN

        DATE = self.date.selectedDate()
        YEAR = DATE.year()
        MONTH = DATE.month()
        DAY = DATE.day()

        HOUR_MIN = [int(self.hour_min.text()), 0]
        HOUR_MAX = [int(self.hour_max.text()), int(self.min_max.text())]

        if HOUR_MAX < HOUR_MIN:
            self.warn("시간 설정 제대로 하셈")  
            return
    
        with open('tmp_data', 'w') as outfile:
            json.dump(self.data, outfile)
        
        # self.run(INPUT_ID, INPUT_DEP, INPUT_DES, TRAIN, YEAR, MONTH, DAY, HOUR_MIN, HOUR_MAX)
        self.reservation_agent = thread_reservation(INPUT_ID, INPUT_DEP, INPUT_DES, TRAIN, YEAR, MONTH, DAY, HOUR_MIN, HOUR_MAX, self)
        self.reservation_agent.onprogress.connect(self.log)
        self.reservation_agent.start()
        return

    def log(self, *txt):
        log = '\n'
        for word in txt:
            log += " " + str(word)
        self.message_log.insertPlainText(log)
        self.message_log.verticalScrollBar().setValue(self.message_log.verticalScrollBar().maximum())
        
        cursor = self.message_log.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.select(QTextCursor.LineUnderCursor)
        cursor.removeSelectedText()


    def warn(self, txt):
        alert = QWidget()
        QMessageBox.warning(alert, "alert", txt)
        alert.show()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(styleData)
    dialog = Dialog()
    sys.exit(dialog.exec_())