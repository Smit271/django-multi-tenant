# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connection
from django.db.utils import ProgrammingError

from .models import DbDetails


@receiver(post_save, sender=DbDetails)
def create_tenant_database(sender, instance, created, **kwargs):
    """
    Creates a new PostgreSQL database with the given name.
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("CREATE DATABASE {}".format(instance.name))
        except ProgrammingError:
            # The database already exists
            pass
