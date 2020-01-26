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
from datetime import datetime as dt
import pdb
from db_connect import get_list_of_urls

def prepare_driver():
    '''Returns a Firefox Webdriver.'''
    options = Options()
    # options.add_argument('-headless')
    driver = Firefox(executable_path='geckodriver', options=options)

    return driver

def open_pages_one_by_one(driver, urls):
    list_of_dicts = []
    try:
        for url in urls:
            bestbuy_dict = {}
            bestbuy_dict["product_url"] = str(url)
            print(str(url))
            driver.get(url)
            wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'input.search-input')))
            try:
                bestbuy_dict['date'] = dt.today()
                bestbuy_dict['date_str'] = bestbuy_dict['date'].strftime('%Y-%m-%d')

                try:
                    bestbuy_dict["product_name"] = driver.find_element_by_xpath("//*[@id='shop-product-title-ad81b09a-d15e-4a55-994b-ad7f98b9da11']/div/div/div[1]/h1").text
                except:
                    bestbuy_dict["product_name"] = "Not available"


            except Exception as e1:
                print("Could not gather-> ",str(e1))
            finally:
                if bestbuy_dict:
                    print(bestbuy_dict)
                    list_of_dicts.append(bestbuy_dict)
    except Exception as e:
        print(e)
    finally:
        if driver:
            driver.quit()


if __name__ == '__main__':

    try:
        urls = get_list_of_urls("bestbuy")
        driver = prepare_driver()
        open_pages_one_by_one(driver, urls)
    finally:
        pass
