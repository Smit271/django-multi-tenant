from django.contrib import admin
from .models import DbDetails, DomainDb

# Register your models here.
admin.site.register(DbDetails)
admin.site.register(DomainDb)
