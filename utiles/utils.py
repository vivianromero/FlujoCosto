from django.contrib.auth.models import User

def crear_superusuario(credentials):

    user, created = User.objects.get_or_create(
        username = credentials["username"],
        email=credentials["email"],
        defaults={"is_active": True, "is_staff": True, "is_superuser": True},
    )
    if created:
        user.set_password(credentials["password"])
        user.save()
        msg = "Superusuario - %(email)s creado satisfactoriamente " % credentials
    else:
        msg = "Superusuario - %(email)s ya existe " % credentials
    return msg
