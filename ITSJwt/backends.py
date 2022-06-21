from .models import User
from django.contrib.auth import get_user_model

UserModel = get_user_model()
print(UserModel)
class HashModelBackend:
    def authenticate(request=None, username=None):
        try:
            user = User.objects.get(username=username)
            print(user.id)
            print(user.is_active)
            return user
        except User.DoesNotExist:
            return None

