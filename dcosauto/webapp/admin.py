# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import platformcluster,platformcomponent,platformtemplate,platformhosts

class PlatformClusterAdmin(admin.ModelAdmin):
    list_display = ('name','version','createtime')
    
class PlatformComponentAdmin(admin.ModelAdmin):
    list_display = ('cluster','name','host','netmode','image',
                    'cport','hport','env','volume','template','status')
    
class PlatformtemplateAdmin(admin.ModelAdmin):
    list_display = ('name','label','type','netmode','image','cport',
                    'hport','env','volume','createtime')
    
class PlatformHostsAdmin(admin.ModelAdmin):
    list_display = ('hostname','address','sversion','dversion','ddriver','ddata','cpu','mem','status')
    

admin.site.register(platformcluster, PlatformClusterAdmin)
admin.site.register(platformcomponent, PlatformComponentAdmin)
admin.site.register(platformtemplate, PlatformtemplateAdmin)
admin.site.register(platformhosts, PlatformHostsAdmin)