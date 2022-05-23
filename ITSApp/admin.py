from django.contrib import admin
from .models import Issue, Attachment

class PhotoInline(admin.TabularInline):
    model = Attachment

class PostAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]

admin.site.register(Issue, PostAdmin)
