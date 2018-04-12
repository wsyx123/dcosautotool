#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年3月19日

@author: yangxu
'''
from django.shortcuts import render_to_response,HttpResponseRedirect
from webapp.models import platformhosts,platformtemplate
from webapp.forms.install import InstallForm
from webapp.common.dockerapi125 import DockerOps

def install(request):
    if request.method == "POST":
        saveobj = InstallForm(request.POST)
#         if saveobj.save():
        result = saveobj.get_docker_json_data()
        for key,value in result.items():
            name = key.split(':')[0]
            host = key.split(':')[1]
            if name == 'influxdb':
                print DockerOps.create(host, '6071', name, result[key])
            
        return HttpResponseRedirect('/platform/manage/')
    hosts = platformhosts.objects.all()
    templates = platformtemplate.objects.all()
    return render_to_response('platform/install.html',{'hosts':hosts,'templates':templates})