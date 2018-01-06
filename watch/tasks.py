from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User

from .models import Watch, Price
from .views import get_product_from_ebay, get_product_from_amazon


@task
def watch_task():
    for watch in Watch.objects.all():
        if watch.service == Watch.AMAZON:
            product_data = get_product_from_amazon(watch.item_id)
            Price.objects.create(product=watch, price=product_data.price_and_currency[0])
        elif watch.service == Watch.EBAY:
            product_data = get_product_from_ebay(watch.item_id)
            Price.objects.create(product=watch, price=product_data['ConvertedCurrentPrice']['value'])

@task
def email_task():
    emails = []
    for watch in Watch.objects.all():
        prices = watch.prices.all().order_by('-changed')
        if prices[0].price < prices[1].price:
            for user in watch.users.all():
                emails.append((
                    f'{watch.product.title} - Price Lowered',
                    f'The item you are watching has a lower price of ${prices[0].price}.',
                    'watch@example.com',
                    [user.email],
                ))

    send_mass_mail(emails, fail_silently=False)
