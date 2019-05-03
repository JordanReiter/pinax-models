from django.db import models, router
from django.utils import timezone
from django.conf import settings

from . import managers
from .utils import get_related_objects


DELETE_RELATED_OBJECTS = getattr(settings, 'LOGICALDELETE_DELETE_RELATED_OBJECTS', True)

class LogicalDeleteMixin(models.Model):
    def active(self):
        return self.date_removed is None
    active.boolean = True

    def delete(self):
        # Fetch related models
        if DELETE_RELATED_OBJECTS:
            using = router.db_for_write(self.__class__, instance=self)
            to_delete = get_related_objects(self, using)

            for obj in to_delete:
                obj.delete()

        # Soft delete the object
        self.date_removed = timezone.now()
        self.save()

    class Meta:
        abstract = True


class LogicalDeleteModel(LogicalDeleteMixin, models.Model):
    """
    This base model provides date fields and functionality to enable logical
    delete functionality in derived models.
    """
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)
    date_removed = models.DateTimeField(null=True, blank=True)

    objects = managers.LogicalDeletedManager()

    class Meta:
        abstract = True
