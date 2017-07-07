from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome('chromedriver')

INPUT_ID = "1670766294"
INPUT_PW = "PW"

INPUT_DEP = "청량리"
INPUT_DES = "가평"

YEAR = 2017
MONTH = 7
DATE = 7
HOUR_MIN = 18
HOUR_MAX = 20

#Korail Login
browser.get("http://www.letskorail.com/korail/com/login.do")

#ID : 1670766294
#LOGIN
browser.find_element_by_id("txtMember").send_keys(INPUT_ID)
browser.find_element_by_id("txtPwd").send_keys(INPUT_PW)
browser.find_element_by_xpath("//img[@alt='확인']").click()



#Korail Homepage
browser.get("http://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do")


#기차종료 - ITX
browser.find_element_by_name("selGoTrainRa").click()

#인원
browser.find_element_by_xpath("//option[@value='1']").click()


#Depart
browser.find_element_by_id("start").clear()
browser.find_element_by_id("start").send_keys(INPUT_DEP)

#Destination
browser.find_element_by_id("get").clear()
browser.find_element_by_id("get").send_keys(INPUT_DES)


#PUt year and hours
yearX = "//select[@id='s_year']/option[@value='" + str(YEAR) +"']"
monthX = "//select[@id='s_month']/option[@value='" + str(MONTH).zfill(2) +"']"
dateX ="//select[@id='s_day']/option[@value='" + str(DATE).zfill(2) + "']"
hourX = "//select[@id='s_hour']/option[@value='" + str(HOUR_MIN).zfill(2) + "']"
browser.find_element_by_xpath(yearX).click()
browser.find_element_by_xpath(monthX).click()
browser.find_element_by_xpath(dateX).click()
browser.find_element_by_xpath(hourX).click()



browser.find_element_by_xpath("//input[@title='ITX-청춘']").click()


# Find Ticket
browser.find_element_by_xpath("//a[@href='javascript:inqSchedule()']/img").click()



available = False


while not available:
    WebDriverWait(browser, 3).until(EC.presence_of_element_located(("id", "divResult")))

    reserveButtons = browser.find_elements_by_xpath("//tr[@class='']/td[6]/a/img[@alt='예약하기']")
    count = len(reserveButtons)
    print("Available : ", count)
    if count == 0:
        #다시 조회
        browser.execute_script("inqSchedule();")

    else:
        earlyTime = reserveButtons[0].find_element_by_xpath("../../../td[3]").text.encode('utf-8')
        earlyTime = str(earlyTime).split('\\n')
        earlyTime = earlyTime[1].split(':')[0]

        if int(earlyTime) < HOUR_MAX:
            print("Ticket Available : ", earlyTime)
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
    print("Alert Handle")
except TimeoutException:
    print("no alert")


try:
    wait = WebDriverWait(browser, 3).until(EC.alert_is_present())

    alert = browser.switch_to.alert
    alert.accept()
    print("Alert Handle")
except TimeoutException:
    print("no alert")
#
#
# #Press rufwpgkrl Button
# browser.find_element_by_id("btn_next").click()
