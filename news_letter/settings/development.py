from .base import *

try:
    from news_letter.settings.local import *
except Exception:
    pass

DEBUG = True

ALLOWED_HOSTS = [
    '*'
]

DEV_APP = [

]

INSTALLED_APPS += DEV_APP

DEV_MID = [

]

MIDDLEWARE += DEV_MID