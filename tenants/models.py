from django.db import models


class Tenants(models.Model):
    name = models.CharField(max_length=500)
    sub_domain = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
