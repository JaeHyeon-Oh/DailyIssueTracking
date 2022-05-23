from .models import User
from django.contrib.auth import get_user_model

from django.conf import settings
UserModel = get_user_model()
print(UserModel)
class HashModelBackend:
    def authenticate(request=None, username=None):
        try:
            # print(User.objects.get(username=username))
            user = User.objects.get(username=username)
            print(user.id)
            print(user.is_active)
            return user
        except User.DoesNotExist:
            return None

    # def get_user(self, user_id):
    #     try:
    #         return User.objects.get(pk=user_id)
    #     except User.DoesNotExist:
    #         return None