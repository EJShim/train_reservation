from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


browser = webdriver.Chrome('chromedriver')
# 경후닠
# 카메나시1
INPUT_ID = "rudgnslz"
INPUT_PW = "zkapsktl1"

# #Melon Login
browser.get("https://member.melon.com/muid/family/ticket/login/web/login_inform.htm?cpId=MP15&returnPage=http://ticket.melon.com/main/readingGate.htm")
browser.find_element_by_id("id").send_keys(INPUT_ID)
browser.find_element_by_id("pwd").send_keys(INPUT_PW)
browser.find_element_by_id("btnLogin").click()


WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "btnLogout")))


#Rservation Page 200898
browser.get("http://ticket.melon.com/performance/index.htm?prodId=200898")





WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@class='box_btn']")))
browser.find_element_by_xpath("//div[@class='box_btn']").click()
# browser.execute_script("seatReservation('200898','PT0001');")

WebDriverWait(browser, 30).until(EC.number_of_windows_to_be(2))
handles = browser.window_handles
browser.switch_to_window(handles[1])

WebDriverWait(browser, 30).until(EC.frame_to_be_available_and_switch_to_it(("id", "oneStopFrame")))

available = False
attemp = 0
while not available:
    availableTickets = browser.find_elements_by_xpath("//*[name()='rect' and not(@fill='#dddddd') and not(@fill='none')]")

    WebDriverWait(browser, 30).until(EC.invisibility_of_element_located((By.XPATH,"//div[@class='loding_back']")))

    if len(availableTickets) < 1:
        attemp += 1
        print("no tickets available.. close window, attempt",attemp)
        browser.find_element_by_id('btnReloadSchedule').click()
        # browser.close()
        # browser.switch_to_window(handles[0])
        continue
    else:
        print("tickets available : ", len(availableTickets))
        for ticket in availableTickets:
            try:                
                ticket.click()
    
                browser.find_element_by_id('nextTicketSelection').click()
                browser.find_element_by_id('nextPayment').click()
                browser.find_element_by_id('payMethodCode009').click()
                # browser.find_element_by_xpath("//option[@value='BK20']").click()
                # browser.find_element_by_id('cashReceiptIssueCode3').click()
                browser.find_element_by_id('chkAgreeAll').click()
                browser.find_element_by_id('btnFinalPayment').click()

                available=True
                break
            except:
                WebDriverWait(browser, 3).until(EC.alert_is_present())
                alert = browser.switch_to.alert
                alert.accept()



WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "tfPhone")))
browser.find_element_by_id("tfPhone").send_keys("01049313394")
browser.find_element_by_id("tfBirthday").send_keys("890716")
browser.find_element_by_xpath("//button[@type='submit']").click()

