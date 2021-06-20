from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
from time import sleep
import random
import csv

'''Hunting on mouse with shotgun and cannons.'''

__requirements__ = "selenium: 3.141.0, python: 3.8.3, chromedriver: 91.0.4472.**"
__date__ = "17.06.2021"

chrome_options = webdriver.ChromeOptions()
# hide grumpy bluetooth_adapter problem
chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])
# set selenium anti-bot a few options
chrome_options.add_argument("start-maximized")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(executable_path=os.path.join("chromedriver_win32", "chromedriver.exe"),
                          options=chrome_options)

driver.get("https://www.nseindia.com/")
sleep(3)

way_elem = driver.find_element_by_xpath("//a[text()='Market Data']")
aim_elem = driver.find_element_by_xpath("//a[text()='Pre-Open Market']")
logo = driver.find_element_by_xpath('/html/body/header/nav/div[1]/a')

hover = ActionChains(driver).move_to_element(way_elem)
sleep(random.randint(4, 6))
hover.move_to_element(aim_elem)
sleep(random.randint(4, 6))
hover.click(aim_elem).perform()
sleep(random.randint(2, 4))
for i in range(350):
    driver.execute_script(f"window.scrollTo(0, {i})")
sleep(2)

table = driver.find_element_by_id("livePreTable")
cols = {0: "Symbol", 1: "PREV. CLOSE", 2: "IEP  Price", 3: "Chng",
        4: "%Chng", 5: "Final Price", 6: "Final Quantity",
        7: "Value", 8: "FFM CAP", 9: "NM 52w H", 10: "NM 52w L", 11: "Today"}
with open('nseindia.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow([cols[0], cols[5]])
    for k, row in enumerate(table.find_elements_by_tag_name("tr")):
        if k > 0:
            cols = row.text.split(" ")
            writer.writerow([cols[0], cols[5]])
    f.close()

sleep(random.randint(2, 4))
driver.get("https://www.nseindia.com/")
sleep(random.randint(4, 6))

graph_up = driver.find_element_by_xpath('//*[@id="NIFTY 50"]/div/div/div[1]/div[2]')
bank = driver.find_element_by_xpath('//*[@id="nse-indices"]/div[2]/div/div/nav/div/div/a[4]')
view = driver.find_element_by_xpath('//*[@id="tab4_gainers_loosers"]/div[3]/a')
scrolling = random.randrange(bank.location['y'], graph_up.location['y'])-126
for i in range(scrolling):
    driver.execute_script(f"window.scrollTo(0, {i})")
sleep(2)

actions = ActionChains(driver)
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bank)
sleep(2)
actions.move_to_element(bank).click().perform()
sleep(2)
driver.execute_script(f"window.scrollTo(0, {scrolling})")
actions.move_to_element(view).click().perform()
sleep(2)
driver.find_element_by_tag_name('body').send_keys(Keys.END)

sleep(4)
driver.close()
