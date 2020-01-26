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
    popup_handler(driver)
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
    #driver.implicitly_wait(5)

    driver.find_element_by_class_name('obv_adobe_landing_submit')\
        .click()
    wait = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'adobe_obv_result_buy_droom')))

def scrape_results(driver):
    '''Returns the data from n_results amount of results.'''
    price_data = {'Good':'','Fair':'','V Good':'','Excellent':''}
    popup_handler(driver)
    for key in price_data:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, key))).click()
        range_from = driver.find_element_by_xpath('/html/body/div[3]/div[5]/div[2]/div/div[1]/div[1]/div/div/div/div[1]/div[1]/span[2]').text
        range_to = driver.find_element_by_xpath('/html/body/div[3]/div[5]/div[2]/div/div[1]/div[1]/div/div/div/div[1]/div[1]/span[4]').text
        price_data[key] = str(range_from)+' to '+str(range_to)

    return price_data

def popup_handler(driver):
    popup_cross = driver.find_element_by_xpath("//*[@id='ad_campain_modal']/div/div/div/button/i").click()

    #driver.switch_to_window(driver.window_handles[0])

if __name__ == '__main__':

    try:
        file = open("filtered.csv","r")
        reader = csv.reader(file)
        headings = next(reader)
        driver = prepare_driver()
        iterator_rows = [row for index, row in enumerate(reader) if index > 1115]
        file.close()
        file = open("filtered_obv.csv","a")
        writer = csv.writer(file)
        for row in iterator_rows:
            try:
                driver.get(domain)
                wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.ID, 'category')))
                row.append('5000')
                fill_form(driver, row)
                cars_data = scrape_results(driver)
                row.append(str(cars_data))
                writer.writerow(row)
            except Exception as e:
                print("Exception->"+str(e))
            finally:
                print(row)

    except Exception as e:
        print("Exception occurred->"+str(e))
    finally:
        driver.quit()
        file.close()
# x=[['Hyundai', 'Verna', '2007', 'xxi abs', '5000', "{'Good': '1,71,383 to 1,81,984', 'Fair': '1,67,098 to 1,77,434', 'V Good': '1,75,668 to 1,86,534', 'Excellent': '1,79,952 to 1,91,083'}"],
# ['Hyundai', 'Verna', '2019', '1.4 VTVT E', '5000', "{'Good': '7,01,092 to 7,44,458', 'Fair': '6,83,564 to 7,25,847', 'V Good': '7,18,619 to 7,63,070', 'Excellent': '7,36,146 to 7,81,681'}"],
# ['Hyundai', 'Verna', '2019', '1.4 VTVT EX', '5000', "{'Good': '8,04,345 to 8,54,099', 'Fair': '7,84,237 to 8,32,746', 'V Good': '8,24,454 to 8,75,451', 'Excellent': '8,44,563 to 8,96,804'}"],
# ['Hyundai', 'Verna', '2019', '1.6 CRDI SX', '5000', "{'Good': '10,92,505 to 11,60,083', 'Fair': '10,65,193 to 11,31,081', 'V Good': '11,19,818 to 11,89,085', 'Excellent': '11,47,130 to 12,18,087'}"],
# ['Hyundai', 'Verna', '2019', '1.6 CRDI SX (O)', '5000', "{'Good': '12,10,290 to 12,85,154', 'Fair': '11,80,033 to 12,53,025', 'V Good': '12,40,548 to 13,17,283', 'Excellent': '12,70,805 to 13,49,411'}"],
# ['Hyundai', 'Verna', '2019', '1.6 CRDI SX (O) AT', '5000', "{'Good': '13,06,813 to 13,87,647', 'Fair': '12,74,143 to 13,52,956', 'V Good': '13,39,483 to 14,22,338', 'Excellent': '13,72,154 to 14,57,029'}"],
# ['Hyundai', 'Verna', '2019', '1.6 CRDI SX PLUS AT', '5000', "{'Good': '12,34,571 to 13,10,937', 'Fair': '12,03,707 to 12,78,163', 'V Good': '12,65,436 to 13,43,710', 'Excellent': '12,96,300 to 13,76,483'}"],
# ['Hyundai', 'Verna', '2019', '1.6 VTVT SX', '5000', "{'Good': '8,80,934 to 9,35,424', 'Fair': '8,58,910 to 9,12,039', 'V Good': '9,02,957 to 9,58,810', 'Excellent': '9,24,980 to 9,82,196'}"],
# ['Hyundai', 'Verna', '2019', '1.6 VTVT SX (O)', '5000', "{'Good': '10,67,642 to 11,33,682', 'Fair': '10,40,951 to 11,05,340', 'V Good': '10,94,333 to 11,62,024', 'Excellent': '11,21,024 to 11,90,366'}"],
# ['Hyundai', 'Verna', '2019', 'EX 1.4 CRDI', '5000', "{'Good': '8,90,931 to 9,46,041', 'Fair': '8,68,658 to 9,22,390', 'V Good': '9,13,205 to 9,69,692', 'Excellent': '9,35,478 to 9,93,343'}"],
# ['Hyundai', 'Verna', '2019', 'SX PLUS 1.6 VTVT AT', '5000', "{'Good': '10,58,617 to 11,24,099', 'Fair': '10,32,152 to 10,95,996', 'V Good': '10,85,083 to 11,52,201', 'Excellent': '11,11,548 to 11,80,304'}"],
# ['Hyundai', 'Verna', '2018', '1.4 vtvt e', '5000', "{'Good': '6,18,926 to 6,57,210', 'Fair': '6,03,453 to 6,40,780', 'V Good': '6,34,400 to 6,73,641', 'Excellent': '6,49,873 to 6,90,071'}"],
# ['Hyundai', 'Verna', '2018', '1.4 VTVT EX', '5000', "{'Good': '7,19,195 to 7,63,682', 'Fair': '7,01,215 to 7,44,590', 'V Good': '7,37,175 to 7,82,774', 'Excellent': '7,55,155 to 8,01,866'}"],
# ['Hyundai', 'Verna', '2018', '1.6 crdi e', '5000', "{'Good': '7,66,942 to 8,14,382', 'Fair': '7,47,769 to 7,94,023', 'V Good': '7,86,116 to 8,34,742', 'Excellent': '8,05,290 to 8,55,101'}"],
# ['Hyundai', 'Verna', '2018', '1.6 crdi ex', '5000', "{'Good': '8,65,999 to 9,19,566', 'Fair': '8,44,349 to 8,96,577', 'V Good': '8,87,649 to 9,42,555', 'Excellent': '9,09,299 to 9,65,544'}"],
# ['Hyundai', 'Verna', '2018', '1.6 crdi ex at', '5000', "{'Good': '9,82,956 to 10,43,758', 'Fair': '9,58,382 to 10,17,664', 'V Good': '10,07,530 to 10,69,852', 'Excellent': '10,32,104 to 10,95,946'}"],
# ['Hyundai', 'Verna', '2018', '1.6 crdi sx', '5000', "{'Good': '9,54,330 to 10,13,361', 'Fair': '9,30,472 to 9,88,027', 'V Good': '9,78,188 to 10,38,695', 'Excellent': '10,02,047 to 10,64,029'}"],
# ['Hyundai', 'Verna', '2018', '1.6 crdi sx (o)', '5000', "{'Good': '10,65,563 to 11,31,474', 'Fair': '10,38,924 to 11,03,187', 'V Good': '10,92,202 to 11,59,761', 'Excellent': '11,18,841 to 11,88,048'}"],
# ['Hyundai', 'Verna', '2018', '1.6 crdi sx at', '5000', "{'Good': '10,66,450 to 11,32,416', 'Fair': '10,39,789 to 11,04,106', 'V Good': '10,93,111 to 11,60,727', 'Excellent': '11,19,773 to 11,89,037'}"],
# ['Hyundai', 'Verna', '2018', '1.6 crdi sx plus at', '5000', "{'Good': '10,77,013 to 11,43,633', 'Fair': '10,50,088 to 11,15,042', 'V Good': '11,03,939 to 11,72,223', 'Excellent': '11,30,864 to 12,00,814'}"],
# ['Hyundai', 'Verna', '2018', '1.6 vtvt e', '5000', "{'Good': '6,41,378 to 6,81,050', 'Fair': '6,25,343 to 6,64,024', 'V Good': '6,57,412 to 6,98,077', 'Excellent': '6,73,446 to 7,15,103'}"],
# ['Hyundai', 'Verna', '2018', '1.6 vtvt ex', '5000', "{'Good': '7,34,150 to 7,79,561', 'Fair': '7,15,796 to 7,60,072', 'V Good': '7,52,504 to 7,99,050', 'Excellent': '7,70,857 to 8,18,539'}"],
# ['Hyundai', 'Verna', '2018', '1.6 vtvt ex at', '5000', "{'Good': '8,66,932 to 9,20,557', 'Fair': '8,45,259 to 8,97,543', 'V Good': '8,88,606 to 9,43,571', 'Excellent': '9,10,279 to 9,66,585'}"],
# ['Hyundai', 'Verna', '2018', '1.6 vtvt sx', '5000', "{'Good': '7,71,375 to 8,19,089', 'Fair': '7,52,090 to 7,98,611', 'V Good': '7,90,659 to 8,39,566', 'Excellent': '8,09,944 to 8,60,043'}"],
# ['Hyundai', 'Verna', '2018', '1.6 vtvt sx (o)', '5000', "{'Good': '9,35,762 to 9,93,644', 'Fair': '9,12,368 to 9,68,803', 'V Good': '9,59,156 to 10,18,485', 'Excellent': '9,82,550 to 10,43,326'}"],
# ['Hyundai', 'Verna', '2018', '1.6 vtvt sx (o) at', '5000', "{'Good': '10,27,001 to 10,90,527', 'Fair': '10,01,326 to 10,63,264', 'V Good': '10,52,677 to 11,17,791', 'Excellent': '10,78,352 to 11,45,054'}"],
# ['Hyundai', 'Verna', '2018', 'Anniversary Edition 1.6 CRDI SX (O)', '5000', "{'Good': '11,01,900 to 11,70,059', 'Fair': '10,74,353 to 11,40,807', 'V Good': '11,29,448 to 11,99,310', 'Excellent': '11,56,995 to 12,28,562'}"],
# ['Hyundai', 'Verna', '2018', 'Anniversary Edition 1.6 VTVT SX (O)', '5000', "{'Good': '9,71,069 to 10,31,135', 'Fair': '9,46,792 to 10,05,357', 'V Good': '9,95,346 to 10,56,913', 'Excellent': '10,19,622 to 10,82,692'}"],
# ['Hyundai', 'Verna', '2018', 'Anniversary Edition 1.6 VTVT SX (O) AT', '5000', "{'Good': '10,62,925 to 11,28,673', 'Fair': '10,36,352 to 11,00,456', 'V Good': '10,89,498 to 11,56,890', 'Excellent': '11,16,071 to 11,85,107'}"],
# ['Hyundai', 'Verna', '2015', '1.4 crdi', '5000', "{'Good': '5,07,458 to 5,38,847', 'Fair': '4,94,771 to 5,25,376', 'V Good': '5,20,144 to 5,52,318', 'Excellent': '5,32,831 to 5,65,789'}"],
# ['Hyundai', 'Verna', '2015', '1.4 cx crdi mt', '5000', "{'Good': '5,43,177 to 5,76,775', 'Fair': '5,29,597 to 5,62,356', 'V Good': '5,56,756 to 5,91,195', 'Excellent': '5,70,335 to 6,05,614'}"],
# ['Hyundai', 'Verna', '2015', '1.4 cx vtvt mt', '5000', "{'Good': '4,63,382 to 4,92,045', 'Fair': '4,51,797 to 4,79,744', 'V Good': '4,74,966 to 5,04,346', 'Excellent': '4,86,551 to 5,16,647'}"],
# ['Hyundai', 'Verna', '2015', '1.4 gl crdi mt', '5000', "{'Good': '4,88,742 to 5,18,974', 'Fair': '4,76,524 to 5,05,999', 'V Good': '5,00,961 to 5,31,948', 'Excellent': '5,13,179 to 5,44,922'}"],
# ['Hyundai', 'Verna', '2015', '1.4 gl vtvt mt', '5000', "{'Good': '4,11,704 to 4,37,170', 'Fair': '4,01,411 to 4,26,241', 'V Good': '4,21,996 to 4,48,099', 'Excellent': '4,32,289 to 4,59,028'}"],
# ['Hyundai', 'Verna', '2015', '1.4 vtvt', '5000', "{'Good': '4,33,033 to 4,59,819', 'Fair': '4,22,208 to 4,48,323', 'V Good': '4,43,859 to 4,71,314', 'Excellent': '4,54,685 to 4,82,810'}"],
# ['Hyundai', 'Verna', '2015', '1.6 crdi', '5000', "{'Good': '5,37,918 to 5,71,192', 'Fair': '5,24,470 to 5,56,912', 'V Good': '5,51,366 to 5,85,471', 'Excellent': '5,64,814 to 5,99,751'}"],
# ['Hyundai', 'Verna', '2015', '1.6 crdi s', '5000', "{'Good': '5,88,997 to 6,25,429', 'Fair': '5,74,272 to 6,09,794', 'V Good': '6,03,722 to 6,41,065', 'Excellent': '6,18,447 to 6,56,701'}"],
# ['Hyundai', 'Verna', '2015', '1.6 crdi s(o)', '5000', "{'Good': '6,24,372 to 6,62,993', 'Fair': '6,08,763 to 6,46,418', 'V Good': '6,39,981 to 6,79,568', 'Excellent': '6,55,590 to 6,96,142'}"],
# ['Hyundai', 'Verna', '2015', '1.6 crdi sx', '5000', "{'Good': '6,20,120 to 6,58,478', 'Fair': '6,04,617 to 6,42,016', 'V Good': '6,35,623 to 6,74,940', 'Excellent': '6,51,126 to 6,91,402'}"],
# ['Hyundai', 'Verna', '2015', '1.6 crdi sx (o)', '5000', "{'Good': '6,82,238 to 7,24,439', 'Fair': '6,65,182 to 7,06,328', 'V Good': '6,99,294 to 7,42,550', 'Excellent': '7,16,350 to 7,60,661'}"],
# ['Hyundai', 'Verna', '2015', '1.6 crdi sx (o) at', '5000', "{'Good': '7,41,117 to 7,86,960', 'Fair': '7,22,589 to 7,67,286', 'V Good': '7,59,645 to 8,06,634', 'Excellent': '7,78,173 to 8,26,308'}"],
# ['Hyundai', 'Verna', '2015', '1.6 sx crdi at', '5000', "{'Good': '7,18,706 to 7,63,162', 'Fair': '7,00,738 to 7,44,083', 'V Good': '7,36,673 to 7,82,241', 'Excellent': '7,54,641 to 8,01,320'}"],
# ['Hyundai', 'Verna', '2015', '1.6 sx vtvt at', '5000', "{'Good': '5,57,130 to 5,91,592', 'Fair': '5,43,202 to 5,76,802', 'V Good': '5,71,058 to 6,06,381', 'Excellent': '5,84,987 to 6,21,171'}"],
# ['Hyundai', 'Verna', '2015', '1.6 vtvt', '5000', "{'Good': '4,76,694 to 5,06,180', 'Fair': '4,64,777 to 4,93,526', 'V Good': '4,88,611 to 5,18,835', 'Excellent': '5,00,529 to 5,31,489'}"],
# ['Hyundai', 'Verna', '2015', '1.6 vtvt s', '5000', "{'Good': '4,97,422 to 5,28,190', 'Fair': '4,84,987 to 5,14,986', 'V Good': '5,09,858 to 5,41,395', 'Excellent': '5,22,293 to 5,54,600'}"],
# ['Hyundai', 'Verna', '2015', '1.6 vtvt s (o) at', '5000', "{'Good': '5,83,128 to 6,19,198', 'Fair': '5,68,550 to 6,03,718', 'V Good': '5,97,706 to 6,34,678', 'Excellent': '6,12,284 to 6,50,158'}"],
# ['Hyundai', 'Verna', '2015', '1.6 VTVT S(O)', '5000', "{'Good': '5,27,807 to 5,60,455', 'Fair': '5,14,612 to 5,46,444', 'V Good': '5,41,003 to 5,74,467', 'Excellent': '5,54,198 to 5,88,478'}"],
# ['Hyundai', 'Verna', '2015', '1.6 vtvt sx', '5000', "{'Good': '5,13,614 to 5,45,384', 'Fair': '5,00,774 to 5,31,750', 'V Good': '5,26,455 to 5,59,019', 'Excellent': '5,39,295 to 5,72,653'}"],
# ['Hyundai', 'Verna', '2015', '1.6 vtvt sx (o)', '5000', "{'Good': '5,96,490 to 6,33,386', 'Fair': '5,81,577 to 6,17,551', 'V Good': '6,11,402 to 6,49,221', 'Excellent': '6,26,314 to 6,65,055'}"],
# ['Hyundai', 'Verna', '2015', '1.6 vtvt sx (o) at', '5000', "{'Good': '6,50,643 to 6,90,889', 'Fair': '6,34,377 to 6,73,617', 'V Good': '6,66,909 to 7,08,162', 'Excellent': '6,83,176 to 7,25,434'}"],
# ['Hyundai', 'Verna', '2014', '1.4 crdi', '5000', "{'Good': '4,11,901 to 4,37,379', 'Fair': '4,01,604 to 4,26,445', 'V Good': '4,22,199 to 4,48,314', 'Excellent': '4,32,496 to 4,59,248'}"],
# ['Hyundai', 'Verna', '2014', '1.4 crdi ex', '5000', "{'Good': '4,63,903 to 4,92,598', 'Fair': '4,52,305 to 4,80,283', 'V Good': '4,75,500 to 5,04,913', 'Excellent': '4,87,098 to 5,17,228'}"],
# ['Hyundai', 'Verna', '2014', '1.4 cx crdi mt', '5000', "{'Good': '4,82,011 to 5,11,826', 'Fair': '4,69,961 to 4,99,030', 'V Good': '4,94,061 to 5,24,622', 'Excellent': '5,06,111 to 5,37,417'}"],
# ['Hyundai', 'Verna', '2014', '1.4 cx vtvt mt', '5000', "{'Good': '4,13,207 to 4,38,767', 'Fair': '4,02,877 to 4,27,798', 'V Good': '4,23,538 to 4,49,736', 'Excellent': '4,33,868 to 4,60,705'}"],
# ['Hyundai', 'Verna', '2014', '1.4 gl crdi mt', '5000', "{'Good': '4,33,706 to 4,60,533', 'Fair': '4,22,863 to 4,49,020', 'V Good': '4,44,549 to 4,72,046', 'Excellent': '4,55,391 to 4,83,560'}"],
# ['Hyundai', 'Verna', '2014', '1.4 gl vtvt mt', '5000', "{'Good': '3,67,125 to 3,89,833', 'Fair': '3,57,947 to 3,80,088', 'V Good': '3,76,303 to 3,99,579', 'Excellent': '3,85,481 to 4,09,325'}"],
# ['Hyundai', 'Verna', '2014', '1.4 vtvt', '5000', "{'Good': '3,86,557 to 4,10,468', 'Fair': '3,76,893 to 4,00,206', 'V Good': '3,96,221 to 4,20,730', 'Excellent': '4,05,885 to 4,30,991'}"],
# ['Hyundai', 'Verna', '2014', '1.4 vtvt ex', '5000', "{'Good': '4,20,332 to 4,46,332', 'Fair': '4,09,823 to 4,35,173', 'V Good': '4,30,840 to 4,57,490', 'Excellent': '4,41,348 to 4,68,648'}"],
# ['Hyundai', 'Verna', '2014', '1.6 crdi', '5000', "{'Good': '4,82,025 to 5,11,841', 'Fair': '4,69,974 to 4,99,045', 'V Good': '4,94,075 to 5,24,637', 'Excellent': '5,06,126 to 5,37,433'}"],
# ['Hyundai', 'Verna', '2014', '1.6 crdi ex', '5000', "{'Good': '4,96,485 to 5,27,196', 'Fair': '4,84,073 to 5,14,016', 'V Good': '5,08,897 to 5,40,376', 'Excellent': '5,21,309 to 5,53,555'}"],
# ['Hyundai', 'Verna', '2014', '1.6 crdi ex at', '5000', "{'Good': '5,69,255 to 6,04,467', 'Fair': '5,55,024 to 5,89,355', 'V Good': '5,83,486 to 6,19,578', 'Excellent': '5,97,718 to 6,34,690'}"],
# ['Hyundai', 'Verna', '2014', '1.6 CRDI SX', '5000', "{'Good': '5,50,289 to 5,84,328', 'Fair': '5,36,532 to 5,69,720', 'V Good': '5,64,047 to 5,98,936', 'Excellent': '5,77,804 to 6,13,544'}"],
# ['Hyundai', 'Verna', '2014', '1.6 crdi sx (o)', '5000', "{'Good': '6,01,907 to 6,39,138', 'Fair': '5,86,859 to 6,23,160', 'V Good': '6,16,955 to 6,55,117', 'Excellent': '6,32,002 to 6,71,095'}"],
# ['Hyundai', 'Verna', '2014', '1.6 crdi sx (o) at', '5000', "{'Good': '6,51,338 to 6,91,627', 'Fair': '6,35,055 to 6,74,337', 'V Good': '6,67,622 to 7,08,918', 'Excellent': '6,83,905 to 7,26,209'}"],
# ['Hyundai', 'Verna', '2014', '1.6 SX CRDI AT', '5000', "{'Good': '6,37,774 to 6,77,224', 'Fair': '6,21,830 to 6,60,293', 'V Good': '6,53,718 to 6,94,154', 'Excellent': '6,69,663 to 7,11,085'}"],
# ['Hyundai', 'Verna', '2014', '1.6 sx vtvt at', '5000', "{'Good': '4,89,639 to 5,19,926', 'Fair': '4,77,398 to 5,06,928', 'V Good': '5,01,880 to 5,32,924', 'Excellent': '5,14,121 to 5,45,922'}"],
# ['Hyundai', 'Verna', '2014', '1.6 vtvt', '5000', "{'Good': '4,24,663 to 4,50,931', 'Fair': '4,14,047 to 4,39,658', 'V Good': '4,35,280 to 4,62,205', 'Excellent': '4,45,897 to 4,73,478'}"],
# ['Hyundai', 'Verna', '2014', '1.6 VTVT EX', '5000', "{'Good': '4,31,113 to 4,57,780', 'Fair': '4,20,336 to 4,46,336', 'V Good': '4,41,891 to 4,69,225', 'Excellent': '4,52,669 to 4,80,669'}"],
# ['Hyundai', 'Verna', '2014', '1.6 vtvt ex at', '5000', "{'Good': '5,04,346 to 5,35,543', 'Fair': '4,91,738 to 5,22,154', 'V Good': '5,16,955 to 5,48,932', 'Excellent': '5,29,564 to 5,62,320'}"],
# ['Hyundai', 'Verna', '2014', '1.6 vtvt sx', '5000', "{'Good': '4,57,554 to 4,85,857', 'Fair': '4,46,115 to 4,73,710', 'V Good': '4,68,993 to 4,98,003', 'Excellent': '4,80,432 to 5,10,149'}"],
# ['Hyundai', 'Verna', '2014', '1.6 vtvt sx (o)', '5000', "{'Good': '5,25,747 to 5,58,267', 'Fair': '5,12,603 to 5,44,311', 'V Good': '5,38,891 to 5,72,224', 'Excellent': '5,52,034 to 5,86,181'}"],
# ['Hyundai', 'Verna', '2014', '1.6 vtvt sx (o) at', '5000', "{'Good': '5,71,824 to 6,07,195', 'Fair': '5,57,529 to 5,92,015', 'V Good': '5,86,120 to 6,22,375', 'Excellent': '6,00,416 to 6,37,555'}"],
# ['Hyundai', 'Verna', '2017', '1.4 crdi', '5000', "{'Good': '6,48,394 to 6,88,500', 'Fair': '6,32,184 to 6,71,288', 'V Good': '6,64,603 to 7,05,713', 'Excellent': '6,80,813 to 7,22,925'}"],
# ['Hyundai', 'Verna', '2017', '1.4 VTVT', '5000', "{'Good': '5,50,421 to 5,84,467', 'Fair': '5,36,660 to 5,69,856', 'V Good': '5,64,181 to 5,99,079', 'Excellent': '5,77,942 to 6,13,691'}"],
# ['Hyundai', 'Verna', '2017', '1.6 crdi e', '5000', "{'Good': '6,61,755 to 7,02,688', 'Fair': '6,45,211 to 6,85,121', 'V Good': '6,78,299 to 7,20,255', 'Excellent': '6,94,842 to 7,37,822'}"],
# ['Hyundai', 'Verna', '2017', '1.6 crdi ex', '5000', "{'Good': '7,42,180 to 7,88,088', 'Fair': '7,23,626 to 7,68,386', 'V Good': '7,60,735 to 8,07,790', 'Excellent': '7,79,289 to 8,27,493'}"],
# ['Hyundai', 'Verna', '2017', '1.6 crdi ex at', '5000', "{'Good': '8,45,307 to 8,97,594', 'Fair': '8,24,174 to 8,75,154', 'V Good': '8,66,439 to 9,20,033', 'Excellent': '8,87,572 to 9,42,473'}"],
# ['Hyundai', 'Verna', '2017', '1.6 CRDi S', '5000', "{'Good': '7,61,559 to 8,08,666', 'Fair': '7,42,520 to 7,88,449', 'V Good': '7,80,598 to 8,28,882', 'Excellent': '7,99,637 to 8,49,099'}"],
# ['Hyundai', 'Verna', '2017', '1.6 CRDi S AT', '5000', "{'Good': '8,26,353 to 8,77,468', 'Fair': '8,05,694 to 8,55,531', 'V Good': '8,47,012 to 8,99,404', 'Excellent': '8,67,671 to 9,21,341'}"],
# ['Hyundai', 'Verna', '2017', '1.6 CRDi SX', '5000', "{'Good': '8,17,144 to 8,67,689', 'Fair': '7,96,715 to 8,45,997', 'V Good': '8,37,573 to 8,89,381', 'Excellent': '8,58,001 to 9,11,073'}"],
# ['Hyundai', 'Verna', '2017', '1.6 crdi sx (o)', '5000', "{'Good': '9,09,504 to 9,65,762', 'Fair': '8,86,766 to 9,41,618', 'V Good': '9,32,241 to 9,89,906', 'Excellent': '9,54,979 to 10,14,050'}"],
# ]
# file = open("filtered_obv.csv","a")
# writer = csv.writer(file)
# writer.writerows(x)
# file.close()
