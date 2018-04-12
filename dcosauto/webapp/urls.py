"""devops_ci URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from views import index,manage
from platformcenter.component import component,component_delete
from platformcenter.template import template
from platformcenter.install import install
from platformcenter.log import log
admin.autodiscover()

urlpatterns = [
    url(r'^admin/',include(admin.site.urls)),
    url(r'^$',index),
    url(r'^index/$',index,name='index'),
    url(r'^manage/$',manage),
    url(r'^platform/manage/$',component),
    url(r'^platform/manage/delete/$',component_delete),
    url(r'^platform/template/$',template),
    url(r'^platform/install/$',install),
    url(r'^platform/log/$',log),
]
