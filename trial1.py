import os
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium

# Assuming ChromeDriver is saved under the directory /path/to/chromedriver
os.environ["PATH"] += os.pathsep + 'C:/Users/aarya/Desktop/chromedriver-win64/chromedriver'

driver = webdriver.Chrome()


driver.get('https://www.businesstoday.in/mutual-funds/best-mf')

time.sleep(5)


#Find the element
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "flt_btn"))).click()
# filter_button = driver.find_element(By.CLASS_NAME, "flt_btn")
# filter_button.click
filter_option = "ELSS (Tax Savings)"
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='categoryCapsSectionId']/label[1]"))).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "flt_btn"))).click()
page_source = driver.page_source    


