# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class platformhosts(models.Model):
    hostname = models.CharField(max_length=32,null=True,blank=True,verbose_name='主机名')
    address = models.CharField(max_length=32,verbose_name='IP地址')
    sversion = models.CharField(max_length=32,null=True,blank=True,verbose_name='系统版本')
    dversion = models.CharField(max_length=32,null=True,blank=True,verbose_name='docker版本')
    ddriver = models.CharField(max_length=32,null=True,blank=True,verbose_name='docker存储驱动')
    ddata = models.CharField(max_length=32,null=True,blank=True,verbose_name='docker存储目录')
    cpu = models.CharField(max_length=32,null=True,blank=True,verbose_name='CPU')
    mem = models.CharField(max_length=32,null=True,blank=True,verbose_name='内存')
    status = models.CharField(max_length=10,default='down',verbose_name='CPU')
    
    def __unicode__(self):
        return '%s' %(self.address)


class platformcluster(models.Model):
    name = models.CharField(max_length=32,unique=True,verbose_name='集群名')
    version = models.CharField(max_length=32,verbose_name='版本')
    createtime = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    
    
    def __unicode__(self):
        return '%s' %(self.name)   

    
class platformtemplate(models.Model):
    name =  models.CharField(max_length=20,unique=True,verbose_name='模版名')
    label = models.CharField(max_length=64,verbose_name='说明')
    type = models.CharField(max_length=20,verbose_name='模版类型')
    image = models.CharField(max_length=255,verbose_name='镜像名')
    netmode = models.CharField(max_length=32,verbose_name='网络模式')
    cport = models.CharField(max_length=10,verbose_name='容器端口')
    hport = models.CharField(max_length=10,verbose_name='主机端口')
    env  = models.TextField(null=True,blank=True,verbose_name='环境变量')
    volume = models.TextField(max_length=512,null=True,blank=True,verbose_name='卷映射')
    dockerfile = models.TextField(null=True,blank=True)
    createtime = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    
    def __unicode__(self):
        return '%s' %(self.name)

class platformcomponent(models.Model):
    cluster = models.ForeignKey('platformcluster',verbose_name='集群')
    template = models.ForeignKey('platformtemplate',verbose_name='模版')
    name = models.CharField(max_length=20,unique=True,verbose_name='容器名')
    host = models.ForeignKey('platformhosts',verbose_name='主机IP')
    netmode = models.CharField(max_length=32,verbose_name='网络模式')
    image = models.CharField(max_length=255,verbose_name='镜像名')
    cport = models.CharField(max_length=10,verbose_name='容器端口')
    hport = models.CharField(max_length=10,verbose_name='主机端口')
    env  = models.CharField(max_length=512,null=True,blank=True,verbose_name='环境变量')
    volume = models.CharField(max_length=512,null=True,blank=True,verbose_name='卷映射')
    createtime = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    status = models.CharField(max_length=5,default='up',verbose_name='状态')
    
    def __unicode__(self):
        return '%s' %(self.name)
