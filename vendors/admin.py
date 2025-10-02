from django.contrib import admin
from django.utils.html import format_html
from .models import Vendor, Service, ServiceReminder


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone', 'status', 'active_services_count', 'total_contract_value', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'contact_person', 'email']
    readonly_fields = ['created_at', 'updated_at', 'active_services_count', 'total_contract_value']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'contact_person', 'email', 'phone', 'status')
        }),
        ('Statistics', {
            'fields': ('active_services_count', 'total_contract_value'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'vendor', 'start_date', 'expiry_date', 'payment_due_date', 'amount', 'status', 'status_color_display', 'created_at']
    list_filter = ['status', 'vendor', 'start_date', 'expiry_date', 'payment_due_date']
    search_fields = ['service_name', 'vendor__name']
    readonly_fields = ['created_at', 'updated_at', 'days_until_expiry', 'days_until_payment_due', 'is_expiring_soon', 'is_payment_due_soon', 'is_overdue', 'status_color']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Service Information', {
            'fields': ('vendor', 'service_name', 'start_date', 'expiry_date', 'payment_due_date', 'amount', 'status')
        }),
        ('Status Information', {
            'fields': ('days_until_expiry', 'days_until_payment_due', 'is_expiring_soon', 'is_payment_due_soon', 'is_overdue', 'status_color'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_color_display(self, obj):
        color = obj.status_color
        color_map = {
            'red': '#ff4444',
            'orange': '#ff8800',
            'green': '#44ff44',
            'blue': '#4444ff'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color_map.get(color, '#000000'),
            obj.status.upper()
        )
    status_color_display.short_description = 'Status Color'


@admin.register(ServiceReminder)
class ServiceReminderAdmin(admin.ModelAdmin):
    list_display = ['service', 'reminder_type', 'reminder_date', 'is_sent', 'sent_at', 'created_at']
    list_filter = ['reminder_type', 'is_sent', 'reminder_date', 'created_at']
    search_fields = ['service__service_name', 'service__vendor__name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Reminder Information', {
            'fields': ('service', 'reminder_type', 'reminder_date', 'is_sent', 'sent_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )