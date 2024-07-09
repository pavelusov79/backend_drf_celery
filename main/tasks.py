from __future__ import absolute_import, unicode_literals
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from wildberies.celery import app


def import_django_instance():
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wildberies.settings')
    django.setup()


@app.task()
def parse_card(art, user_id):
    import_django_instance()
    from django.contrib.auth.models import User
    from main.models import MyTrackedGoods

    url = f'https://www.wildberries.ru/catalog/{art}/detail.aspx'
    service = Service(executable_path=ChromeDriverManager().install())
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options, service=service)
    try:
        driver.get(url)
        time.sleep(3)
        name = driver.find_element(By.XPATH, '//h1').text.strip()
        brand_name = driver.find_element(By.XPATH, '//a[contains(@class, "product-page__header-brand")]').text
        try:
            el = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//ins[contains(@class, "price-block__final-price")]')))
            price = int(el.get_attribute('innerHTML').strip().replace('&nbsp;', '').replace('₽', ''))
        except Exception:
            price = 0
        try:
            el_1 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="price-block__wallet-price"]')))
            discount_price = int(el_1.get_attribute('innerHTML').strip().replace('&nbsp;', '').replace('₽', ''))
        except Exception:
            discount_price = None

        # print('name = ', name)
        # print('brand_name = ', brand_name)
        # print('price = ', price)
        # print('disc_price = ', discount_price)
        user = User.objects.get(pk=int(user_id))
        # print('user =', user)
        if name and brand_name and price and discount_price:
            data = {'status': 'success', 'data': {
                'name': name,
                'brand_name': brand_name,
                'price': price,
                'discount_price': discount_price
            }}
            print('data= ', data)
            g = MyTrackedGoods(brand_name=brand_name, name=name, price=price, discount_price=discount_price,
                               articul=int(art))
            g.user = user
            g.save()
        elif name and brand_name and price:
            data = {'status': 'success', 'data': {
                'name': name,
                'brand_name': brand_name,
                'price': price,
            }}
            print('data= ', data)
            g = MyTrackedGoods(brand_name=brand_name, name=name, price=price, articul=int(art))
            g.user = user
            g.save()

        driver.quit()

    except Exception as e:
        return {'status': 'error', 'details': e}


# @app.task()
# def add(x, y):
#     return x + y






