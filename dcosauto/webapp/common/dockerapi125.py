#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2017年11月15日

@author: yangxu
'''
from types import  DictType
import httplib
'''
urllib2可以接受一个Request类的实例来设置URL请求的headers，urllib仅可以接受URL。这意味着，你不可以伪装你的User Agent字符串等。
urllib提供urlencode方法用来GET查询字符串的产生，而urllib2没有。这是为何urllib常和urllib2一起使用的原因。
'''
import urllib2
import json
import logging
from django.utils import six  #django 迭代器
from urllib2_http import HttpApi
import httplibapi


class DockerAPIDispatch(object):
    
    method_list_name=['list','create','start','restart','delete','status']
    
    def __init__(self,**kwargs):
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)
        
    @classmethod
    def dispatch(cls,host,port,method,container_name=None,data=None,alls=False):
        self = cls()
        if method in cls.method_list_name and hasattr(DockerOps, method):
            if self.isCreate(method):
                if self.isJson(data):
                    func = getattr(DockerOps, method)
                    return func(host,port,container_name,data)
                return logging.warning('wish you give the dict data')
            else:
                func = getattr(DockerOps, method)
                return func(host,port,container_name,alls)
        else:
            self.http_method_not_allowed(method)       
       
    def http_method_not_allowed(self,method):
        return logging.warning('Method Not Allowed: %s', method)
    
    def isJson(self,data):
        if type(data) is DictType:
            return True
        else:
            return False
        
    def isCreate(self,method):
        if method == 'create':
            return True
        else:
            return False   

class DockerOps(object):
    def __init__(self):
        pass
    
    @classmethod    
    def list(cls,host,port,alls):
        self=cls()
        if alls:
            baseurl='http://'+host+':'+port+'/containers/json?all=true'
        
        else:
            baseurl='http://'+host+':'+port+'/containers/json'
        http_api_obj = HttpApi(baseurl)
        return http_api_obj.get()   
    @classmethod    
    def create(cls,host,port,container_name,data):
        self=cls()
        if container_name:
            url_context = '/containers/create?name='+container_name
            data = json.dumps(data)
            con = httplib.HTTPConnection(host,port)
            try:
                con.request("POST",url_context,data,{"Content-type":"application/json"})
            except:
                return {'code':10060,'reason':'network connection failure'}
            httpres = con.getresponse()
            if httpres.reason == 'Created' and httpres.status == 201:
                if cls.start(host, port,container_name=container_name):
                    return {'code':200,'reason':'create and start {} container success'.format(container_name)}
            else:
                return {'code':httpres.status,'reason':httpres.read()}
        else:
            url_context = '/containers/create'
            data = json.dumps(data)
            con = httplib.HTTPConnection(host,port)
            con.request("POST",url_context,data,{"Content-type":"application/json"})
            httpres = con.getresponse()
            if httpres.reason == 'Created' and httpres.status == 201:
                container_id = json.loads(httpres.read())['Id'][0:12]
                if cls.start(host, port,container_id=container_id): # return True
                    return {'code':200,'reason':'start success'}
            else:
                return {'code':httpres.status,'reason':httpres.read()}
    
    @classmethod
    def delete(cls,host,port,container_name,alls=None):
        self=cls()
        if container_name:
            container_result = self.get_container_id(host,port,container_name)
            if container_result['code'] == 200:
                container_id = container_result['reason']
                url_context = '/containers/'+container_id+'?force=true'
            else:
                return container_result
        else:
            return {'code':404,'reason':'container name is ?'}
        try:
            con = httplib.HTTPConnection(host,port)
            con.request('DELETE', url_context)
            httpres = con.getresponse()
        except Exception as e:
            return {'code':httpres.status,'reason':e}
        return {'code':httpres.status,'reason':httpres.read()}
        
    @classmethod
    def stop(cls,host,port,container_name,alls=None):
        self=cls()
        if container_name:
            container_id = self.get_container_id(host,port,container_name)
            url_context = '/containers/'+container_id+'/stop'
        else:
            return False
        try:
            con1 = httplib.HTTPConnection(host,port)
            con1.request('POST', url_context)
            con1.close()
        except:
            return False
        return True
        
    @classmethod    
    def start(cls,host,port,portbind=None,container_name=None,container_id=None,alls=None):
        self=cls()
        #if portbind:
        #    data = json.dumps(portbind)
        #else:
        data = 'test'
        if container_name:
            container_id = self.get_container_id(host,port,container_name)
            container_id = container_id['reason']
            baseurl='http://'+host+':'+port+'/containers/'+container_id+'/start'
        elif container_id:
            baseurl='http://'+host+':'+port+'/containers/'+container_id+'/start'
        try:
            urlInitObj = urllib2.Request(url=baseurl,data=data)
            urlOpenObj = urllib2.urlopen(urlInitObj)
            urlOpenObj.read()
        except:
            return False
        return "True"
    
    @classmethod
    def restart(cls,host,port,container_name,alls=None):
        self=cls()
        if container_name:
            container_id = self.get_container_id(host,port,container_name)
            baseurl='http://'+host+':'+port+'/containers/'+container_id+'/restart'
        else:
            return False
        try:
            urlInitObj = urllib2.Request(url=baseurl,data="test")
            urlOpenObj = urllib2.urlopen(urlInitObj)
            urlOpenObj.read()
        except:
            return False
        return "True"
    
    def get_container_id(self,host,port,container_name):
        result = self.list(host, port,alls=True)
        if result['code'] == 200:
            for containter in result['reason']:
                if container_name == str(containter["Names"])[4:-2]:
                    return {'code':200,'reason':containter["Id"][0:12]}
        else:
            return result 
    @classmethod        
    def status(cls,host,port,container_name,alls):
        status_result = cls.list(host,port,container_name, alls=False)
        return status_result["State"]["Status"]
    
    @classmethod    
    def getarchive(cls,host,port,container_name,filename):
        self=cls()
        if container_name:
            container_id = self.get_container_id(host,port,container_name)
            url_context='/containers/'+container_id+'/archive?path='+filename
        else:
            return False
        try:
            result = httplibapi.get(host, port, url_context)
        except:
            return False
        return result
    
    @classmethod
    def uploadtarfile(cls,host,port,container_name,uploadpath,filename):
        with open(filename) as f:
            data=f.read()
        self=cls()
        if container_name:
            container_id = self.get_container_id(host,port,container_name)
            url_context='/containers/'+container_id+'/archive?path='+uploadpath
        else:
            return False
        httplibapi.put(host, port, url_context, body=data)
    
    @classmethod    
    def executecmd(cls,host,port,container_name,cmds):
        self = cls()
        headers = {"Content-Type":" application/json"}
        datas = {
                 "Cmd":cmds
                 }
        datas = json.dumps(datas)
        container_id = self.get_container_id(host,port,container_name)
        url_context='/containers/'+container_id+'/exec'
        
        result = httplibapi.post(host, port, url_context, body=datas, headers=headers)
        result_id = json.loads(result)['Id']
        
        url_context = '/exec/'+result_id+'/start'
        data = {
	       "Detach": False,
	       "Tty": False
	}
        data = json.dumps(data)
        return httplibapi.post(host,port,url_context,body=data,headers=headers)
    
    @classmethod    
    def pull(cls,host=None,port=None,image=None):
        imagelist = image.split(":")
        if len(imagelist) == 3:
            imagename = imagelist[0]+':'+imagelist[1]
            imagetag = imagelist[2]
        if len(imagelist) == 2:
            imagename = imagelist[0]
            imagetag = imagelist[1]
        url_context = '/images/create?fromImage='+imagename+'&tag='+imagetag
        if port:
            port = port
        else:
            port = 6071
        con = httplib.HTTPConnection(host,port)
        con.request("POST",url_context,'',{"Content-type":"application/json"})
        httpres = con.getresponse()
        return httpres   
