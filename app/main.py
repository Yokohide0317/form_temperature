# -*- coding: utf-8 -*-
#import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import random
import argparse
import json
import io
import sys
import os
import pyotp

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class sel_main:
    def __init__(self, wait_time, no_facta):
        self.url = os.environ['URL'] #j["url"]
        self.email = os.environ['EMAIL'] #j["email"]
        self.password = os.environ['PASSWORD'] #j["password"]
        self.key = os.environ['AUTH_KEY'] #j["auth_key"]
        self.wait = int(wait_time)
        self.no_facta = no_facta
        print("Login as : ", self.email)


    # https://tanuhack.com/selenium-2step-authentication/
    # 二段階認証突破
    def get_two_facta(self):
        self.two_auth_pass = pyotp.TOTP(self.key).now()

    def login_365(self, driver):
        # Input email
        element = driver.find_element(By.ID, "i0116")
        element.send_keys(self.email)
        time.sleep(self.wait)
        # click "Next"
        element = driver.find_element(By.ID, "idSIButton9")
        element.click()
        time.sleep(self.wait)

        # Input Password
        element = driver.find_element(By.ID, "i0118")
        element.send_keys(self.password)
        time.sleep(self.wait)

        # click "Next"
        element = driver.find_element(By.ID, "idSIButton9")
        element.click()
        time.sleep(self.wait)
       
        # 2Facta認証
        if not self.no_facta:
            # click "mobile auth"
            element = driver.find_element(By.CLASS_NAME, "table")
            element.click()
            time.sleep(self.wait)

            # Get and Enter 2facta
            self.get_two_facta()
            element = driver.find_element(By.XPATH, '//*[@id="idTxtBx_SAOTCC_OTC"]')
            element.send_keys(self.two_auth_pass)
            time.sleep(self.wait*2)

            # Click Enter
            element = driver.find_element(By.XPATH, '//*[@id="idSubmit_SAOTCC_Continue"]')
            element.click()
            time.sleep(self.wait+2)

        # Stay signin -> No
        element = driver.find_element(By.ID, "idBtn_Back")
        element.click()
        time.sleep(self.wait+2)

    def get_random_temp(self):
        self.r_t = random.randrange(16, 18)

    def input_temp(self, driver, debug):
        # 36.5 ~ 36.7でランダム
        self.get_random_temp()
        x_path = '//*[@id="SelectId_0_placeholder"]'
        element = driver.find_element(By.XPATH, x_path)
        element.click()
        
        time.sleep(int(self.wait/2))

        x_path = '//*[@id="SelectId_0"]/div[2]/div[%s]' % (int(self.r_t))
        element = driver.find_element(By.XPATH, x_path)
        element.click()

        time.sleep(int(self.wait/2))

        """
        # メール送信のチェック
        #xpath = '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[6]/div/div[2]/div/div[1]/div/label/input' # はい
        x_path = '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[6]/div/div[2]/div/div[2]/div/label/input' # いいえ
        element = driver.find_element(By.XPATH, x_path)
        element.click()
        time.sleep(self.wait)
        """

        # submit
        if debug == False:
            x_path = '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/button'
            element = driver.find_element(By.XPATH, x_path)
            element.click()

        time.sleep(int(self.wait*2))


    def open_url(self, debug, cui):
        #Chromeを操作
        if cui:
            options = Options()
            options.add_argument('--headless')
            driver = webdriver.Remote(
                    command_executor=os.environ["SELENIUM_URL"],
                    options=options,
                    desired_capabilities=DesiredCapabilities.FIREFOX.copy()
            ) 
            driver.set_window_size('1200', '1000')
        else:
            driver = webdriver.Remote(
                    command_executor=os.environ["SELENIUM_URL"],
                    options=Options()
            )
            driver.implicitly_wait(2)

        driver.get(self.url)
        driver.implicitly_wait(2)

        time.sleep(int(self.wait*3))
        cur_url = driver.current_url
        if cur_url != self.url:
            print("認証画面に移行しました. ２段階認証も行います.")
            self.login_365(driver)

        print("アクセス完了")

        if debug:
            print("Debugモード。送信しません。")
        # input_temp
        self.input_temp(driver, debug)
        driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='自動で健康行動観察表を提出。')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument("-w", "--wait", default=3)
    parser.add_argument("--cui", action="store_true")
    parser.add_argument("--no_facta", action="store_true")
    args = parser.parse_args()

    sel = sel_main(args.wait, args.no_facta)
    sel.open_url(args.debug, args.cui)
