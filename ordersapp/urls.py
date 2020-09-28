from django.conf.urls import url
import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    url(r'^$', ordersapp.OrderList.as_view(), name='zakazes_list'),
    url(r'^order/create/$', ordersapp.OrderItemsCreate.as_view(), name='zakaz_create'),
    url(r'^order/read/(?P<pk>\d+)/$', ordersapp.OrderRead.as_view(), name='zakaz_read'),
    url(r'^order/update/(?P<pk>\d+)/$', ordersapp.OrderItemsUpdate.as_view(), name='zakaz_update'),
    url(r'^order/delete/(?P<pk>\d+)/$', ordersapp.OrderDelete.as_view(), name='zakaz_delete'),

    url(r'^order/forming/complete/(?P<pk>\d+)/$', ordersapp.order_forming_complete, name='zakaz_forming_complete'),

]
