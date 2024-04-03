from dynamic_db_router import DynamicDbRouter
from dynamic_db_router.router import THREAD_LOCAL

class ApiRouter(object):
    """
    A router to control all database operations on models in the
    general_auth application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'app_versat':
            return 'app_versat'
        else:
            return 'default'

    # def db_for_write(self, model, **hints):
    #     if model._meta.app_label == 'app_versat':
    #         return 'app_versat'
    #     else:
    #         return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'app_versat' :
            return False
        else:
            return True


class ApiDynamicDbRouter(DynamicDbRouter):
    """A router that decides what db to read from based on a variable
    local to the current thread.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'app_versat':
            return getattr(THREAD_LOCAL, 'DB_FOR_READ_OVERRIDE', ['default'])[-1]
        else:
            return 'default'


    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'app_versat':
            return getattr(THREAD_LOCAL, 'DB_FOR_WRITE_OVERRIDE', ['default'])[-1]
        else:
            return 'default'

    def allow_relation(self, *args, **kwargs):
        return None

    def allow_syncdb(self, *args, **kwargs):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'app_versat':
            return False
        else:
            return True
