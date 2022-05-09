from rest_framework.views import APIView
from slack_sdk.web import WebClient
import json
from .models import User
import jwt
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import F
from .serializers import AuthLoginSerializer

class BackList(APIView):
    name='Back-List'
    def post(self,request):
        print(request)
        # access_token=request.data['access_token']

        access_token=request.data.get('access_token')
        print('access token'+access_token)
        profiles = WebClient(token=access_token).openid_connect_userInfo()
        data=json.dumps(profiles.data)
        profile=json.loads(data)
        user_id = profile['sub']
        email = profile['email']
        name = profile['name']
        picture=profile['picture']
        user=User.objects.filter(user_id=user_id).first()
        if not user:
            User.objects.create(
                user_id=user_id,
                email=email,
                name=name,
                picture=picture,
            )
        # else:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        jwt_token = jwt.encode({"id": user_id, "name": name}, 'SECRET_KEY', algorithm='HS256')
        return Response({'ACCESS_TOKEN': jwt_token,'user_id': user_id,'name': name,
                }, status=status.HTTP_201_CREATED)
class AutoLoginList(APIView):
    name = 'AutoLogin-List'

    def post(self, request):
        try:
            user = jwt.decode(request.headers['Authorization'], 'SECRET_KEY', algorithms='HS256')
            # print(user)
            user_id = user['id']
            name=user['name']
            # print(user_id)
            # print(name)
            queryset=User.objects.filter(user_id=user_id)
                # .annotate(dept=F('responsibleIssue__department_id'))
            print(queryset[0])
            serializer=AuthLoginSerializer(queryset,many=True)
            print(serializer.data)
            return Response(serializer.data)
            # user=User.objects.filter(user_id=user_id).first()
            # #담당부서도 리턴 포함
            # return Response({'user_id': user_id, 'name': name,'dept':dept }, status=status.HTTP_200_OK)

            # if User.objects.filter(pk=email).exists():
            #     return Response({
            #         {'Success': 'True', 'user_id': user_id, 'email': email, }
            #     }, status=200)
        except KeyError:
            return Response({'message': 'KEY_ERROR'}, status=400)