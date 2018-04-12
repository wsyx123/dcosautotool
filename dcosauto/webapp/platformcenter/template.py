#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年3月19日

@author: yangxu
'''
from django.shortcuts import render_to_response
from webapp.models import platformtemplate

def template(request):
    templates = platformtemplate.objects.all()
    return render_to_response('platform/template.html',{'templates':templates})