from django.contrib import admin
from .models import *
# Register your models here.


class NodeAdmin(admin.ModelAdmin):
    list_display = ('node_name','node_address','node_signer')
    exclude = ['node_signer']
    def save_model(self, request, obj, form, change):
        obj.node_signer = str(request.user)
        obj.save()
class LineAdmin(admin.ModelAdmin):
    exclude = ['line_signer']
    def save_model(self, request, obj, form, change):
        obj.line_signer = str(request.user)
        obj.save()
class DeviceAdmin(admin.ModelAdmin):
    exclude = ['device_signer']
    def save_model(self, request, obj, form, change):
        obj.device_signer = str(request.user)
        obj.save()
class TaskAdmin(admin.ModelAdmin):
    list_display = ['taskname','tasksteps']
admin.site.register(Node,NodeAdmin)
admin.site.register(Line,LineAdmin)
admin.site.register(Device,DeviceAdmin)
admin.site.register(Assets)
admin.site.register(ToolsScript)
admin.site.register(TaskScripts,TaskAdmin)
