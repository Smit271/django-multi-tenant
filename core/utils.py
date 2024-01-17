from core.models import DomainDb, DbDetails


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
