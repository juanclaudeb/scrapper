#!/usr/bin/python
from multiprocessing.connection import wait
import requests
import pandas as pd
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from webdriver_manager.chrome import ChromeDriverManager
from sys import platform

options = Options()

if platform == "darwin":
    # OS X
    os.environ['WDM_LOCAL'] = '0'
elif platform == "win32":
    # Windows...
    os.environ['WDM_LOCAL'] = '1'

# Enable headless mode below:
#options.headless = True

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("https://www.bidorbuy.co.za/")

# create action chain object
action = ActionChains(driver)

time.sleep(10)
action.send_keys(Keys.ESCAPE).perform()

signInLink = driver.find_element_by_xpath("//div[@id='signedoutLinkContainer']/a[@href='https://www.bidorbuy.co.za/jsp/login/UserLogin.jsp?loginTargetURL=https%3A%2F%2Fwww.bidorbuy.co.za']")
signInLink.click()
usernameElement = driver.find_element_by_xpath("/html//input[@id='username']")
usernameElement.clear()
usernameElement.send_keys('insert-username-here')
passwordElement = driver.find_element_by_xpath("/html//input[@id='password']")
passwordElement.clear()
passwordElement.send_keys('insert-password-here')
signInButton = driver.find_element_by_xpath("//form[@id='Login']/button[@type='submit']")
signInButton.click()
bidOrBuyElement = driver.find_element_by_xpath('/html/body//nav[@class=\'main-nav\']//div[@class=\'mybidorbuy-info\']') 
action.move_to_element(bidOrBuyElement).perform()
mySalesElement = driver.find_element_by_xpath('/html/body//nav[@class=\'main-nav\']//div[@class=\'mybidorbuy-menu-scrollable-y-div\']/div[5]/a[@href=\'https://www.bidorbuy.co.za/jsp/seller/sales/Sales.jsp\']')
mySalesElement.click()

time.sleep(5)

page = requests.get(driver.current_url)

soup = BeautifulSoup(page.content, "html.parser")

filteredResult = soup.find_all("div", class_="main-content")

print(filteredResult)

# empty list
data = []
list_header = []

for items in filteredResult:
    try:
        list_header.append(items.get_text())
    except:
        continue

# for getting the data 
for element in filteredResult:
    sub_data = []
    for sub_element in element:
        try:
            sub_data.append(sub_element.get_text())
        except:
            continue
    data.append(sub_data)

# Storing the data into Pandas
# DataFrame 
dataFrame = pd.DataFrame(data = data, columns = ['NA', 'Columns', 'NA', 'Sales Data', 'NA', 'NA', 'NA'])
#dataFrame = pd.DataFrame(data = data, columns = ['NA', 'Columns', 'NA'])

if platform == "darwin":
    # OS X
    # Converting Pandas DataFrame
    # into CSV file
    dataFrame.to_csv(os.path.expanduser('~')+'/Downloads/paymentsfile.csv')
elif platform == "win32":
    # Windows...
    dataFrame.to_csv(os.path.expanduser('~')+'\Downloads\paymentsfile.csv')

driver.quit()