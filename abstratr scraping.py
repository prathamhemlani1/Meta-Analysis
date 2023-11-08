from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Specify the path to chromedriver using a Service object
s = Service(r'C:\Users\Hemlani\Documents\Research Position\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get('http://abstrackr.cebm.brown.edu/account/login')

username_field = driver.find_element(By.ID, 'login')
password_field = driver.find_element(By.ID, 'password')
login_button = driver.find_element(By.ID, 'submit')

username_field.send_keys('phemlani1')
password_field.send_keys('DXMeCgH#RjwA3wP')

login_button.click()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'login-header'))
)

project_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'screen/53929')]"))
)
project_link.click()
