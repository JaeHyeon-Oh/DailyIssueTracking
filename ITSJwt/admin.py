from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'is_staff')
    list_filter=('is_active', 'is_staff', 'is_superuser')
    search_fields = ('name',)
    fields=['username','email','is_staff','is_active','name','picture']


