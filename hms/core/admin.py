from django.contrib import admin

from .models import Appointment, Doctor, Patient
from django.contrib import admin
from .models import SystemNotification # Import your new model

@admin.register(SystemNotification)
class SystemNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    ordering = ('-created_at',)

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)

