from django.db import models
from django.contrib import admin


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'modified_time', 'created_time']
