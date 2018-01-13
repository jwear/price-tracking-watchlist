from django.db import models
from django.db.models import Max, Min

class Watch(models.Model):
    AMAZON = 'amz'
    EBAY = 'eby'
    SERVICE_CHOICES = (
        (AMAZON, 'Amazon'),
        (EBAY, 'eBay'),
    )

    url = models.URLField()
    item_id = models.CharField(max_length=256, primary_key=True)
    title = models.CharField(max_length=512)
    image_url = models.URLField(blank=True, null=True)
    service = models.CharField(
        max_length=3,
        choices=SERVICE_CHOICES,
    )

    users = models.ManyToManyField('auth.User')

    @property
    def lowest_price(self):
        return self.prices.aggregate(Min('price'))['price__min']

    @property
    def highest_price(self):
        return self.prices.aggregate(Max('price'))['price__max']

class Price(models.Model):
    price = models.FloatField()
    changed = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey(
        'watch.Watch',
        on_delete=models.CASCADE,
        related_name='prices'
    )
