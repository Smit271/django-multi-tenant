import subprocess
import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connection
from django.db.utils import ProgrammingError
from django.conf import settings

from .models import DbDetails
from .utils import create_database_dict


@receiver(post_save, sender=DbDetails)
def create_tenant_database(sender, instance, created, **kwargs):
    """
    Creates a new PostgreSQL database with the given name.
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                "CREATE DATABASE IF NOT EXISTS {}".format(instance.name))
        except ProgrammingError:
            # The database already exists
            print("DB ALREADY EXISTS", instance.name)
            pass

    # CREATING DATABASE DICT IN LOCAL MACHINE TO LOAD DATABASE
    create_database_dict()

    config = open('./database.json',)
    settings.DATABASES.update(json.load(config))

    # Apply migrations to the newly created database
    if created:
        try:
            print(
                "===> connection.settings_dict['NAME']: ", connection.settings_dict['NAME'])
            # Change 'your_app' to the actual name of your app containing migrations
            subprocess.run(["python", "manage.py", "migrate",
                           "--database", instance.name])
        except Exception as e:
            # Handle exceptions if any
            print(f"Error applying migrations for {instance.name}: {e}")
