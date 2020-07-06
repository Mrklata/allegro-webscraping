from time import sleep
from selenium import webdriver
from selenium.webdriver.support.select import Select
import pandas as pd

basic_df = pd.DataFrame(columns=['Nazwa, Cena'])

filename = input("nazwa pliku excelowego z rozszeżeniem !!!")
column_name = input("nazwa kolumny w excelu")
df = pd.read_excel(filename, sheet_name=0)
my_list = df[column_name].tolist()

for i in my_list:
    driver = webdriver.Firefox()

    driver.get('https://allegro.pl/')

    driver.find_element_by_xpath('//button[@data-role="reject-consent"]').click()
    driver.find_element_by_xpath('//input[@type="search"]').send_keys(i)
    driver.find_element_by_xpath('//button[@data-role="search-button"]').click()

    s1 = driver.find_element_by_xpath('//select[@class="_1h7wt _k70df _7qjq4 _27496_3VqWr"]')
    s_check = driver.find_element_by_xpath('//select[@class="_1h7wt _k70df _7qjq4 _27496_3VqWr"]/option')
    s2 = Select(s1)
    s2.select_by_index(1)

    count = 1
    for _ in range(10):
        if s_check.text == ' cena: od najniższej ':
            break
        elif count == 10:
            print('Timeout error')
        else:
            sleep(1)

    prices = driver.find_elements_by_xpath('//span[@class="_9c44d_1zemI"]')

    prices_lst = []
    for num in range(10):
        prices_lst.append(prices[num].text)

    prices_int = []
    for price in prices_lst:
        prices_int.append(float(price.replace(" zł", "").replace(",", ".")))

    print(sorted(prices_int))
