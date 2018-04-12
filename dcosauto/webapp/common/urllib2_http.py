#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2017年11月25日

@author: yangxu
'''
import urllib2
import json

class HttpApi(object):
    def __init__(self,url,*head,**data):
        self.url=url
        self.head=head
        self.data=data
    
    def get(self):
        urlInitObj = urllib2.Request(url=self.url)
        try:
            urlOpenObj = urllib2.urlopen(urlInitObj)
        except:
            return {'code':10060,'reason':'network connection failure'}
        else:
            result = json.loads(urlOpenObj.read())
        return  {'code':200,'reason':result}
    
    def post(self):
        para_data = json.dumps(self.data)
        urlInitObj = urllib2.Request(url=self.url,data=para_data)
        urlOpenObj = urllib2.urlopen(urlInitObj)
        print urlOpenObj
        result = urlOpenObj.read()
        print result
        return json.loads(result)

        
    