class DbRouter:
    default_db = "default"
    read_only_db = "funds_db"
    read_only_apps = ["funds"]

    def db_for_read(self, model, **hints):
        if model._meta.app_label not in self.read_only_apps:
            return self.default_db
        elif model._meta.app_label in self.read_only_apps:
            return self.read_only_db

    def db_for_write(self, model, **hints):
        if model._meta.app_label not in self.read_only_apps:
            return self.default_db
        return False

    def allow_relation(self, obj1, obj2, **hints):
        app_labels = (obj1._meta.app_label, obj2._meta.app_label)
        if all(app_label not in self.read_only_apps for app_label in app_labels):
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label not in self.read_only_apps:
            return db == self.default_db
        return False
