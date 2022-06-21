from rest_framework import generics
from .settings import api_settings
from .serializers import (
    JSONWebTokenSerializer, RefreshJSONWebTokenSerializer,
    VerifyJSONWebTokenSerializer
)

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_obtain_response_payload_handler=api_settings.JWT_OBTAIN_RESPONSE_PAYLOAD_HANDLER
jwt_verify_response_payload_handler=api_settings.JWT_VERIFY_RESPONSE_PAYLOAD_HANDLER

import datetime
from slack_sdk.web import WebClient
import json
from .models import User
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from .serializers import UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name='user-list'


class BackList(APIView):
    permission_classes = (permissions.AllowAny,)
    name='Back-List'
    queryset = User.objects.all()
    fields = '__all__'

    def post(self,request):
        access_token=request.data.get('access_token')
        profiles = WebClient(token=access_token).openid_connect_userInfo()
        data=json.dumps(profiles.data)
        profile=json.loads(data)
        username = profile['sub']
        email = profile['email']
        name = profile['name']
        picture=profile['picture']
        user=User.objects.filter(username=username).first()
        if not user:
            User.objects.create(
                username=username,
                email=email,
                name=name,
                picture=picture,
            )
            return Response({"username": username, "name": name, "picture":picture}, status=status.HTTP_201_CREATED)
        else:
            return Response({"username": username, "name": name, "picture":picture}, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class JSONWebTokenAPIView(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = JSONWebTokenSerializer
    def get_serializer_context(self):

        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer_class(self):

        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer=JSONWebTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            access_token = serializer.object.get('access_token')
            refresh_token=serializer.object.get('refresh_token')
            exp=serializer.object.get('exp')

            response_data = jwt_obtain_response_payload_handler(access_token,refresh_token,exp, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    access_token,
                                    refresh_token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainJSONWebToken(JSONWebTokenAPIView):

    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer


class VerifyJSONWebToken(APIView):

    """
    API View that checks the veracity of a token, returning the token if it
    is valid.
    """

    def post(self, request, *args, **kwargs):
        serializer=VerifyJSONWebTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            exp = serializer.object.get('exp')
            response_data = jwt_verify_response_payload_handler(token, exp, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshJSONWebToken(APIView):
    """
    API View that returns a refreshed token (with new expiration) based on
    existing token

    If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token
    """
    def post(self, request, *args, **kwargs):
        serializer= RefreshJSONWebTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


obtain_jwt_token = ObtainJSONWebToken.as_view()
refresh_jwt_token = RefreshJSONWebToken.as_view()
verify_jwt_token = VerifyJSONWebToken.as_view()
