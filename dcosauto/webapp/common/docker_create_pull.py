#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2018年3月21日

@author: yangxu
'''
from dockerapi125 import DockerOps



def create_pull(host,port,container_name,data):
    create_result = DockerOps.create(host, port, container_name, data)
    if create_result['code'] == 404:
        image_result = DockerOps.pull(host=host,port=6071,image=data['Image'])
        if image_result.status == 200:
            try:
                image_result.read()
            except Exception as e:
                return {'status':'failure','msg':e}
            else:
                create_result = DockerOps.create(host, port, container_name, data)
            if create_result['code'] == 200:
                return {'status':'success'}
            else:
                return {'status':'failure','msg':create_result['reason']}
        else:
            return {'status':'failure','msg':image_result.read()}
    elif create_result['code'] == 200:
        return {'status':'success'}
    else:
        return {'status':'failure','msg':create_result['reason']}
        
def delete_container(host,port,container_name):
    delete_result = DockerOps.delete(host, port, container_name)
    return delete_result            
                