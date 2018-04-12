#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年3月20日

@author: yangxu
'''

from webapp.models import platformcluster,platformcomponent,platformhosts,platformtemplate
from dockerjsonformat import generatedockerjson

class InstallForm(object):
    def __init__(self,data):
        self.data = data
        self.cluster = self.data.get('name')
        self.cluster_items = ['name','version']
        self.common_items = ['name','type','netmode','host','image','cport','hport','env','volume']
        self.dockerjson = {}
    
    def get_host_obj(self,host):
        return platformhosts.objects.get(address=host)
    
    def prefix_map(self,prefix):
        prefix_map_dict = {'my':'mysql','re':'redis','in':'influxdb','ra':'rabbitmq',
                           'do1':'dockbox','do2':'dockbox_celery','do3':'dockbox_flower',
                           'do4':'dockbox_task','ic':'icloud','ed':'edgebox'}
        return prefix_map_dict[prefix]
    
    def cluster_save(self):
        modelobj = platformcluster()
        for item in self.cluster_items:
            value = self.data.get(item)
            setattr(modelobj, item, value)
        try:
            modelobj.save()
        except Exception as e:
            print e
            return False
        return True
    
    def common_save(self,clusterobj,prefix):
        modelobj = platformcomponent()
        for item in self.common_items:
            if item == 'host':
                value = self.get_host_obj(self.data.get(prefix+item))
            elif item == 'type':
                value == self.prefix_map(prefix)
            else:
                value = self.data.get(prefix+item)
            if not value:
                value = 'null'
            setattr(modelobj, item, value)
        setattr(modelobj, 'cluster', platformcluster.objects.get(name=self.cluster))
        modelobj.save()
    
    def replacebr(self,item):
        return item.replace('\r\n','')
    
    def generate_docker_json_data(self,prefix):
        key = self.data.get(prefix+'name')+':'+self.get_host_obj(self.data.get(prefix+'host')).address
        if prefix[0:2] == 'do':
            env = (platformtemplate.objects.get(type=self.prefix_map(prefix)).env).split(',')
            env = map(self.replacebr, env)
            binds = (platformtemplate.objects.get(type=self.prefix_map(prefix)).volume).split(',')
            binds = map(self.replacebr, binds)
        else:
            binds = self.data.get(prefix+'volume').split(',')
            env = self.data.get(prefix+'env').split(',')
        image = self.data.get(prefix+'image')
        cport = self.data.get(prefix+'cport')
        hport = self.data.get(prefix+'hport')
        netmode = self.data.get(prefix+'netmode')
        value = generatedockerjson(image, cport, hport, env, binds, netmode)
        self.dockerjson[key]= value
        
    def get_docker_json_data(self):
        prefix_list = ['my','re','in','ra','do1','do2','do3','do4','ic','ed']
        for prefix in prefix_list:
            self.generate_docker_json_data(prefix)
        return self.dockerjson
            
    def save(self):
        clusterobj = self.cluster_save()
        if clusterobj:
            prefix_list = ['my','re','in','ra','do1','do2','do3','do4','ic','ed']
            for prefix in prefix_list:
                try:
                    self.common_save(clusterobj,prefix)
                except Exception as e:
                    print e
                    return False
            return True
        return False    
    
        
    
    
