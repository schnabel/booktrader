import time

from getpass import getpass
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

css_selector_login = '#app > div > div > div:nth-child(1) > header > div > div.header-login-bar.header-login-bar-landingpage > div > div > div.col-sm-5.col-md-4.text-right > div > div > div.btn-header.dropdown-toggle'
css_selector_user_name_field = '#app > div > div > div:nth-child(1) > header > div > div.header-login-bar.header-login-bar-landingpage > div > div > div.col-sm-5.col-md-4.text-right > div > div > div.dropdown-menu.login-dropdown.p-2 > form > div:nth-child(1) > input'
css_selector_password_field = '#app > div > div > div:nth-child(1) > header > div > div.header-login-bar.header-login-bar-landingpage > div > div > div.col-sm-5.col-md-4.text-right > div > div > div.dropdown-menu.login-dropdown.p-2 > form > div:nth-child(2) > div > input'
css_selector_submit = '#app > div > div > div:nth-child(1) > header > div > div.header-login-bar.header-login-bar-landingpage > div > div > div.col-sm-5.col-md-4.text-right > div > div > div.dropdown-menu.login-dropdown.p-2 > form > button'
css_selector_goto_quicksell = '#app > div > div > div.no-gutter-xs.container-body > div > div.sm\:sticky.top-0 > div > div > div > div.col-xs-12.col-sm-9.col-md-8.col-lg-7 > div > div.row.text-xs.font-normal > div.hidden-xs.col-sm-7.mt-1 > a'
css_selector_file_selector = '#quicksell-file-choice-body > div > input[type=file]'
css_selector_upload = '#quicksell-file-choice-body > div > div > div > button'
css_selector_upload_complete = '#app > div > div > div.no-gutter-xs.container-body > div > div.row.quicksell-results-header > div.col-xs-12.col-sm-6.col-md-5.text-right > button'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def goto_momox():
    driver.get("https://www.momox.de")
    driver.maximize_window()
    accept_cookies = driver.find_element_by_xpath('//button[text()="Alle akzeptieren"]')
    time.sleep(1)
    accept_cookies.click()

def login():
    login = driver.find_element_by_css_selector(css_selector_login)
    login.click()
    user_name = input("E-mail: ")
    password = getpass("Passwort: ")
    user_name_field = driver.find_element_by_css_selector(css_selector_user_name_field)
    user_name_field.click()
    time.sleep(1)
    user_name_field.send_keys(user_name)
    password_field = driver.find_element_by_css_selector(css_selector_password_field)
    time.sleep(1)
    password_field.click()
    password_field.send_keys(password)
    submit_field = driver.find_element_by_css_selector(css_selector_submit)
    submit_field.click()
    time.sleep(1)

def goto_quicksell():
    goto_quicksell = driver.find_element_by_css_selector(css_selector_goto_quicksell)
    goto_quicksell.click()
    time.sleep(2)

def file_selector():
    file_selector = driver.find_element(by=By.CSS_SELECTOR, value=css_selector_file_selector)
    file_selector.send_keys(r"/home/dirk/git/schnabel/booktrader/data/ISBN_0001.txt")
    time.sleep(2)
    upload = driver.find_element(by=By.CSS_SELECTOR, value=css_selector_upload)
    upload.click()
    time.sleep(2)

def wait_for_quotes():
    wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "icon-btn-cart-box")))
    print('Weiter geht es!')

def get_quotes():
    quotes = []
    # response = requests.get("https://www.momox.de/schneller-verkaufen/angebot/")
    # soup = BeautifulSoup(response.text, 'html.parser')
    # table = soup.find("table", "quicksell-results-table")
    # for row in soup.find_all("tr", {"class": "product-row-loaded product-row-selected"}):
    #     isbn = row.find(re.compile("\d+,*\d*"))
    #     price_location = row.find("td", {"class": "col-price"})
    #     price = [float(match.replace(",", ".")) for match in re.findall("\d+,*\d*", price_location.get_text())]
    #     quotes.extend(isbn, price)
    products = driver.find_elements(by=By.CLASS_NAME, value='product-row-loaded product-row-selected')
    print(products)
    return quotes

goto_momox()
login()
goto_quicksell()
file_selector()
wait_for_quotes()
get_quotes()