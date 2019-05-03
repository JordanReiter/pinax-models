import pkg_resources

__version__ = pkg_resources.get_distribution("pinax-models").version

from .admin import LogicalDeleteModelAdmin  # noqa
from .models import LogicalDeleteModel  # noqa
