"""parrainage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from parrainage.app.views import HomePageView, EluListView, EluDetailView
from parrainage.app.views import EluCSVForMap, UserDetailView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^elu/$', EluListView.as_view(), name='elu-list'),
    url(r'^elu/(?P<pk>[0-9]+)/$', EluDetailView.as_view(), name='elu-detail'),
    url(r'^user/(?P<username>[a-z]+)/$', UserDetailView.as_view(),
        name='user-detail'),
    url(r'^csv/$', EluCSVForMap.as_view(), name='elu-csv-for-map'),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
]
