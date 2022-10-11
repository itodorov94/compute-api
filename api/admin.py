from django.contrib import admin
import os

from .models import Request, Result


class RequestAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'get_file_name', 'upload_date']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user_name=request.user)

    def get_file_name(self, obj):
        return os.path.basename(obj.file_name.name)

    get_file_name.short_description = 'File Name'


class ResultAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(request__user_name=request.user)

    list_display = ['get_request', 'result', 'result_date', 'status']

    search_fields = ['result']

    list_filter = ('status', 'result_date',)

    def get_request(self, obj):
        return obj.request.file_name.name

    get_request.short_description = 'Request'


admin.site.register(Request, RequestAdmin)
admin.site.register(Result, ResultAdmin)
