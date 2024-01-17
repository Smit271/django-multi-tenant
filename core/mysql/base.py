from importlib import import_module
import time
import json
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
import django.db.backends.mysql.base
WRAPPED_BACKEND = import_module('django.db.backends.mysql.base')


def lower_dict(d):
    new_dict = dict((k.lower(), v) for k, v in d.items())
    return new_dict


class DatabaseWrapper(WRAPPED_BACKEND.DatabaseWrapper):

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.db_info = None
        # self.default_db_info = None
        self.default_db_info = settings.DATABASES['default']

    def _cursor(self):
        cursor = super(DatabaseWrapper, self)._cursor()

        # create a new db object here and set it to connection and db_name
        conn_params = None
        if self.db_info:
            print('--- using %s db connection ---', self.db_info.name)
            # now init the connection using data from db_info and set it to cursor

            conn_params = {
                'ENGINE': self.db_info.engine,
                'NAME': self.db_info.name,
                'USER': self.db_info.user,
                'PASSWORD': self.db_info.password,
                'HOST': self.db_info.host,
                'PORT': self.db_info.port,
                # 'OPTIONS': json.loads(self.db_info.options)
                'OPTIONS': {},
                'AUTOCOMMIT': False
            }
            self.settings_dict = conn_params
            updated_conn_params = self.get_connection_params()

            connection = self.get_new_connection(updated_conn_params)
            # self.connection = connection
            return connection.cursor()
        else:
            print('--- using default db connection ---')
            return cursor