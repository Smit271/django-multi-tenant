from .middlewares import get_current_db_name


class TenantRouter:
    def db_for_read(self, model, **hints):
        print("===> get_current_db_name(): ", get_current_db_name())
        return get_current_db_name()

    def db_for_write(self, model, **hints):
        return get_current_db_name()

    def allow_relation(self, *args, **kwargs):
        return True

    def allow_syncdb(self, *args, **kwargs):
        return None

    def allow_migrate(self, *args, **kwargs):
        print("======== UNDER ALLOW_MIGRATION ========")
        return get_current_db_name()
