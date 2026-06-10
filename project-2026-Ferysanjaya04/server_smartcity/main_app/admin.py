from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('title', 'category')
        }),
        ('Detail', {
            'fields': ('description', 'location')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Waktu', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
