from __future__ import absolute_import, unicode_literals
import requests
from lxml import html
from wildberies.celery import app


def import_django_instance():
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wildberies.settings')
    django.setup()


@app.task()
def parse_card(art, id):
    import_django_instance()
    from django.contrib.auth.models import User
    from .models import MyTrackedGoods

    url = f'https://www.wildberries.ru/catalog/{art}/detail.aspx?targetUrl=ST'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        dom = html.fromstring(res.text)
        name = dom.xpath('//h1/span/text()')[1]
        brand_name=dom.xpath('//h1/span/text()')[0]
        price = int(dom.xpath('//del[contains(@class, "price-block__old-price")]/text()')[0].replace('\xa0', '')[:-1])
        try:
            discount_price=int(dom.xpath('//span[contains(@class, "price-block__final-price")]/text()')[0].replace('\xa0', '').strip()[:-1])
        except Exception:
            pass
        user = User.objects.get(pk=int(id))
        g = MyTrackedGoods(brand_name=brand_name, name=name, price=price, discount_price=discount_price, articul=int(art))
        g.user = user
        g.save()
        return {'status': 'success'}
        

@app.task()
def add(x, y):
    return x + y






