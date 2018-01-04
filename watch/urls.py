from django.urls import path

from .views import *

app_name = 'watch'
urlpatterns = [
    path('profile', ProfilePageView.as_view(), name='profile'),
    path('create', WatchCreateView.as_view(), name='create'),
    path('<str:item_id>', WatchDetailView.as_view(), name='detail'),
    path('<str:item_id>/json', PriceChartJSON.as_view(), name='json')
]
