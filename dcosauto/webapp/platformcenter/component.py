#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年3月18日

@author: yangxu
'''

from django.shortcuts import render_to_response,HttpResponse
from webapp.models import platformcomponent,platformtemplate,platformcluster,platformhosts
from webapp.common.docker_create_pull import create_pull,delete_container
from webapp.forms.component import ComponentForm
import json

def component(request):
    if request.method == 'POST':
        host = request.POST.get('host')
        name = request.POST.get('name')
        componentformobj = ComponentForm(request.POST)
        save_result = componentformobj.save_component()
        if save_result['status']:
            data = componentformobj.generate_docker_json()
            resultmsg = create_pull(host, '6071', name, data)
            if resultmsg['status'] == 'failure':
                platformcomponent.objects.get(name=name).delete()
            return HttpResponse(json.dumps(resultmsg))
        else:
            return HttpResponse(json.dumps({'status':'failure','msg':save_result['msg']}))
    components = platformcomponent.objects.all()
    templates = platformtemplate.objects.values('name')
    clusters = platformcluster.objects.values('name')
    hosts = platformhosts.objects.values('address')
    return render_to_response('platform/component.html',{'components':components,'templates':templates,
                                                         'clusters':clusters,'hosts':hosts})
def component_delete(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        host = request.POST.get('host')
        delete_result = delete_container(host, '6071', name)
        if delete_result['code'] == 204:
            platformcomponent.objects.get(name=name).delete()
            return HttpResponse(json.dumps({'status':'success'}))
        else:
            return HttpResponse(json.dumps({'status':'failure','msg':delete_result['reason']}))
        