from __future__ import absolute_import, unicode_literals
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
    from .models import MyTrackedGoods

    url = f'https://www.wildberries.ru/catalog/{art}/detail.aspx'
    service = Service(executable_path=ChromeDriverManager().install())
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options, service=service)
    try:
        driver.get(url)
        time.sleep(2)
        name = driver.find_element(By.XPATH, '//h1').text.strip()
        brand_name = driver.find_element(By.XPATH,'//a[contains(@class, "product-page__header-brand")]').text
        try:
            price = int(driver.find_element(
                By.XPATH, '//del[contains(@class, "price-block__old-price")]').text.replace(' ', '')[
                        :-1])
        except Exception:
            price = 0
        try:
            discount_price = int(driver.find_element(
                By.XPATH, '//ins[contains(@class, "price-block__final-price")]').text.replace(' ', '')[:-1])
        except Exception:
            discount_price = None

        if name and brand_name and price and discount_price:
            data = {'status': 'success', 'data': {
                'name': name,
                'brand_name': brand_name,
                'price': price,
                'discount_price': discount_price
            }}
            print(data)
            user = User.objects.get(pk=int(user_id))
            g = MyTrackedGoods(brand_name=brand_name, name=name, price=price, discount_price=discount_price,
                               articul=int(art))
            g.user = user
            g.save()

        driver.quit()

    except Exception as e:
        return {'status': 'error', 'details': e}
        

# @app.task()
# def add(x, y):
#     return x + y






