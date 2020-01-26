import selenium
import json
import time
import re
import string
import requests
import bs4
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import csv
import pdb

domain = 'https://www.olx.in/'

def prepare_driver():
    '''Returns a Firefox Webdriver.'''
    options = Options()
    # options.add_argument('-headless')
    driver = Firefox(executable_path='geckodriver', options=options)

    return driver

def connect_to_db():
    import mysql.connector
    from mysql.connector import Error

    try:
        urls = []
        connection = mysql.connector.connect(host='localhost',
                                         database='olx',
                                         user='root',
                                         password='password')

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select car_id, user from olx.car_details where phone = 'NA';")
            for record in cursor:
                urls.append("https://www.olx.in/nf/chat/new/"+str(record[0])+"/"+str(record[1]))

    except Error as e:
        print("Error while connecting to MySQL", e)
        urls = []
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        return urls

def visit_page(driver, page_url):
    try:
        driver.get(page_url)

        page_not_available = WebDriverWait(driver, 10).until_not(
            EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/main/div/section/div/div/div[4]/span[1]')))

        # chat_button = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/main/div/div/div[5]/div[2]/div/div/button')))
        # if chat_button:
        #     chat_button.click()
        #     continue_chat_popup(driver)
        msg_textarea = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/main/div/div/div[2]/div/div[5]/textarea')))
        # driver.implicitly_wait(5)
        if msg_textarea:
            print("located textarea for msg")
            msg_textarea.click()
            msg_textarea.send_keys("Hi, I am interested, please send your contact number..")
            msg_textarea.send_keys(Keys.ENTER)
            # msg_send = driver.find_element_by_xpath('//*[@id="myDiv"]/div[2]/div/div[4]/span')
            # msg_send.click()
            return True
        else:
            print("could not locate msg textarea")
        # else:
        #     return False

    except Exception as e:
        print("Exception in visit_page() method -> "+str(e))
        return False

def login_popup_handler(driver):
    try:
        #popup_cross = driver.find_element_by_xpath("//*[@id='ad_campain_modal']/div/div/div/button/i").click()
        login_with_email = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/button[3]/span').click()
        email = driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div/div[2]/div/div[1]/div/div/input')
        email.send_keys("ezeia.ds11@gmail.com")
        next = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/form/div/button/span')))
        next.click()
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        password_field.click()
        password_field.send_keys("Ezeia@123")
        login_btn = driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div/button/span')
        login_btn.click()
        driver.implicitly_wait(10)
        print("clicked on login after entering email and password")

        #driver.switch_to_window(driver.window_handles[0])
    except Exception as e:
        print("Exception in login method()", str(e))

def continue_chat_popup(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/main/div/div/div[6]/div[2]/div[2]/button')))
    driver.find_element_by_xpath('//*[@id="container"]/main/div/div/div[6]/div[2]/div[2]/button').click()

if __name__ == '__main__':
    driver = None
    try:
        
        url_list = connect_to_db()
        if url_list:
            driver = prepare_driver()
            driver.get(domain)
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='container']/header/div/div/div[3]/button")))
            element.click()
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/button[3]/span')))
            login_popup_handler(driver)
            logged_in = WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.XPATH,
                            '/html/body/div[2]/div/div/form/div/button/span')))
            print("logged in")

            for url in url_list:
                driver.implicitly_wait(5)
                ls = []
                print(url)
                x = visit_page(driver, url)
                if x:
                    url = [url, "Msg sent"]
                    print(url)
                else:
                    url = [url, "Failed sending msg"]
        else:
            print("No urls fetched from olx database that seem to have NA in phone...")

    except Exception as e:
        print("Exception occurred->"+str(e))
    finally:
        if driver:
            driver.quit()

