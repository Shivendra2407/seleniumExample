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

domain =  'https://droom.in/obv'

def prepare_driver():
    '''Returns a Firefox Webdriver.'''
    options = Options()
    # options.add_argument('-headless')
    driver = Firefox(executable_path='geckodriver', options=options)

    return driver

def fill_form(driver, search_argument):
    '''Finds all the input tags in form and makes a POST requests.'''
    category_field = driver.find_element_by_id('category')
    category_select = Select(category_field)
    category_select.select_by_value('1')

    make_field = driver.find_element_by_id('make')
    make_select = Select(make_field)
    make_select.select_by_value(search_argument[0])

    model_field = driver.find_element_by_id('model')
    model_select = Select(model_field)
    model_select.select_by_value(search_argument[1])

    year_field = driver.find_element_by_id('year')
    year_select = Select(year_field)
    year_select.select_by_value(search_argument[2])

    trim_field = driver.find_element_by_id('trim')
    trim_select = Select(trim_field)
    trim_select.select_by_value(search_argument[3])

    kms_field = driver.find_element_by_id('kms_driven')
    kms_field.send_keys(search_argument[4])
    driver.implicitly_wait(5)

    driver.find_element_by_class_name('obv_adobe_landing_submit')\
        .click()
    wait = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'adobe_obv_result_buy_droom')))

def scrape_results(driver):
    '''Returns the data from n_results amount of results.'''
    price_data = {'Good':'','Fair':'','V Good':'','Excellent':''}
    for key in price_data:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, key))).click()
        range_from = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[2]/div/div[1]/div[1]/div/div/div/div[1]/div[1]/span[2]').text
        range_to = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[2]/div/div[1]/div[1]/div/div/div/div[1]/div[1]/span[4]').text
        price_data[key] = str(range_from)+' to '+str(range_to)

    return price_data



if __name__ == '__main__':


    try:
        file = open("final.csv","r")
        reader = csv.reader(file)
        headings = next(reader)
        driver = prepare_driver()
        final_rows = []
        iterator_rows = [row for index, row in enumerate(reader) if index > 754]
        file.close()
        file = open("final_data.csv","a")
        writer = csv.writer(file)

        for row in iterator_rows:
            try:
                driver.get(domain)
                wait = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.ID, 'category')))
                row.append('5000')
                fill_form(driver, row)
                cars_data = scrape_results(driver)
                row.append(str(cars_data))
            except Exception as e:
                print("Exception->"+str(e))
            finally:
                print(row)
                writer.writerow(row)
                final_rows.append(row)


        #accommodations_data = json.dumps(accommodations_data, indent=4)
        #with open('booking_data.json', 'w') as f:
        #    f.write(accommodations_data)
    except Exception as e:
        print("Exception occurred->"+str(e))
    finally:
        driver.quit()
        file.close()
