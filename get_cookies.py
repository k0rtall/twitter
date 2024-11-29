import pickle
from selenium import webdriver
browser = webdriver.Chrome()

browser.get(f'https://twitter.com/')
browser.delete_all_cookies()
input()
pickle.dump(browser.get_cookies(), open("cookies", "wb"))