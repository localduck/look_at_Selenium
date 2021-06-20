from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import os
import re
import logging


__requirements__ = "selenium: 3.141.0, python: 3.8.3, chromedriver: 91.0.4472.**"
__date__ = "18.06.2021"


class Stalker:
    def __init__(self, url="https://twitter.com/elonmusk"):
        self.body = None
        self.wait = None
        self.xtw = '//*[@id="react-root"]/div/div/div[2]/main/' \
                   'div/div/div/div[1]/div/div[2]/div/div/div[2]/' \
                   'section/div/div'
        self.url = url

        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("excludeSwitches", ['enable-logging'])
        self.driver = webdriver.Chrome(executable_path=os.path.join("chromedriver_win32", "chromedriver.exe"),
                                       options=self.options)

        self.tweet_list = set()

        # shuld to use group...
        # self.token_name = re.compile('Elon Musk, the 2nd;@elonmusk;·;\w+\s\w+\\.;')
        # self.token_likes = re.compile(
        #     ';\d+(?:,\d+)*(?![.,]?\d)\s\w+\\.;\d+(?:,\d+)*(?![.,]?\d)\s\w+\\.;\d+(?:,\d+)*(?![.,]?\d)\s\w+\\.')

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        logger_handler = logging.FileHandler("IlonMask_tweet.log")
        logger_handler.setLevel(logging.INFO)
        logger_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s:\n %(message)s\n***\n")
        logger_handler.setFormatter(logger_format)
        self.logger.addHandler(logger_handler)
        self.logger.info("Ready to log!")

    def chase(self):
        self.driver.get(self.url)
        self.body = self.driver.find_element_by_tag_name("body")
        self.wait = WebDriverWait(self.driver, 3)

        if len(self.tweet_list) < 20:
            self.grab_tweet()

    def grab_tweet(self):
        while len(self.tweet_list) < 20:
            # or we can use execute script: window.scrollTo(0, document.body.scrollHeight);
            try:
                self.wait.until(ec.visibility_of_element_located(
                    (By.XPATH, "//span[contains(@class, 'Ilon, im watch at u!')]")))
                break
            except:
                self.body.send_keys(Keys.PAGE_DOWN)
                self.tweet_log()

    def tweet_log(self):
        tweets = self.driver.find_elements_by_xpath(self.xtw)
        name = re.compile('Elon Musk, the 2nd[\n]@elonmusk[\n]·[\n]\\w+\\s\\w+\\.[\n]')
        likes = re.compile('\\d+(?:,\\d+)*(?![.,]?\\d)\\s\\w+\\.[\n]'*3)
        for tweet in tweets:
            mtext = re.sub(name, 'ZZZ', tweet.text)
            mtext = re.sub(likes, 'XXXX', mtext)

            # a little bit problem with: re.search('zzz(.*)xxxx', mtext).group(1) - so... :(
            sub_str = []
            end_str = [m.start() for m in re.finditer('XXXX', mtext)]
            for i in [m.end() for m in re.finditer('ZZZ', mtext)]:
                if i < min(end_str):
                    sub_str.append((i, min(end_str)))
                    if len(end_str) > 1:
                        end_str.remove(min(end_str))
                else:
                    if len(end_str) > 1:
                        end_str.remove(min(end_str))
                        sub_str.append((i, min(end_str)))
            for i in sub_str:
                if mtext[i[0]:i[1]] not in self.tweet_list:
                    self.logger.info(mtext[i[0]:i[1]])
                self.tweet_list.add(mtext[i[0]:i[1]])
                if len(self.tweet_list) == 20:
                    print(self.tweet_list)
                    break

    # ...and hell
    # def tweet_log(self):
    #     tweets = self.driver.find_elements_by_xpath(self.xtw)
    #     for tweet in tweets:
    #         t = tweet.text.replace('\n', ';')
    #         for name in re.findall(self.token_name, t):
    #             t = t.replace(name, '\n')
    #         for likes in re.findall(self.token_likes, t):
    #             t = t.replace(likes, '')
    #         if 'Показать эту ветку' in t:
    #             t = t.replace('Показать эту ветку', '')
    #         if ';Elon Musk, the 2nd ретвитнул(а)' in t:
    #             t = t.replace(';Elon Musk, the 2nd ретвитнул(а)', '\nElon Musk, the 2nd ретвитнул(а)')
    #             t = t.replace('\n\n', '\n')
    #         t = t.replace(';', '').split('\n')
    #         for txt in t:
    #             if 'Elon Musk, the 2nd ретвитнул(а)' not in txt:
    #                 if txt not in self.tweet_list:
    #                     self.logger.info(txt)
    #                 self.tweet_list.add(txt)
    #             if len(self.tweet_list) == 20:
    #                 break


observer = Stalker()
observer.chase()
