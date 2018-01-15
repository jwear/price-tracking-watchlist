from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import View
from django.views.generic import DetailView
from urllib.parse import urlparse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from amazon.api import AmazonAPI
from ebaysdk.shopping import Connection as Shopping

from .forms import WatchForm
from .models import Watch, Price
from . import keys

class URLParseError(BaseException):
    pass

def parse_url(url):
    try:
        if 'amazon' and '?pd' in url:
            items = urlparse(url).path.split('/')
            item_id = items[-1]
            return (Watch.AMAZON, item_id)
        if 'amazon' and '?pf' in url:
            items = urlparse(url).path.split('/')
            item_id = items[-1]
            return (Watch.AMAZON, item_id)
        elif 'amazon' in url:
            items = url.split('/')
            for i, v in enumerate(items):
                if v == 'dp':
                    item_id = items[i + 1]
                    return (Watch.AMAZON, item_id)
        elif 'ebay' in url:
            items = urlparse(url).path.split('/')
            item_id = items[-1]
            return (Watch.EBAY, item_id)
        elif 'amazon' not in url and 'ebay' not in url:
            raise URLParseError
    except BaseException:
        raise URLParseError

def get_product_from_amazon(item_id):
    amazon = AmazonAPI(keys.AMAZON_CLIENT_KEY, keys.AMAZON_SECRET_KEY, keys.AMAZON_APP_NAME)
    return amazon.lookup(ItemId=item_id)

def get_product_from_ebay(item_id):
    shopping = Shopping(siteid='EBAY-US', appid=keys.EBAY_APP_ID)
    return shopping.execute('GetSingleItem', {'ItemID': item_id}).dict()['Item']

class WelcomePageView(View):
    form_class = WatchForm
    template_name = 'welcome.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name='dispatch')
class ProfilePageView(View):
    form_class = WatchForm
    template_name = 'watch/profile.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        watches = request.user.watch_set.all()
        return render(request, self.template_name, {'watches': watches, 'form': form})

class WatchCreateView(View):
    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponse(status=405)

        url = request.POST['url']

        try:
            item_id = parse_url(url)
            return JsonResponse({
                'detail_url': reverse('watch:detail', kwargs={'item_id': item_id[1]}) + f'?service={item_id[0]}'
            })
        except URLParseError:
            return HttpResponse(status=400)

class WatchDetailView(View):
    template_name = 'watch/detail.html'

    def create_product(self, request, item_id):
        if request.GET.get('service') == Watch.AMAZON:
            product_data = get_product_from_amazon(item_id)
            product = Watch.objects.create(
                pk=item_id,
                title=product_data.title,
                url=product_data.detail_page_url,
                service=Watch.AMAZON,
                image_url=product_data.medium_image_url,
            )
            Price.objects.create(product=product, price=product_data.price_and_currency[0])
            return product
        elif request.GET.get('service') == Watch.EBAY:
            product_data = get_product_from_ebay(item_id)
            product = Watch.objects.create(
                pk=item_id,
                title=product_data['Title'],
                url=product_data['ViewItemURLForNaturalSearch'],
                service=Watch.EBAY,
                image_url=product_data['PictureURL'][0],
            )
            Price.objects.create(product=product, price=product_data['ConvertedCurrentPrice']['value'])
            return product


    def get(self, request, *args, **kwargs):
        try:
            product = Watch.objects.get(pk=self.kwargs['item_id'])
        except ObjectDoesNotExist:
            product = self.create_product(request, self.kwargs['item_id'])

        is_watched = request.user.watch_set.filter(pk=self.kwargs['item_id']).exists() if request.user.is_authenticated else False
        return render(request, self.template_name, {'product': product, 'is_watched': is_watched})

    @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        model = Watch.objects.get(pk=self.kwargs['item_id'])
        if request.is_ajax():
            request.user.watch_set.add(model)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=402)

    @method_decorator(login_required, name='dispatch')
    def delete(self, request, *args, **kwargs):
        model = Watch.objects.get(pk=self.kwargs['item_id'])
        if request.user.watch_set.filter(pk=self.kwargs['item_id']).exists() and request.is_ajax():
            request.user.watch_set.remove(model)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=402)

class PriceChartJSON(View):
    def get(self, request, *args, **kwargs):
        model = Watch.objects.get(pk=self.kwargs['item_id'])
        prices = list(model.prices.all().values('price', 'changed'))
        return JsonResponse(prices, safe=False)
