import threading

from django.db import connection
from core import utils
from django.conf import settings

DATABASES = settings.DATABASES
THREAD_LOCAL = threading.local()


class TenantMiddleware:
    def __init__(self, get_response):
        print("===== MIDDLEWARE LOADED =====")
        self.get_response = get_response

    def __call__(self, request):
        db = utils.tenant_db_from_request(request)
        print("===> db: ", db)
        setattr(THREAD_LOCAL, "DB", db)
        print("===> THREAD_LOCAL: ", THREAD_LOCAL)
        response = self.get_response(request)
        print("===> response: ", response)
        return response


def get_current_db_name():
    return getattr(THREAD_LOCAL, "DB", None)


def set_db_for_router(db):
    setattr(THREAD_LOCAL, "DB", db)


class MTMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # get hostname
        hostname = request.get_host().split(':')[0].lower()

        # get tenant db_info - just put these tables in cacheops, we dont need to deal with redis explicitly
        db_info = utils.get_tenant(hostname)

        # set db cursor via the database wrapper
        print("===> hostname: ", hostname)
        print("===> db_info: ", db_info)
        print("===> db_info.name: ", db_info.name if db_info is not None else None)

        # ===== Switch the database connection =====
        # connection.close()
        # connection.settings_dict = DATABASES[f'{db_info.name}'] if db_info is not None else DATABASES['default']
        # connection.connect()
        # ==========================================
        print("===> connection.settings_dict: ", connection.settings_dict)
        setattr(THREAD_LOCAL, "DB", db_info.name if db_info else 'default')
        # connection.db_info = db_info if db_info is not None else default_db_info
        response = self.get_response(request)
        print("===> response: ", response)
        return response
