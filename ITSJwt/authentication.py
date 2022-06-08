import jwt,json
from slack_sdk.web import WebClient

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header
)

from .models import User


def jwt_get_username_from_payload(payload):
    """
    Override this function if user_id is formatted differently in payload
    """
    return payload.get('username')


# def jwt_decode_handler(token):
#     print('해독가능?')
#     options = {
#         'verify_exp': True,
#     }
#     # get user from token, BEFORE verification, to get user secret key
#     # unverified_payload = jwt.decode(token, None, False)
#     secret_key = 'default'
#     return jwt.decode(
#         token,
#         secret_key,
#         True,
#         options=options,
#         leeway=0,
#         audience=None,
#         issuer=None,
#         algorithms=[settings.JWT_ALG]
#     )
def jwt_decode_handler(token):
    options = {
        'verify_exp': False,
    }
    # get user from token, BEFORE verification, to get user secret key
    # unverified_payload = jwt.decode(token, None, False)
    # secret_key = jwt_get_secret_key(unverified_payload)
    return jwt.decode(
        token,
        'SECRET_KEY',
        False,
        options=options,
        leeway=0,
        audience=None,
        issuer=None,
        algorithms='HS256'
    )

class BaseJSONWebTokenAuthentication(BaseAuthentication):
    """
    Token based authentication using the JSON Web Token standard.
    """
    def authenticate(self, request):

        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignatureError:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        return (user, payload)

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        User = get_user_model()
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):
    """
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string specified in the setting
    `JWT_AUTH_HEADER_PREFIX`. For example:

        Authorization: JWT eyJhbGciOiAiSFMyNTYiLCAidHlwIj
    """
    www_authenticate_realm = 'api'
    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        if not auth:
            return None

        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]
