from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def prepare_driver():
    '''Returns a Firefox Webdriver.'''
    options = Options()
    # options.add_argument('-headless')
    driver = Firefox(executable_path='/home/shivendra/seleniumExample/geckodriver/geckodriver', options=options)

    return driver
driver = prepare_driver()
wait = WebDriverWait(driver, 10)

driver.get("https://stackoverflow.com/users/login")

# Click GMail login
driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[2]/button[1]").click()

# type email
wait.until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys('shivendra.srivastava@auditoria.ai')

# click next
wait.until(EC.presence_of_element_located((By.ID, "next"))).click()

# type password
wait.until(EC.presence_of_element_located((By.ID, "Passwd"))).send_keys('ezeia@123')

# click signin
wait.until(EC.presence_of_element_located((By.ID, "signIn"))).click()

# wait for the end of the redirection
wait.until(EC.presence_of_element_located((By.ID, "nav-questions")))
