from django.contrib import admin
from .models import UserLoginHistory
from django.http import HttpResponse
import csv


def download_csv(modeladmin, request, queryset):
    """Action to download data as csv"""

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=export_logs.csv"

    keys = ['user_id', 'ip_address']
    writer = csv.writer(response)
    writer.writerow(keys)
    for obj in queryset:
        writer.writerow([obj.user_id, obj.ip_addr])

    return response


@admin.register(UserLoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'ip_addr')
    actions = [download_csv]
