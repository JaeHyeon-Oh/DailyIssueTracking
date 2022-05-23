
import logging
from .serializers import CommentSerializer,IssueSerializer,ProjectSerializer,BoardSerializer
from .serializers import DepartmentSerializer,SignUpSerializer
from .models import Comment,Issue,Project,Department,User,Board
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.reverse import reverse
from django.db.models import F

import requests
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

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
    # print(queryset)
    serializer_class = SignUpSerializer
    lookup_url_kwarg = 'username'
    lookup_field = 'username'
    name = 'signUp-list'


    def get_queryset(self):
        username = self.kwargs['username']
        # board_id = self.kwargs['board_id']
        print(username)
        return User.objects.filter(username=username)


class DeptIssueList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    name = 'department-list'

class DepartmentList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Department.objects.all()
    serializer_class = DepartmentSerializer
    name='department-list'

class CommentList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Comment.objects.filter(parent=None)
    serializer_class= CommentSerializer
    name='comment-list'

class IssueList(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Issue.objects.order_by('-created_at')
    serializer_class = IssueSerializer
    name = 'issue-list'

class IssueDetailList(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Issue.objects.all()
    # print(queryset)
    serializer_class = IssueSerializer
    lookup_url_kwarg = 'issue_id'
    lookup_field = 'issue_id'
    name = 'issue-detail-list'

    def get_queryset(self):
        issue_id = self.kwargs['issue_id']
        # board_id = self.kwargs['board_id']
        return Issue.objects.filter(issue_id=issue_id)

class ProjectList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Project.objects.all()
    serializer_class = ProjectSerializer
    name='project-list'

class BoardList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Board.objects.all()
    serializer_class=BoardSerializer
    name='board-list'

class BoardDetailList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BoardSerializer
    lookup_url_kwarg = 'project_id'
    lookup_field = 'project_id'
    name = 'boardDetail-list'

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        # board_id = self.kwargs['board_id']

        return  Board.objects.filter(project_id=project_id)
