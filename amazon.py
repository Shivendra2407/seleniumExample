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
                amazon_dict = {}
                amazon_dict["product_url"] = str(url)
                driver.get(url)
                try:
                    wait = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                        (By.ID, 'twotabsearchtextbox')))
                except:
                    continue
                amazon_dict['date'] = dt.today()
                amazon_dict['date_str'] = amazon_dict['date'].strftime('%Y-%m-%d')

                try:
                    rank_data = driver.find_element_by_xpath("//*[@id='productDetails_detailBullets_sections1']/tbody/tr[8]/td/span/span[1]").text.split('(')[0]
                    amazon_dict["product_bestseller_rank"] = rank_data.split("in")[0]
                    amazon_dict["product_category"] = rank_data.split("in")[1]
                except:
                    amazon_dict["product_bestseller_rank"] = ' '
                    amazon_dict["product_category"] = ' '
                try:
                    amazon_dict["product_support"] = driver.find_element_by_xpath("//*[@id='productSupportAndReturnPolicy-product-support-policy-anchor-text']").text
                except:
                    amazon_dict["product_support"] = ' '
                try:
                    amazon_dict["product_name"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[2]/div/h1/div").text
                except:
                    amazon_dict["product_name"] = " "
                try:
                    amazon_dict["product_sold_by"] = driver.find_element_by_xpath("//*[@id='sellerProfileTriggerId']").text
                except:
                    amazon_dict["product_sold_by"] = " "
                try:
                    amazon_dict["product_buying_features"] = {}
                    amazon_dict["product_buying_features"]["new_used"] = "at " +str(driver.find_element_by_xpath("//*[@id='buyNew_noncbb']/span").text)
                except:
                    try:
                        amazon_dict["product_buying_features"]["new_used"] = str(driver.find_element_by_xpath("//*[@id='olp-upd-new-used']/span/a").text).split(")")[1]
                    except:
                        amazon_dict["product_buying_features"]["new_used"] = ' '
                try:
                    amazon_dict["product_sale_price"] = str(driver.find_element_by_xpath("//*[@id='priceblock_ourprice']").text)
                    amazon_dict["product_sale_price"] = amazon_dict["product_sale_price"].replace("$","")
                except:
                    try:
                        amazon_dict["product_sale_price"] = str(driver.find_element_by_xpath("//*[@id='comparison_price_row']/td[1]/span/span[2]/span[2]").text)+"."+str(driver.find_element_by_xpath("//*[@id='comparison_price_row']/td[1]/span/span[2]/span[3]").text)
                    except:
                        try:
                            amazon_dict["product_sale_price"] = "from "+str(driver.find_element_by_xpath("//*[@id='comparison_price_row']/td[1]/span").text).split("$")[1]
                        except:
                            amazon_dict["product_sale_price"] = " "
                try:
                    amazon_dict["product_original_price"] = str(driver.find_element_by_xpath("//*[@id='price']/table/tbody/tr[1]/td[2]/span[1]").text).replace("$","")
                except:
                    amazon_dict["product_original_price"] =  " "
                try:
                    amazon_dict["product_shipping"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[7]/div/div/div/div/div/span/div/div/div[1]/div[1]/span").text
                except:
                    amazon_dict["product_shipping"] = "No free shipping"
                try:
                    amazon_dict["product_delivery"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[10]/div/div/div/div/div/span/div/div").text
                except:
                    try:
                        amazon_dict["product_delivery"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[7]/div/div/div/div/div/span/div/div/div[1]/div[1]").text
                    except:
                        amazon_dict["product_delivery"] = "No information"
                try:
                    amazon_dict["product_review"] = driver.find_element_by_xpath("//*[@id='dp-summary-see-all-reviews']/h2").text
                except:
                    amazon_dict["product_review"] = "No reviews"
                try:
                    amazon_dict["product_sku"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[3]/div/div[3]").text.split("# ")[1]
                except:
                    amazon_dict["product_sku"] = " "
                try:
                    amazon_dict["product_pickup"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[8]/div/div/div/div/span/div/div/div[1]/div[1]/span/span").text
                except:
                    try:
                        amazon_dict["product_pickup"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[11]/div/div/div/div/span/div/div/div[1]").text
                    except:
                        amazon_dict["product_pickup"] = "No free pickups"
                try:
                    amazon_dict["product_gift_wrap"] = driver.find_element_by_xpath("//*[@id='detailPageGifting_feature_div']/span").text
                except:
                    amazon_dict["product_gift_wrap"] = "Gift wrap not available"
                try:
                    amazon_dict["product_image"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[1]/div[3]/div/div/div/div/div[1]/button/span/div[2]/div[1]/img").get_attribute("src")
                except:
                    amazon_dict["product_image"] = " "
                try:
                    amazon_dict["product_stock"] = str(driver.find_element_by_xpath("//*[@id='availability']/span").text).strip()
                    amazon_dict["product_availability"] = "Available"
                except:
                    amazon_dict["product_stock"] = " "
                    amazon_dict["product_availability"] = "Not available"
                try:
                    amazon_dict["product_emi"] = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div[4]/div/div[1]/div[1]/div[2]/div/div/div[1]/span[1]/object/b").text
                except:
                    amazon_dict["product_emi"] = "No information"
                try:
                    amazon_dict["product_rating"] = driver.find_element_by_xpath("//*[@id='reviewsMedley']/div/div[1]/div[1]/div/div/div[2]/div/span/span/a/span").text.split("out")[0].strip()
                except:
                    amazon_dict["product_rating"] = "No ratings"

            except Exception as e1:
                print("Encountered an exception -> ",str(e1))
            finally:
                #print(count)
                if amazon_dict:
                    yield amazon_dict
                    list_of_dicts.append(amazon_dict)
    except Exception as e:
        print(e)
    finally:
        print("Scraping completed..")
        if driver:
            driver.quit()

if __name__ == '__main__':

    try:
        urls = get_list_of_urls("amazon")
        print("Total number of urls found ",len(urls))
        driver = prepare_driver()
        client_to_save_to = get_collection("amazon","116.203.177.107")
        collection = client_to_save_to["samsung_scraping"]["amazon"]
        try:
            print("Scraping started..")
            for data in open_pages_one_by_one(driver, urls):
                print(data)
                if data.get("product_sale_price").strip() != "":
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
