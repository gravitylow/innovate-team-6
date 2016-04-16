import sys

dir = "/var/www/html/irs/flask/"
sys.path.insert(0, dir)

from api import app as application
