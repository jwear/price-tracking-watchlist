from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from celery import chain
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
import random

from .models import Watch, Price
from .views import get_product_from_ebay, get_product_from_amazon


@task
def watch_task():
    random_number = random.randint(-2, 2)
    for watch in Watch.objects.all():
        if watch.service == Watch.AMAZON:
            product_data = get_product_from_amazon(watch.item_id)
            Price.objects.create(product=watch, price=product_data.price_and_currency[0] + random_number)
        elif watch.service == Watch.EBAY:
            product_data = get_product_from_ebay(watch.item_id)
            price = float(product_data['ConvertedCurrentPrice']['value']) + random_number
            Price.objects.create(product=watch, price=price)

@task(ignore_result=True)
def email_task():
    emails = []
    for watch in Watch.objects.all():
        prices = watch.prices.all().order_by('-changed')
        if len(prices) <= 2:
            continue
        if prices[0].price < prices[1].price:
            for user in watch.users.all():
                emails.append((
                    f'{watch.title} - Price Lowered',
                    f'The item you are watching has a lower price of ${prices[0].price}.',
                    'watch@example.com',
                    [user.email],
                ))

    send_mass_mail(emails, fail_silently=False)

@task
def watchman_batch_task():
    chain(watch_task.si(), email_task.si()).apply_async()
