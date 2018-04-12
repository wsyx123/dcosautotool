#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年3月21日

@author: yangxu
'''
from webapp.models import platformcluster,platformcomponent,platformhosts,platformtemplate
from dockerjsonformat import generatedockerjson

class ComponentForm(object):
    def __init__(self,data):
        self.data = data
        self.clusterobj = None
        self.name = self.data.get('name')
        self.hostobj = None
        self.netmode = None
        self.image = None
        self.cport = None
        self.hport = None
        self.env = None
        self.volume = None
        self.templateobj = None
        
    def replace_br(self,item):
        return item.replace('\r\n','')
    
    def get_cluster_obj(self):
        self.clusterobj = platformcluster.objects.get(name=self.data.get('cluster'))
    
    def get_host_obj(self):
        self.hostobj = platformhosts.objects.get(address=self.data.get('host'))
        
    def get_template_parameters(self):
        self.templateobj = platformtemplate.objects.get(name=self.data.get('template'))
        self.netmode = self.templateobj.netmode
        self.cport = self.templateobj.cport
        self.hport = self.templateobj.hport
        self.image = self.templateobj.image
        self.env = self.templateobj.env
        self.volume = self.templateobj.volume
    
    def save_component(self):
        try:
            self.get_cluster_obj()
            self.get_host_obj()
            self.get_template_parameters()
        except Exception as e:
            return {'status':False,'msg':e}
        else:
            try:
                platformcomponent.objects.create(cluster=self.clusterobj,template=self.templateobj,
                                             name=self.name,host=self.hostobj,
                                             netmode=self.netmode,image=self.image,
                                             cport=self.cport,hport=self.hport,
                                             env=self.env,volume=self.volume)
            except Exception as e:
                return {'status':False,'msg':e}
            else:
                return {'status':True,'msg':''}
                
    def generate_docker_json(self):
        env = map(self.replace_br, self.env.split(','))
        if env:
            env = []
        volume = map(self.replace_br, self.volume.split(','))
        if volume:
            volume = []
        return generatedockerjson(self.image, self.cport, self.hport, env, volume, self.netmode)
        
        
        
    
    
        