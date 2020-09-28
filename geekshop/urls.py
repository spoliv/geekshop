"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
import mainapp.views as mainapp
import authapp.views as authapp

if settings.DEBUG:
    import debug_toolbar

urlpatterns = [
    url(r'^$', mainapp.main, name='index'),
    url(r'^auth/', include('authapp.urls', namespace='auth')),
    url(r'^products/', include('mainapp.urls', namespace='products')),
    url(r'^showroom/', mainapp.showroom, name='showroom'),
    url(r'^contacts/', mainapp.contact, name='contacts'),
    url(r'^basket/', include('basketapp.urls', namespace='basket')),
    url(r'^admin_custom/', include('adminapp.urls', namespace='admin_custom')),
    url(r'^admin/', admin.site.urls),
    #url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^social/', include('social_django.urls', namespace='social')),
    url(r'^zakaz/', include('ordersapp.urls', namespace='zakaz')),

]

if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)