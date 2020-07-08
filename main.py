from time import sleep
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options
import pandas as pd


def main():
    data = []
    filename = input("Nazwa pliku excelowego  -->  ")
    if '.xlsx' in filename:
        filename = filename
    else:
        filename = f'{filename}.xlsx'
    column_name = input("Nazwa kolumny w excelu -->  ")
    df = pd.read_excel(filename, sheet_name=0)
    my_list = df[column_name].tolist()

    options = Options()
    options.add_argument('--headless')

    for i in my_list:

        driver = webdriver.Firefox(options=options)

        driver.get('https://allegro.pl/')

        driver.find_element_by_xpath('//button[@data-role="reject-consent"]').click()
        driver.find_element_by_xpath('//input[@type="search"]').send_keys(i)
        driver.find_element_by_xpath('//button[@data-role="search-button"]').click()

        s1 = driver.find_element_by_xpath('//select[@data-value="m"]')
        s_check = driver.find_element_by_xpath('//select[@data-value="m"]/option')
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

    data_frame.to_excel(f'{filename}_output.xlsx')


if __name__ == '__main__':
    main()
