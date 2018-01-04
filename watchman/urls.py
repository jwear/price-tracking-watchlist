from django.contrib import admin
from django.urls import include, path

from watch.views import WelcomePageView
urlpatterns = [
    path('', WelcomePageView.as_view(), name='welcome'),
    path('admin/', admin.site.urls),
    path('watch/', include('watch.urls', namespace='watch')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]
