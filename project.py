import sys
import transforms

from maltego_trx.handler import handle_run
from maltego_trx.registry import register_transform_classes
from maltego_trx.server import app as application

register_transform_classes(transforms)

if __name__ == '__main__':
    handle_run(__name__, sys.argv, application)
