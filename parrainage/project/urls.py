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
from django.views.generic import TemplateView

from parrainage.app.views import HomePageView, EluListView, EluDetailView
from parrainage.app.views import EluCSVForMap, EluCSVForMailing, UserDetailView
from parrainage.app.views import DepartmentRankingView, UserRankingView
from parrainage.app.views import DepartmentSynopticView, EluAnswerView
from parrainage.app.views import redirect_by_city_code, PublicAssignation

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^elu/$', EluListView.as_view(), name='elu-list'),
    url(r'^elu/(?P<pk>[0-9]+)/$', EluDetailView.as_view(), name='elu-detail'),
    url(r'^user/(?P<username>[a-z]+)/$', UserDetailView.as_view(),
        name='user-detail'),
    url(r'^csv/$', EluCSVForMap.as_view(), name='elu-csv-for-map'),
    url(r'^csv/mailing/$', EluCSVForMailing.as_view(), name='elu-csv-for-map'),
    url(r'^r/city_code/(?P<city_code>[0-9a-zA-z]+)/$',
        redirect_by_city_code, name='redirect-by-city-code'),
    url(r'r/assign/', PublicAssignation.as_view(), name='assign'),
    url(r'^u/(?P<pk>[0-9]+)/(?P<token>\w+)/$', EluAnswerView.as_view(),
        name='elu-answer'),
    url(r'^stats/ranking/department/$', DepartmentRankingView.as_view(),
        name='department-ranking'),
    url(r'^stats/ranking/user/$', UserRankingView.as_view(),
        name='user-ranking'),
    url(r'^stats/synoptic/department/$', DepartmentSynopticView.as_view(),
        name='department-synoptic'),
    url(r'^infos-legales/',
        TemplateView.as_view(template_name='infos-legales.html'),
        name='infos-legales'),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
]
