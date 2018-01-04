from __future__ import absolute_import, unicode_literals
from celery.decorators import task

from .models import Watch, Price
from .views import get_product_from_ebay, get_product_from_amazon


@task
def watch_task():
    for watch in Watch.objects.all():
        if watch.service == Watch.AMAZON:
            product_data = get_product_from_amazon(watch.item_id)
            Price.objects.create(product=watch, price=product_data.price_and_currency[0],)
        elif watch.service == Watch.EBAY:
            product_data = get_product_from_ebay(watch.item_id)
            Price.objects.create(product=watch, price=product_data['ConvertedCurrentPrice']['value'],)
