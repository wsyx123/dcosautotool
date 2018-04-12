# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
import json

from webapp.models import platformcluster,platformcomponent,platformtemplate,platformhosts

# Create your views here.
def index(request):
    clusters = platformcluster.objects.all().count()
    hosts = platformhosts.objects.all().count()
    components = platformcomponent.objects.all().count()
    templates = platformtemplate.objects.all().count()
    return render_to_response("dashboard/dashboard.html",{'clusters':clusters,
                                                          'hosts':hosts,
                                                          'components':components,
                                                          'templates':templates})

def manage(request):
    return render_to_response("system/system.html",)
