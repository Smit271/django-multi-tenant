import json

from django.db.models import F
from django.db import connection
from django.conf import settings

from core.models import DomainDb, DbDetails
from core.constants import EXTRA_ARGS
from .middlewares import set_db_for_router


def hostname_from_request(request):
    # split on `:` to remove port
    return request.get_host().split(':')[0].lower()


def tenant_db_from_request(request):
    hostname = hostname_from_request(request)
    return hostname


def get_tenant(hostname):
    try:
        print("===> settings.DATABASES: ", settings.DATABASES)
        print("===> hostname in get_tenant: ", hostname)
        print("===> connection.settings_dict  in get_tenant: ",
            connection.settings_dict)
        # ===== Switch the database connection =====
        # connection.close()
        # connection.settings_dict = settings.DATABASES['default']
        # connection.connect()
        # ==========================================

        set_db_for_router('default')
        domain_db = DomainDb.objects.using('default').get(name=hostname)
        print("===> domain_db in get_tenant: ", domain_db)
        db_obj = DbDetails.objects.using('default').get(id=domain_db.db_id)
        print("===> db_obj in get_tenant: ", db_obj)
        
        set_db_for_router(db_obj.name)
    except Exception as e:
        set_db_for_router('default')
        print("====> Exception in get_tenant: ", e)
        db_obj = None
    return db_obj


def create_database_dict():
    context = list(DbDetails.objects.all().values(
        ENGINE=F('engine'),
        NAME=F('name'),
        USER=F('user'),
        HOST=F('host'),
        PORT=F('port'),
        PASSWORD=F('password'),
    ))

    # Create a dictionary with database names as keys
    data_context = dict()
    for i in context:
        i.update(EXTRA_ARGS)
        data_context[f'{i["NAME"]}'] = i

    # Print data_context for debugging
    print("===> data_context: ", data_context)
    # file_print = f"DATABASES = {data_context}"

    # Write data_context to a JSON file
    file_path = 'database.json'
    with open(file_path, 'w') as file:
        json.dump(data_context, file, indent=2)

    return data_context
