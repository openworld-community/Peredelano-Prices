import time

from selenium import webdriver
from selenium.webdriver.common.by import By

list_urls_cafe = list()


web = webdriver.Chrome()  # Optional argument, if not specified will search path.


def recurrent_find_link(address, counter):
    web.get(address)
    store_body = web.find_elements(By.XPATH, '//a[@data-test-id="store-item"]')
    for el in store_body:
        list_urls_cafe.append(el.get_attribute("href"))
        counter += 1

    # находим ссылку на следующую страницу

    # Найдите элемент ссылки
    try:
        link_element = web.find_element(By.XPATH, '//a[@rel="next"]')

        # Получите значение ссылки (URL) из атрибута href
        link_url = link_element.get_attribute("href")

        # Выведите значение ссылки в консоль
        if link_url is not None:
            recurrent_find_link(link_url, counter)

    except:
        print(str(counter))


recurrent_find_link("https://glovoapp.com/me/sr/podgorica/restorani_1/", 0)
with open("cafe_urls.txt", mode="w", encoding="utf-8") as file:
    for url in list_urls_cafe:
        file.write(url)
        file.write("\n")

web.quit()