# from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import pickle, time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

clicked = set()
y_last = 1000000000
button_no_light = f'//*[@class="css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-ymttw5 r-1f1sjgu r-o7ynqc r-6416eg r-13qz1uu"]/div[2]/div'
button_light = f'//*[@class="css-1dbjc4n r-1cuuowz r-1loqt21 r-18u37iz r-1ny4l3l r-ymttw5 r-1f1sjgu r-o7ynqc r-6416eg r-13qz1uu"]/div[2]/div'
twited = 'Retweet' # обычный проход Retweeted, в обратную сторону Retweet

browser = webdriver.Chrome()

browser.get(f'https://twitter.com/')
browser.maximize_window()

browser.delete_all_cookies()
with open('cookies', 'rb') as file:
    for cookie in pickle.load(file):
        browser.add_cookie(cookie)
browser.refresh()

browser.get(f'https://twitter.com/63cities')

while True:
    
    #прокрутка вниз
    
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)

        if len(browser.find_elements(By.XPATH, '//div[contains(@class, "r-o52ifk")]')) > 0:
            break

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    

    #удаление верхней плашки
    element = browser.find_element(By.XPATH, '//div[@class="css-1dbjc4n r-aqfbo4 r-gtdqiz r-1gn8etr r-1g40b8q"]')
    browser.execute_script("""
    var element = arguments[0];
    element.parentNode.removeChild(element);
    """, element)

    input()
    time.sleep(1)

    while True:
        try:
            time.sleep(0.1)
            elements = browser.find_elements(By.XPATH, "//div[@class='css-1dbjc4n r-1ta3fxp r-18u37iz r-1wtj0ep r-1s2bzr4 r-1mdbhws']")
            elements.reverse()
            print('new elems ===============', len((elements)))
            check_elms_no_update = True

            for elm in (elements):
                html = elm.get_attribute('outerHTML')

                item_id = html.split('r-1mdbhws" id="')[1].split('"')[0]
                print(item_id)
                
                if item_id not in clicked:
                    clicked.add(item_id)
                    html_button_twit = browser.find_element(By.XPATH, f'//*[@id="{item_id}"]/div[2]/div').get_attribute('outerHTML')
                    if y_last > browser.find_element(By.XPATH, f'//*[@id="{item_id}"]/div[2]').location['y'] or\
                        html_button_twit.split('. ')[1].split('" ')[0] != twited:
                        try:
                            check_elms_no_update = False
                            y_last = browser.find_element(By.XPATH, f'//*[@id="{item_id}"]/div[2]').location['y']
                            h = y_last - 500
                            browser.execute_script(f"window.scrollTo(0, {h})")

                            while html_button_twit.split('. ')[1].split('" ')[0] != twited:
                                time.sleep(0.1)
                                browser.find_element(By.XPATH, f'//*[@id="{item_id}"]/div[2]').click()
                                time.sleep(0.1)
                                try:
                                    browser.find_element(By.XPATH, button_no_light).click()
                                except:
                                    browser.find_element(By.XPATH, button_light).click()
                                html_button_twit = browser.find_element(By.XPATH, f'//*[@id="{item_id}"]/div[2]/div').get_attribute('outerHTML')

                        except Exception as ex:
                            print('item error', ex)
                            browser.execute_script(f"window.scrollTo(0, {h})")
                            time.sleep(0.5)
                            webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
                            time.sleep(0.5)
                            browser.find_element(By.XPATH, f'//*[@id="{item_id}"]/div[2]').click()
                            time.sleep(0.5)
                            try:
                                browser.find_element(By.XPATH, button_no_light).click()
                            except:
                                browser.find_element(By.XPATH, button_light).click()

            if check_elms_no_update:
                #выполняется, если elements не обновляется
                webdriver.ActionChains(browser).send_keys(Keys.PAGE_UP).perform()
                time.sleep(0.2)
                
        except Exception as ex:
            print('err',ex)
            