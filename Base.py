from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os
from time import sleep
import csv
import logging

__requirements__ = "selenium: 3.141.0, python: 3.8.3, chromedriver: 91.0.4472.**"
__date__, __update__ = "17.06.2021", "22.06.2021"


def logger(func):
    def wrapper(self, *argv, **kwargv):
        logging.basicConfig(filename='myapp.log',
                            level=logging.INFO,
                            format="%(asctime)s - %(name)s - %(levelname)s:\n %(message)s\n***\n")
        res = func(self, *argv, **kwargv)
        logging.info("function method: {} and actions: {}".format(func.__name__, func.__doc__))
        return func

    return wrapper


class Nseindicrawle:
    def __init__(self, url="https://www.nseindia.com/"):
        self.wait = None

        self.url = url

        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("excludeSwitches", ['enable-logging'])
        # set download dir
        self.options.add_experimental_option('prefs',
                                             {'download.default_directory': os.path.dirname(os.path.abspath(__file__))})
        # set selenium anti-bot a few options
        self.options.add_argument("start-maximized")
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(executable_path=os.path.join("chromedriver_win32", "chromedriver.exe"),
                                       options=self.options)

        self.actions = ActionChains(self.driver)

    @logger
    def start(self):
        '''\nOpen home url. \nHover Market Data. \nClick at Pre-Open Market. \n'''
        self.driver.get(self.url)
        self.wait = WebDriverWait(self.driver, 6)
        sleep(4)
        market_data = self.driver.find_element_by_css_selector("#main_navbar > ul > li:nth-child(3)")
        pre_order = self.driver.find_element_by_css_selector("#main_navbar > ul > li:nth-child(3) > div > "
                                                             "div.container > div > div:nth-child(1) > "
                                                             "ul > li:nth-child(1) > a")
        self.actions.move_to_element(market_data).pause(3).move_to_element(pre_order).pause(4).click().perform()
        sleep(6)
        # need some good tips to use WebDriverWait instead sleep(x) at string 51, 57, 94

        return self.driver.current_url

    @logger
    def parse_csv(self):
        '''\nThe act of random activity. \nWait untile table visibility. \nParse table data.
        \nSave data to file nseindia.csv \n'''
        # random action
        # if url == "https://www.nseindia.com/market-data/pre-open-market-cm-and-emerge-market":
        for i in range(350):
            self.driver.execute_script(f"window.scrollTo(0, {i})")
        self.wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR,
                                                          "#preopen-market > div > div.note_container")))

        table = WebDriverWait(self.driver, 4).until(ec.visibility_of_element_located((By.ID, "livePreTable")))
        # !!!OR WE CAN JUST DO!!! execute script: downloadPreopen(); - and get nice CSV file at one line!
        # get num of cols i.e. row data
        with open('nseindia.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            name_head = table.find_element_by_css_selector("thead > tr > th:nth-child(2)").text
            price_head = table.find_element_by_css_selector("thead > tr > th:nth-child(7)").text
            writer.writerow([name_head, price_head])
            for cols in table.find_elements_by_css_selector("tbody > tr"):
                name = cols.find_element_by_css_selector("td:nth-child(2)").text
                price = cols.find_element_by_css_selector("td:nth-child(7)").text
                writer.writerow([name, price])
                # print('name: {}   price: {}'.format(name, price))

        return self.driver.current_url

    @logger
    def base_action(self):
        '''\nUser activite log: \nOpen main url. \nScroll to table visibility. \nSelect NIFTY BANK.
        \nClick "View all". \nClose driver.\n'''
        self.driver.get(self.url)
        sleep(4)
        # target_list = [graph, bank, view_all] [css, xpath] - unit
        target_list = [["#tab4_container", '//*[@id="NIFTY 50"]/div/div/div[1]/div[2]'],
                       ["#nse-indices > div.container-fluid > div > div > nav > div > div > a:nth-child(4)",
                        '//*[@id="nse-indices"]/div[2]/div/div/nav/div/div/a[4]'],
                       ["#tab4_gainers_loosers > div.link-wrap > a",
                        '//*[@id="tab4_gainers_loosers"]/div[3]/a']]

        for target in target_list:
            for i in range(800):
                self.driver.execute_script(f"window.scrollTo(0, {i})")
            celement = self.driver.find_element_by_css_selector(target[0])
            xelement = self.driver.find_element_by_xpath(target[1])
            if celement:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", celement)
                focus = celement
            else:
                focus = xelement
            try:
                check = WebDriverWait(self.driver, 4).until(ec.element_to_be_clickable((focus)))
                if check:
                    self.actions.click(focus).perform()
            except:
                pass
            sleep(2)

        self.driver.close()


ndc = Nseindicrawle()
ndc.start()
ndc.parse_csv()
ndc.base_action()
