#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年3月21日

@author: yangxu
'''

def generatedockerjson(image,cport,hport,env,binds,netmode):
    image = image
    cport = cport
    hport = hport
    env = env
    binds = binds
    netmode = netmode
    
    data = {
      "Image":image,
      "User":"root",
      "Env":env,
      "ExposedPorts":{"{}/tcp".format(cport):{}},
      "HostConfig":{
                   "Binds":binds,
                   "NetworkMode":netmode,
                   "Privileged":True,
                   "RestartPolicy":{
                                   "Name": "always",
                                   "MaximumRetryCount": 0
                                    },
                   "PortBindings":{
                                   "{}/tcp".format(cport):[
                                            {"HostPort":"{}".format(hport)}
                                       ]
                                    },
                   },
          }
    return data