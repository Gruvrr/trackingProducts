import random
import time
import datetime
import undetected_chromedriver
from selenium.webdriver.common.by import By


def get_unit_data(url):
    try:
        driver = undetected_chromedriver.Chrome()
        driver.get(url)
        time.sleep(random.uniform(1.2, 2.5))


        # find articul
        new_articul = ''
        articul = driver.find_element(By.CLASS_NAME, "t12nw7s2_pdp").text
        for i in articul:
            if i.isdigit():
                new_articul += i
        new_articul = int(new_articul)

        # search in stock
        find_div_for_class_name = driver.find_element(By.CLASS_NAME, "p6vr4yt_pdp").text.split()
        arr = []
        fsm = driver.find_element(By.CLASS_NAME, "sy2hk37_pdp").find_elements(By.CLASS_NAME, "sgokg61_pdp")
        fsp = driver.find_element(By.CLASS_NAME, "sy2hk37_pdp").find_elements(By.CLASS_NAME, "s16m0ngq_pdp")
        lst_markets = [i.text for i in fsm]
        lst_stocks = [i.text for i in fsp]
        stock_dict = dict(zip(lst_markets, lst_stocks))
        for key in stock_dict:
            a = stock_dict[key].find(" ")
            arr.append(stock_dict[key][:a])
        mega = int(arr[0])
        orbitalnaya = int(arr[1])
        dovatora = int(arr[2])

        # search price
        for element in range(len(find_div_for_class_name)):
            if find_div_for_class_name[element] == "В" and find_div_for_class_name[element + 1] == 'корзину':
                if find_div_for_class_name[element - 3].isdigit:
                    num1 = find_div_for_class_name[element - 3]
                    num2 = find_div_for_class_name[element - 2]
                    price = str(num1) + str(num2)
                else:
                    price = str(find_div_for_class_name[element - 2])
        global new_price
        new_price = ''
        for i in price:
            if i.isdigit():
                new_price += i
        new_price = int(new_price)

        values = {
            'product_articul': new_articul,
            'product_url': url,
            'product_price': new_price,
            'stock_mega': mega,
            'stock_severniy': orbitalnaya,
            'stock_dovatora': dovatora,
            'last_change_date': datetime.datetime.now(),
        }



    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        time.sleep(2)
        return values