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
from db_connect import get_list_of_urls, get_collection
from datetime import datetime as dt
import pdb

def prepare_driver():
    '''Returns a Firefox Webdriver.'''
    options = Options()
    # options.add_argument('-headless')
    driver = Firefox(executable_path='geckodriver', options=options)

    return driver

def open_pages_one_by_one(driver, urls):
    list_of_dicts = []
    try:
        for count, url in enumerate(urls):
            try:
                walmart_dict = {}
                walmart_dict["product_url"] = str(url)
                driver.get(url)
                wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.ID, 'global-search-input')))
                walmart_dict['date'] = dt.today()
                walmart_dict['date_str'] = walmart_dict['date'].strftime('%Y-%m-%d')
                try:
                    walmart_dict["product_availability"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[4]/div[1]").text
                except:
                    walmart_dict["product_availability"] = "Available"
                try:
                    walmart_dict["product_category"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[3]/div[1]/div/nav/ol/li[1]/a/span").text
                except:
                    walmart_dict["product_category"] = " "
                try:
                    walmart_dict["product_name"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[2]/div/h1/div").text
                except:
                    walmart_dict["product_name"] = " "
                try:
                    walmart_dict["product_brand"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[3]/div/div[2]/a/span").text
                except:
                    walmart_dict["product_brand"] = " "
                try:
                    walmart_dict["product_sale_price"] = str(driver.find_element_by_xpath("//*[@id='price']/div/span[1]/span/span").get_attribute("aria-label")).split("$")[1]
                except:
                    try:
                        walmart_dict["product_sale_price"] = driver.find_element_by_xpath("//*[@id='price']/span/div[1]/span[1]/span/span[1]").text +" - "+ driver.find_element_by_xpath("//*[@id='price']/span/div[2]/span[1]/span/span[1]").text
                    except:
                        try:
                            walmart_dict["product_sale_price"] = driver.find_element_by_xpath("//*[@id='price']/div/span[1]/span/span[1]").text
                        except:
                            walmart_dict["product_sale_price"] = " "


                try:
                    walmart_dict["product_original_price"] = str(driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[4]/div/div[1]/div[1]/div[1]/div/div/div/span/span").get_attribute("aria-label")).split("$")[1]
                except:
                    try:
                        walmart_dict["product_original_price"] = str(driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[4]/div/div[1]/div[1]/div[1]/div/div/div/span[2]/span[1]").text).replace("Was $","")
                    except:
                        walmart_dict["product_original_price"] =  " "
                try:
                    walmart_dict["product_shipping"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[7]/div/div/div/div/div/span/div/div/div[1]/div[1]/span").text
                except:
                    walmart_dict["product_shipping"] = "No free shipping"
                try:
                    walmart_dict["product_delivery"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[10]/div/div/div/div/div/span/div/div").text
                except:
                    try:
                        walmart_dict["product_delivery"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[7]/div/div/div/div/div/span/div/div/div[1]/div[1]").text
                    except:
                        walmart_dict["product_delivery"] = "No information"
                try:
                    walmart_dict["product_review"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[3]/div/div[1]/div/span[3]/span").text
                except:
                    walmart_dict["product_review"] = "No reviews"
                try:
                    walmart_dict["product_sku"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[3]/div/div[3]").text.split("# ")[1]
                except:
                    walmart_dict["product_sku"] = " "
                try:
                    walmart_dict["product_pickup"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[8]/div/div/div/div/span/div/div/div[1]/div[1]/span/span").text
                except:
                    try:
                        walmart_dict["product_pickup"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[11]/div/div/div/div/span/div/div/div[1]").text
                    except:
                        walmart_dict["product_pickup"] = "No free pickups"
                try:
                    walmart_dict["product_image"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[1]/div[3]/div/div/div/div/div[1]/button/span/div[2]/div[1]/img").get_attribute("src")
                except:
                    walmart_dict["product_image"] = " "
                try:
                    walmart_dict["product_stock"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[4]/div/div[1]/div[2]/div[2]/div/div").text
                except:
                    try:
                        walmart_dict["product_stock"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[4]/div/div[1]/div[2]/div/div/div/span").text
                    except:
                        walmart_dict["product_stock"] = " "
                try:
                    walmart_dict["product_emi"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[4]/div/div[1]/div[1]/div[2]/div/div/div[1]/span[1]/object/b").text
                except:
                    walmart_dict["product_emi"] = "No information"
                try:
                    walmart_dict["product_rating"] = driver.find_element_by_xpath("//*[@id='customer-reviews-header']/div[2]/div[1]/div[1]/div[1]/span/span").text
                except:
                    walmart_dict["product_rating"] = "No ratings"

            except Exception as e1:
                print("Encountered an exception -> ",str(e1))
            finally:
                #print(count)
                if walmart_dict:
                    yield walmart_dict
                    list_of_dicts.append(walmart_dict)
    except Exception as e:
        print(e)
    finally:
        print("Scraping completed..")


if __name__ == '__main__':

    try:
        urls = get_list_of_urls("walmart")
        print("Total number of urls found ",len(urls))
        driver = prepare_driver()
        client_to_save_to = get_collection("walmart","116.203.177.107")
        collection = client_to_save_to["samsung_scraping"]["walmart"]
        try:
            print("Scraping started..")
            for data in open_pages_one_by_one(driver, urls):
                print(data)
                if data.get("product_sale_price").strip() != "" or data.get("product_original_price").strip() != "":
                    collection.insert(data)
                    print("Inserted data into MongoDB..")

        except:
            pass
    except Exception as e:
        print(str(e))
    finally:
        if driver:
            driver.quit()
        if client_to_save_to:
            client_to_save_to.close()
