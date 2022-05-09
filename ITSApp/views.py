# # ~/ITSApp/views.py
import os
import time
import logging
from django.http import Http404
from rest_framework import status, permissions

from django.views import View
from slack_sdk.oauth import OpenIDConnectAuthorizeUrlGenerator, RedirectUriPageRenderer
from slack_sdk.oauth.state_store import FileOAuthStateStore
from django.http.response import JsonResponse
from ITS.settings import SLACK_CLIENT_ID, SLACK_CLIENT_SECRET_ID, SLACK_OAUTH_REDIRECT_URI, LOGIN_URL
from .serializers import CommentSerializer,IssueSerializer,ProjectSerializer,BoardSerializer
from .serializers import DepartmentSerializer,SignUpSerializer
from .models import Comment,Issue,Project,Department,User,Board
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.reverse import reverse
from django.db.models import F

import requests

client_id = "1652575731968.3400923882144"
client_secret = "a346582347d334384e4d27e6a7429f53"
redirect_uri = "https://5723-221-148-180-175.ngrok.io/slack/oauth_redirect"
scopes = ["openid", "email", "profile"]
slack_token = "xoxb-1652575731968-3389792429617-FLXRcJbqTWFG62c1jGsaJ8Xx"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

bot_token = 'xoxb-1652575731968-3356240076419-CJrKx8YKYLBuYuJ5wlvDG7NP'

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
# 봇 토큰 추가



# Create your views here.
class Attend(APIView):
    name='slack-dm'
    def post(self, request):
        # challenge = request.data.get('challenge')
        # return Response(status=200, data=dict(challenge=challenge))
        user_id='@U01JVAQ25CZ'
        post_message(bot_token,user_id, f'{user_id}에 DM 체크하는 중입니다')
        return Response(status=200)

class ApiRoot(generics.GenericAPIView):
    name='api-root'
    def get(self,request,*arg,**kwargs):
        return Response({
            'department':reverse(DepartmentList.name,request=request),
            'comment': reverse(CommentList.name, request=request),
            'issue': reverse( IssueList.name, request=request),
            'project': reverse(ProjectList.name, request=request),
            'board':reverse(BoardList.name,request=request),
            'DM':reverse(Attend.name,request=request),
        })




class SignUpList(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    name = 'signUp-list'

class DeptIssueList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    name = 'department-list'
class DepartmentList(generics.ListAPIView):
    queryset=Department.objects.all()
    serializer_class = DepartmentSerializer
    name='department-list'

class CommentList(generics.ListCreateAPIView):
    queryset=Comment.objects.filter(parent=None)
    serializer_class= CommentSerializer
    name='comment-list'

class IssueList(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    name = 'issue-list'

class ProjectList(generics.ListCreateAPIView):
    queryset=Project.objects.all()
    serializer_class = ProjectSerializer
    name='project-list'

class BoardList(generics.ListAPIView):
    queryset=Board.objects.all()
    serializer_class=BoardSerializer
    name='board-list'

class BoardDetailList(generics.ListAPIView):
    serializer_class = BoardSerializer
    lookup_url_kwarg = 'project_id'
    lookup_field = 'project_id'
    name = 'boardDetail-list'

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        # board_id = self.kwargs['board_id']

        return  Board.objects.filter(project_id=project_id)
