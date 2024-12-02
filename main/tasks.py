from __future__ import absolute_import, unicode_literals

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
    options.add_argument("--window-size=1920x1080")
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        print('start parsing...')
        name = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//h1'))).text.strip()
        try:
            brand_name = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
                By.XPATH, '//a[contains(@class, "product-page__header-brand")]'))).text
        except Exception:
            brand_name = 'No name'
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

        user = User.objects.get(pk=int(user_id))
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
        driver.quit()

    except Exception as e:
        return {'status': 'error', 'details': e}







