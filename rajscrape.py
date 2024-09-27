from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# Setup the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 60)

# Navigate to the page
val = "https://www.businesstoday.in/mutual-funds/best-mf"
driver.get(val)
wait.until(EC.url_to_be(val))

# Click the filter button
filter_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Filter")]')))
filter_button.click()

# Select "Debt Funds" from the dropdown
debt_funds_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Debt Funds")]')))
debt_funds_option.click()

# Select the "ELSS (Tax Savings)" radio button
elss_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "ELSS (Tax Savings)")]')))

# Scroll into view and click
ActionChains(driver).move_to_element(elss_option).click(elss_option).perform()

# Close the driver
driver.quit()