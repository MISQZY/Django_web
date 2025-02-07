from django.contrib import admin
from django.core.management import call_command
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from django.utils.html import format_html

from .models import *

class InboundAdmin(admin.ModelAdmin):
    list_display = ('id', 'remark', 'protocol', 'enable')
    list_filter = ('enable',)
    search_fields = ('remark',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('email','enable', 'method', 'total_gb')
    list_filter = ('enable',)
    search_fields = ('email',)

    
admin.site.register(Inbound, InboundAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(UserClient)
admin.site.register(Settings)
admin.site.register(StreamSettings)
admin.site.register(Sniffing)

