from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import codecs

import re

from webdriver_manager.chrome import ChromeDriverManager


options= Options()
options.add_argument('--allow-running-insecure-content')
options.add_argument('--ignore-certificate-errors')

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
val = "https://www.businesstoday.in/mutual-funds/best-mf"
driver.maximize_window()
wait = (WebDriverWait(driver,60))
driver.get(val)
wait.until(EC.url_to_be(val))

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "flt_btn"))).click()
# filter_button = driver.find_element(By.CLASS_NAME, "flt_btn")
# filter_button.click
filter_option = "ELSS (Tax Savings)"
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='categoryCapsSectionId']/label[1]/span[1]"))).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "flt_btn"))).click()
page_source = driver.page_source    


soup = BeautifulSoup(page_source,features="html.parser")
keyword="fnd_crd_ttl"
matches = soup.find_all(class_=re.compile(keyword))

len_match = len(matches)

title = soup.title.text


file=codecs.open('article_scraping.txt', 'a+')

file.write(title+"\n")

file.write("The following are all instances of your keyword:\n")

count=1

for i in matches:

    file.write(str(count) + "." +  str(i)  + "\n")

    count+=1

file.write("There were "+str(len_match)+" matches found for the keyword.")

file.close()

driver.quit()

