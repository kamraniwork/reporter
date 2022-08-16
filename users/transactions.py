from django.db import transaction


@transaction.atomic
def set_user_password(user, password):
    user.set_password(password)
    user.is_active = True
    user.save()
