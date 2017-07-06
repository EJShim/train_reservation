from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome('chromedriver')


#Korail Login
browser.get("http://www.letskorail.com/korail/com/login.do")

#ID : 1670766294
#LOGIN
browser.find_element_by_id("txtMember").send_keys("1670766294")
browser.find_element_by_id("txtPwd").send_keys("password")
browser.find_element_by_xpath("//img[@alt='확인']").click()



#Korail Homepage
browser.get("http://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do")


#기차종료 - ITX
browser.find_element_by_name("selGoTrainRa").click()

#인원
browser.find_element_by_xpath("//option[@value='1']").click()


#출발지
browser.find_element_by_id("start").clear()
browser.find_element_by_id("start").send_keys("청량리")

#Destination
browser.find_element_by_id("get").clear()
browser.find_element_by_id("get").send_keys("가평")

#date
browser.find_element_by_xpath("//select[@id='s_year']/option[@value='2017']").click()
browser.find_element_by_xpath("//select[@id='s_month']/option[@value='07']").click()
browser.find_element_by_xpath("//select[@id='s_day']/option[@value='08']").click()
browser.find_element_by_xpath("//select[@id='s_hour']/option[@value='21']").click()


#Find Ticket
browser.find_element_by_xpath("//a[@href='javascript:inqSchedule()']/img").click()


#Get The First Ticket of List
try:
    wait = WebDriverWait(browser, 3).until(EC.presence_of_element_located(("xpath", "//a[@href='javascript:infochk(1,0);']")))

    browser.find_element_by_xpath("//a[@href='javascript:infochk(1,0);']/img").click()

except TimeoutException:
    print("shit")



#Handle Alert
try:
    wait = WebDriverWait(browser, 3).until(EC.alert_is_present())

    alert = browser.switch_to.alert
    alert.accept()
    print("alert1 accepted")
except TimeoutException:
    print("no alert")


try:
    wait = WebDriverWait(browser, 3).until(EC.alert_is_present())

    alert = browser.switch_to.alert
    alert.accept()
    print("alert1 accepted")
except TimeoutException:
    print("no alert")


#Press rufwpgkrl Button
browser.find_element_by_id("btn_next").click()
