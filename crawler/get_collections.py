"""
    Get all collections from Muji online store
"""
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("https://www.muji.us/collections/")
assert "MUJI" in driver.title
elem = driver.find_elements(By.TAG_NAME, "a")
print(len(elem))
driver.quit()