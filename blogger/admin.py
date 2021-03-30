from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Blog)
admin.site.register(models.Post)
admin.site.register(models.Like)
admin.site.register(models.Comment)
admin.site.register(models.View)
admin.site.register(models.Follow)
admin.site.register(models.Complaint)
