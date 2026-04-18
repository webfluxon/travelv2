# app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, VisaPackage, TourPackage, Testimonial, WhyUsItem, Enquiry, ExchangeRate, SiteSettings

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'phone_verified', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'phone_verified')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'phone_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(VisaPackage)
admin.site.register(TourPackage)
admin.site.register(Testimonial)
admin.site.register(WhyUsItem)
admin.site.register(Enquiry)
admin.site.register(ExchangeRate)
admin.site.register(SiteSettings)