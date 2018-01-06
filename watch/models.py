from django.db import models

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
    image_url = models.URLField()
    service = models.CharField(
        max_length=3,
        choices=SERVICE_CHOICES,
    )

    users = models.ManyToManyField('auth.User')

class Price(models.Model):
    price = models.FloatField()
    changed = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey(
        'watch.Watch',
        on_delete=models.CASCADE,
        related_name='prices'
    )
