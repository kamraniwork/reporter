from rest_framework import routers
from django.urls import path, include
from users.views.users import (
    RegisterUser
)

router = routers.SimpleRouter()
router.register(r'', RegisterUser, basename='register')

app_name = 'auth'
urlpatterns = [
    path('', include(router.urls)),
]
