from users.models.user import User


def validate_email(email):
    try:
        User.objects.get(email=email)
        return False
    except User.DoesNotExist:
        return True
