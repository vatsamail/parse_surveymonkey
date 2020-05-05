from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint

import os
import time


class Survey():
    debug = 0

    def __init__(self, url, user, passwd, debug=0):
        self.debug = debug
        self._setup()
        self.login(url, user, passwd)




    def _setup(self):
        chrome_options = Options()
        if not self.debug:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

        if os.name == 'nt':
            # for windows Chrome
            self.browser = webdriver.Chrome(os.path.join('', 'chromedriver.exe'), chrome_options=chrome_options)
        else:
            # for non-windows (aka Ubuntu-Linux) use headless gecko
            self.browser = webdriver.Chrome(chrome_options=chrome_options)

    def login(self, url, user, passwd):
        self.browser.get(url)
        self.browser.find_element_by_id("username").send_keys(user)
        self.browser.find_element_by_id("password").send_keys(passwd)
        self.browser.find_element_by_class_name("wds-button--arrow-right").submit()
        # <button class="wds-button wds-button--stretch wds-button--icon-right wds-button--arrow-right" type="submit">LOG IN<span></span></button>


    def get_report(self,respondent):
        filename = os.path.join(os.getcwd(), 'output', 'response-'+str(respondent)+'.txt')
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='btn-menu sm-respondent-nav-buttons sm-float-l']//a[@title='Previous respondent ( j )']")))
        page = self.browser.find_element_by_class_name("response-question-list")
        li_objs = self.browser.find_elements_by_tag_name('span')
        wr = open(filename, 'w')
        for o in li_objs:
            wr.write(o.text+"\n")
        wr.close()

        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='btn-menu sm-respondent-nav-buttons sm-float-l']//a[@title='Previous respondent ( j )']"))).click()
        self.easy()


    def easy(self):
        sleep_time = self.debug * 5
        time.sleep(sleep_time)


##########################################
url     = '***********'
user    = '***********'
passwd  = '***********'
##########################################

s = Survey(url, user, passwd, 1)
ranger = 100

for i in range(ranger, 0, -1):
    print("Surveying",i,"report")
    s.get_report(i)
