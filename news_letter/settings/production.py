from .base import *

try:
    from news_letter.settings.local import *
except Exception:
    pass

DEBUG = False
ALLOWED_HOSTS = [
    'test.com',
    'www.test.com',
]
