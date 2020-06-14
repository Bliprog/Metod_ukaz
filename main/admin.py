from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *
# Register your models here.
class ManagerInline(admin.StackedInline):
    model = Manager
    can_delete = False
    verbose_name_plural = 'Менеджеры'

class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'Клиенты'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ClientInline, ManagerInline)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email','first_name','last_name'),
        }),
    )
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    pass

@admin.register(GPU)
class GPUAdmin(admin.ModelAdmin):
    pass

@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Orders_products)
class OrderProductsAdmin(admin.ModelAdmin):
    pass
