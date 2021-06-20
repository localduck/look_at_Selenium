from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from time import sleep
import random
import logging


__requirements__ = "selenium: 3.141.0, python: 3.8.3, chromedriver: 91.0.4472.**"
__date__ = "19.06.2021"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger_handler = logging.FileHandler("twetch_pool.log")
logger_handler.setLevel(logging.INFO)
logger_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s:\n %(message)s\n***\n")
logger_handler.setFormatter(logger_format)
logger.addHandler(logger_handler)
logger.info("Ready to log!")

search_container = set()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])

driver = webdriver.Chrome(executable_path=os.path.join("chromedriver_win32", "chromedriver.exe"), options=chrome_options)
driver.get("https://www.twitch.tv/")

sleep(3)

elem = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/nav/div/div[2]/div/div/div/div/div[1]/div/div/div/input')
elem.click()

for ch in "pool":
    elem.send_keys(ch)
    sleep(random.randint(1, 2))
    container = driver.find_element_by_xpath('// *[ @ id = "search-tray__container"]')
    for con in container.text.split('\n'):
        search_container.add(con)

print('search_container:\n', search_container)

elem.send_keys(Keys.RETURN)
sleep(3)

link_elements = driver.find_elements_by_xpath("//a")
for link in link_elements:
    logger.info(link.get_attribute('href'))

driver.close()
