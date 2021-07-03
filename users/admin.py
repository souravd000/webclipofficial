from django.contrib import admin
from django.db import models
from .models import profile

# Register your models here.




class profileAdmin(admin.ModelAdmin):
    search_fields = ['user__username__icontains',]


admin.site.register(profile, profileAdmin)