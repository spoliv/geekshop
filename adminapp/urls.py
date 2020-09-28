from django.conf.urls import url

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    #url(r'^users/create/$', adminapp.user_create, name='user_create'),
    url(r'^users/create/$', adminapp.ShopUserCreateView.as_view(), name='user_create'),
    #url(r'^users/read/$', adminapp.users, name='users'),
    url(r'^users/read/$', adminapp.ShopUserListView.as_view(), name='users'),
    #url(r'^users/update/(?P<pk>\d+)/$', adminapp.user_update, name='user_update'),
    url(r'^users/update/(?P<pk>\d+)/$', adminapp.ShopUserUpdateView.as_view(), name='user_update'),
    #url(r'^users/delete/(?P<pk>\d+)/$', adminapp.user_delete, name='user_delete'),
    url(r'^users/delete/(?P<pk>\d+)/$', adminapp.ShopUserDeleteView.as_view(), name='user_delete'),
    url(r'^categories/create/$', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    url(r'^categories/read/$', adminapp.ProductCategoryListView.as_view(), name='categories'),
    #url(r'^categories/read/$', adminapp.ProductCategoryListView.as_view(), name='admin_custom'),
    url(r'^categories/update/(?P<pk>\d+)/$', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    url(r'^categories/delete/(?P<pk>\d+)/$', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),
    url(r'^products/create/category/(?P<pk>\d+)/$', adminapp.ProductCreateView.as_view(), name='product_create'),
    url(r'^products/read/category/(?P<pk>\d+)/$', adminapp.ProductListView.as_view(), name='products'),
    url(r'^products/read/(?P<pk>\d+)/$', adminapp.ProductDetailView.as_view(), name='product_read'),
    url(r'^products/update/(?P<pk>\d+)/$', adminapp.ProductUpdateView.as_view(), name='product_update'),
    #url(r'^products/update/(?P<pk>\d+)/$', adminapp.ProductUpdateView.as_view(), name='admin_custom'),
    # url(r'^products/delete/(?P<pk>\d+)/$', adminapp.ProductDeleteView.as_view(), name='product_delete'),
    url(r'^products/delete/(?P<pk>\d+)/$', adminapp.product_delete, name='product_delete'),
]