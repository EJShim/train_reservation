from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def run(INPUT_ID, INPUT_DEP, INPUT_DES, TRAIN, YEAR, MONTH, DATE, HOUR_MIN, HOUR_MAX):
    browser = webdriver.Chrome('chromedriver')

    #Korail Login
    browser.get("http://www.letskorail.com/korail/com/login.do")

    #ID : 1670766294
    #LOGIN
    browser.find_element_by_id("txtMember").send_keys(INPUT_ID)
    # browser.find_element_by_id("txtPwd").send_keys(INPUT_PW)
    # browser.find_element_by_xpath("//img[@alt='확인']").click()

    # reserveButtons = browser.find_elements_by_xpath()

    WebDriverWait(browser, 180).until(EC.presence_of_element_located(("xpath", "//img[@alt='승차권예매']")))



    #Korail Homepage
    browser.get("http://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do")


    #KTX = 1
    #ITX = 2
    radio = browser.find_elements_by_name("selGoTrainRa")
    radio[TRAIN].click()

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
    hourX = "//select[@id='s_hour']/option[@value='" + str(HOUR_MIN[0]).zfill(2) + "']"
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
            print("History")
            continue

        reserveButtons = browser.find_elements_by_xpath("//td/a/img[@alt='예약하기']")
        count = len(reserveButtons)
        print("Available : ", count)
        if count == 0:
            #다시 조회
            try: browser.execute_script("inqSchedule();")
            except Exception as e:
                WebDriverWait(browser, 3).until(EC.presence_of_element_located(("xpath", "//a[@class='btn_blue_ang']")))
                browser.execute_script("history.go(-1);")
                print("History", e)
                continue

        else:
            
            earlyTime = reserveButtons[0].find_element_by_xpath("../../../td[3]").text.encode('utf-8')
            
            earlyTime = str(earlyTime).split('\\n')
            earlyMin = earlyTime[1].split(':')[1]
            earlyMin = earlyMin[:2]
            earlyTime = earlyTime[1].split(':')[0]        

            if int(earlyTime) < HOUR_MAX[0]:
                print("Ticket Available : ", earlyTime, earlyMin)
                # reserveButtons[0].click()
                script = str(reserveButtons[0].find_element_by_xpath("..").get_attribute("href")).split(':')[1]
                browser.execute_script(script)

                available = True
            elif int(earlyTime) == HOUR_MAX[0] and int(earlyMin) < HOUR_MAX[1]:
                print("Ticket Available : ", earlyTime, earlyMin)
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


if __name__ == "__main__":
    INPUT_ID = "1670766294"    

    INPUT_DEP = "서울"
    INPUT_DES = "전주"

    YEAR = 2018
    MONTH = 2
    DATE = 14
    HOUR_MIN = [14, 00]
    HOUR_MAX = [17, 00]

    run(INPUT_ID, INPUT_DEP, INPUT_DES, YEAR, MONTH, DATE, HOUR_MIN, HOUR_MAX)

