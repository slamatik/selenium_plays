from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time


tickers = ['AAPL', 'TSLA']

EXE_PATH = r'C:\Users\slama\Desktop\chromedriver.exe'
driver = webdriver.Chrome(service=Service(EXE_PATH), options=webdriver.ChromeOptions())
driver.get('https://finance.yahoo.com/quote/AAPL/history')

URL = 'https://finance.yahoo.com/quote/'
URL_SETTINGS = '/history?period1=345427200&period2=1648944000&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'

for ticker in tickers:
    driver.get(URL + ticker + URL_SETTINGS)
    try:
        driver.find_element(by=By.NAME, value='agree').click()
    except Exception as e:
        print(e)
        pass
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[text()='Download']").click()
    time.sleep(5)
    driver.quit()
    # driver.close()
    # break
# driver.get('https://finance.yahoo.com')
# element = driver.find_element_by_name('agree').click()
# driver.find_element(by=By.NAME, value='agree').click()
# driver.find_element(by=By.CLASS_NAME, value='Py(5px) W(45px) Fz(s) C($tertiaryColor) Cur(p) Bd Bdc($seperatorColor) Bgc($lv4BgColor) Bdc($linkColor):h Bdrs(3px)').click()

# input_field = driver.find_element(by=By.ID, value='yfin-usr-qry')
# input_field.send_keys('AAPL', Keys.ENTER)
#
# time.sleep(2)

# driver.find_element(By.XPATH, "//span[text()='HISTORICAL_DATA']").click()
# driver.find_element(By.XPATH, "//span[text()='Historical Data']").click()


# time.sleep(2)
# driver.find_element(By.XPATH, "//input[@data-test='date-picker-full-range']").click()

## driver.find_element(by=By.XPATH, value="//li[@data-test='HISTORICAL_DATA']").click()
## driver.find_element(by=By.NAME, value='HISTORICAL_DATA').click()

# element = driver.find_element_by_id('yfin-usr-qry')
# print(element)
