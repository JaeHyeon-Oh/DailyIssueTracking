# import datetime
# from slack_sdk.web import WebClient
# import json
# from django.conf import settings
#
# from .authentication import JSONWebTokenAuthentication
# from .models import User,Token
# import jwt
# from rest_framework import permissions
# # from .serializers import MyTokenObtainPairSerializer
# from rest_framework.permissions import IsAuthenticated
# # from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework.response import Response
# from datetime import datetime
#
#
#
#
# class ObtainTokenPairWithColorView(APIView):
#     authentication_classes =(JSONWebTokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     # permission_classes = (IsAuthenticated,)
#     # def post(self,request):
#     #         username = request.data.get('username')
#     #         print(username)
#     #         name=request.data.get('name')
#     #         print(name)
#     #         payload = {
#     #             "iss": "dailyfunding",
#     #             "iat": datetime.datetime.utcnow(),
#     #             "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
#     #             "aud": "www.dailyfunding.com",
#     #             "sub": username,
#     #             "name": name,
#     #             "scopes": ['open']
#     #         }
#     #         token = jwt.encode(payload, 'secret', algorithm='HS256')
#     #         payload['grant_type'] = "refresh"
#     #         payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=14)
#     #         refresh_token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
#     #         Token.objects.create(key=refresh_token,username=username)
#     #         return Response({
#     #             'access_token': token,
#     #             # 'user_id': user_id,
#     #             "refresh_token": refresh_token}, status=status.HTTP_201_CREATED)
#
# class BackList(APIView):
#     permission_classes = (permissions.AllowAny,)
#     name='Back-List'
#     queryset = User.objects.all()
#     # serializer_class = CustomUserSerializer
#     fields = '__all__'
#
#
#     def post(self,request):
#         # print(request)
#         access_token=request.data.get('access_token')
#         print('access token'+access_token)
#         profiles = WebClient(token=access_token).openid_connect_userInfo()
#         data=json.dumps(profiles.data)
#         profile=json.loads(data)
#         username = profile['sub']
#         email = profile['email']
#         name = profile['name']
#         picture=profile['picture']
#         user=User.objects.filter(username=username).first()
#         if not user:
#             User.objects.create(
#                 username=username,
#                 email=email,
#                 name=name,
#                 picture=picture,
#             )
#             return Response({"username": username,"name":name},status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
# class TokenRefreshView(APIView):
#     permission_classes = (permissions.AllowAny,)
#     def post(self, request):
#         try:
#             refresh_token = request.data.get("refresh_token")
#             checkRefreshtoken= Token.objects.filter(key=refresh_token)
#             if checkRefreshtoken:
#                 payload = {
#                     "iss": "dailyfunding",
#                     "iat": datetime.datetime.utcnow(),
#                     "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
#                     "aud": "www.dailyfunding.com",
#                     "sub": checkRefreshtoken.user.username,
#                     "name": checkRefreshtoken.user.name,
#                     "scopes": ['open']
#                 }
#                 token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALG)
#                 return Response({
#                             'access_token': token,
#                             # 'user_id': user_id,
#                            }, status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#
#
# class AutoLoginList(APIView):
#     # permission_classes = (IsAuthenticated,)
#     name = 'AutoLogin-List'
#
#     def post(self, request):
#         try:
#             user = jwt.decode(request.headers['Authorization'], settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALG)
#             # print(user)
#             username = user['username']
#             name=user['name']
#             # print(user_id)
#             # print(name)
#             queryset=User.objects.filter(username=username)
#                 # .annotate(dept=F('responsibleIssue__department_id'))
#             print(queryset[0])
#             serializer=AuthLoginSerializer(queryset,many=True)
#             print(serializer.data)
#             return Response(serializer.data)
#             # user=User.objects.filter(user_id=user_id).first()
#             # #담당부서도 리턴 포함
#             # return Response({'user_id': user_id, 'name': name,'dept':dept }, status=status.HTTP_200_OK)
#
#             # if User.objects.filter(pk=email).exists():
#             #     return Response({
#             #         {'Success': 'True', 'user_id': user_id, 'email': email, }
#             #     }, status=200)
#         except KeyError:
#             return Response({'message': 'KEY_ERROR'}, status=400)
#
#
#
#
#
#
#
#
