import json
from django.db.models import F
from core.models import DomainDb, DbDetails
from core.constants import EXTRA_ARGS

def hostname_from_request(request):
    # split on `:` to remove port
    return request.get_host().split(':')[0].lower()


def tenant_db_from_request(request):
    hostname = hostname_from_request(request)
    return hostname


def get_tenant(hostname):
    try:
        domain_db = DomainDb.objects.using('default').get(name=hostname)
        db_obj = DbDetails.objects.using('default').get(id=domain_db.db_id)
    except:
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
