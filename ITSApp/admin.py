from django.contrib import admin
from .models import Issue, Attachment,Project

class PhotoInline(admin.TabularInline):
    model = Attachment

class PostAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]

admin.site.register(Issue, PostAdmin)
admin.site.register(Project)
