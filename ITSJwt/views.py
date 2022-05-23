from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from datetime import datetime

from .settings import api_settings
from .serializers import (
    JSONWebTokenSerializer, RefreshJSONWebTokenSerializer,
    VerifyJSONWebTokenSerializer
)

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

import datetime
from slack_sdk.web import WebClient
import json
from django.conf import settings

from ITSJwt.authentication import JSONWebTokenAuthentication
from .models import User
import jwt
from rest_framework import permissions
# from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime




class BackList(APIView):
    permission_classes = (permissions.AllowAny,)
    name='Back-List'
    queryset = User.objects.all()
    # serializer_class = CustomUserSerializer
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
        # user, created = User.objects.get_or_create(
        #     username=username,
        # )
        user=User.objects.filter(username=username).first()
        if not user:
            User.objects.create(
                username=username,
                email=email,
                name=name,
                picture=picture,
            )
            return Response({"username": username, "name": name}, status=status.HTTP_201_CREATED)
        else:
            print(username)
            print(name)
            return Response({"username": username, "name": name}, status=status.HTTP_202_ACCEPTED)
        # if created:
        #     User.objects.filter(username=username).update(
        #         email=email,
        #         name=name,
        #         picture=picture,
        #     )
        #     return Response({"username": username,"name":name},status=status.HTTP_201_CREATED)

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


class ObtainJSONWebToken(JSONWebTokenAPIView):

    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer


class VerifyJSONWebToken(APIView):

    # permission_classes = (IsAuthenticated,)
    """
    API View that checks the veracity of a token, returning the token if it
    is valid.
    """

    # serializer_class = VerifyJSONWebTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer=VerifyJSONWebTokenSerializer(data=request.data)
        if serializer.is_valid():
            print('확인')
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

class RefreshJSONWebToken(APIView):
    # permission_classes = (IsAuthenticated,)
    """
    API View that returns a refreshed token (with new expiration) based on
    existing token

    If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token
    """
    # serializer_class = RefreshJSONWebTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer= RefreshJSONWebTokenSerializer(data=request.data)
        if serializer.is_valid():
            print('확인')
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
