from time import sleep
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options
import pandas as pd

data = []
filename = input("Nazwa pliku excelowego bez rozszerzenia !!! -->  ")
column_name = input("Nazwa kolumny w excelu -->  ")
filename = f'{filename}.xlsx'
df = pd.read_excel(filename, sheet_name=0)
my_list = df[column_name].tolist()

for i in my_list:
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    driver.get('https://allegro.pl/')

    driver.find_element_by_xpath('//button[@data-role="reject-consent"]').click()
    driver.find_element_by_xpath('//input[@type="search"]').send_keys(i)
    driver.find_element_by_xpath('//button[@data-role="search-button"]').click()

    s1 = driver.find_element_by_xpath('//select[@class="_1h7wt _k70df _7qjq4 _27496_3VqWr"]')
    s_check = driver.find_element_by_xpath('//select[@class="_1h7wt _k70df _7qjq4 _27496_3VqWr"]/option')
    s2 = Select(s1)
    s2.select_by_index(1)
    span_check = driver.find_element_by_xpath('//span[.="nowe"]').click()
    count = 1
    for _ in range(10):
        if s_check.text == ' cena: od najniższej ' and span_check.text == 'nowe':
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
        if price != '':
            prices_int.append(float(price.replace(" zł", "").replace(",", ".").replace(' ', '')))
        else:
            continue
    data.append([i, sorted(prices_int)[0], sorted(prices_int)[1], sorted(prices_int)[2]])
    print([i, sorted(prices_int)[0], sorted(prices_int)[1], sorted(prices_int)[2]])

    driver.quit()

data_frame = pd.DataFrame(data, columns=['Nazwa', 'Cena 1', 'Cena 2', 'Cena 3'])

data_frame.to_excel('output.xlsx')
