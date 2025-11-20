"""
Database router for handling SIS database connections
Place this file in /srv/ribbon2helmsman/helmsman/helmsman/routers.py
"""

class SISRouter:
    """
    A router to control database operations for SIS models.
    Models with app_label 'sis' will use the 'sis' database.
    """
    
    sis_app_labels = {'sis'}  # Add any SIS-related app labels here
    
    def db_for_read(self, model, **hints):
        """
        Attempts to read sis models go to sis database.
        """
        if model._meta.app_label in self.sis_app_labels:
            return 'sis'
        return None
    
    def db_for_write(self, model, **hints):
        """
        Attempts to write sis models go to sis database.
        """
        if model._meta.app_label in self.sis_app_labels:
            return 'sis'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both models are in the same database.
        """
        if (
            obj1._meta.app_label in self.sis_app_labels or
            obj2._meta.app_label in self.sis_app_labels
        ):
            return obj1._meta.app_label == obj2._meta.app_label
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure sis apps only appear in the 'sis' database.
        """
        if app_label in self.sis_app_labels:
            return db == 'sis'
        return None
