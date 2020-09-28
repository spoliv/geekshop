from django.conf.urls import url
import mainapp.views as mainapp
from django.urls import path

app_name = 'mainapp'


urlpatterns = [
    url('^$', mainapp.products, name='products'),
    url(r'^(?P<pk>\d+)/$', mainapp.product, name='product'),
    url(r'^category/(?P<pk>\d+)/page/(?P<page>\d+)/$', mainapp.products, name='page'),
    #path('category/<int:pk>/page/<int:page>/', mainapp.products, name='page'),
    url(r'^category/(?P<pk>\d+)/$', mainapp.products, name='category'),
]

