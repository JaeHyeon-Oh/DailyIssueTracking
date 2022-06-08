
import logging
from .serializers import CommentSerializer, IssueSerializer, ProjectSerializer, BoardSerializer, ShortProjectSerializer, \
    ResponsibilitySerializer, AssigneeSerializer, MensionAssigneeSerializer, IssueDetailSerializer, SubscribeSerializer, \
    FilterIssueListSerializer, FilterBoardListSerializer, MyPageSerializer, MyIssueListSerializer
from .serializers import DepartmentSerializer,SignUpSerializer
from .models import Comment, Issue, Project, Department, User, Board, Responsibility, Assignee, Subscribe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.reverse import reverse
from django.db.models import F, Q
from django.shortcuts import get_object_or_404
import requests
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from ITSJwt.views import UserList
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import PageNumberPagination

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
        print(request.data.get('username'))
        print(request.data.get('state'))

        # challenge = request.data.get('challenge')
        # return Response(status=200, data=dict(challenge=challenge))
        user_id=request.data.get('username')
        state=request.data.get('state')
        # user_id='@U01JVAQ25CZ'
        post_message(bot_token,user_id, f'{user_id}가 {state}로 변경했습니다.')
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
            'user': reverse(UserList.name, request=request),
            'responsibility': reverse(ResponsibilityList.name, request=request),
            'assignee': reverse(AssigneeList.name, request=request),
            'subscribe': reverse(SubscribeList.name, request=request),
            # 'Filter': reverse(FilterIssueList.name, request=request),
            # 'myPage':reverse(MyPageList.name,request=request),
        })

class MyPageList(generics.RetrieveUpdateAPIView):
    name = 'MyPage-list'
    queryset = User.objects.all()
    serializer_class = MyPageSerializer
    lookup_url_kwarg = 'username'
    lookup_field = 'username'

    def get_queryset(self):
        user_id = self.kwargs['username']
        return User.objects.filter(username=user_id)

class MyIssueList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    name = 'MyIssue-list'
    serializer_class = MyIssueListSerializer
    # lookup_url_kwarg = 'board__project__project_id'
    # lookup_field = 'board__project__project_id'
    filter_fields = ['board__state','assignee__mension','subscribe__flag']
    search_fields = ['title','content']
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['board__state','deadline','created_at']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        print(self.request.user)
        # project_id = self.kwargs['board__project__project_id']
        # return Issue.objects.filter(board__project__project_id=project_id).filter(
        #  Q(reporter__username=self.request.user) | Q(assignee__user__username=self.request.user)
        # ).order_by('-created_at')
        return Issue.objects.filter(
         Q(reporter__username=self.request.user) | Q(assignee__user__username=self.request.user)
        ).order_by('-created_at')

class FilterIssueList(generics.ListCreateAPIView):
    name = 'filter-issueList-list'
    # queryset = Issue.objects.all().order_by('-created_at')
    serializer_class = FilterIssueListSerializer
    lookup_url_kwarg = 'board__project__project_id'
    lookup_field = 'board__project__project_id'
    filter_fields = ['board__state',]
    search_fields = ['title','content']
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['board__state','deadline','created_at']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        project_id = self.kwargs['board__project__project_id']
        return Issue.objects.filter(board__project__project_id=project_id).order_by('-created_at')

class FilterBoardList(generics.ListCreateAPIView):
    name = 'filter-boardList-list'
    queryset = Board.objects.all()
    serializer_class =BoardSerializer
    lookup_url_kwarg = 'project_id'
    lookup_field = 'project_id'

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Board.objects.filter(project_id=project_id).order_by('order')

    def post(self, request, *args, **kwargs):
        print(Board.objects.filter(project__owner=self.request.user))
        # if 'board' in request.data.keys():
        #     board = self.get_board(request.data['board'])
        #     return super().post(request, *args, **kwargs)
        # return Response(status=status.HTTP_400_BAD_REQUEST)

class SignUpList(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    lookup_url_kwarg = 'username'
    lookup_field = 'username'
    name = 'signUp-list'


    def get_queryset(self):
        print(self)
        username = self.kwargs['username']
        print(username)
        return User.objects.filter(username=username)

class ResponsibilityList(generics.ListCreateAPIView):
    queryset = Responsibility.objects.all().order_by('order')
    serializer_class = ResponsibilitySerializer
    name = 'responsibility-list'

class DeptIssueList(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    name = 'department-list'

class DepartmentList(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset=Department.objects.all()
    serializer_class = DepartmentSerializer
    name='department-list'

class CommentList(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset=Comment.objects.filter(parent=None)
    serializer_class= CommentSerializer
    name='comment-list'



class CommentDetailList(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset=Comment.objects.all()
    serializer_class= CommentSerializer
    name='commentDatail-list'

class IssueList(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Issue.objects.order_by('-created_at')
    serializer_class = IssueSerializer
    name = 'issue-list'
    # lookup_url_kwarg = 'board__project__project_id'
    # lookup_field = 'board__project__project_id'
    # def get_queryset(self):
    #     project_id = self.kwargs['board__project__project_id']
    #     return Issue.objects.filter(board__project__project_id=project_id)

class IssueList(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Issue.objects.order_by('-created_at')
    serializer_class = IssueSerializer
    name = 'issue-list'
    # lookup_url_kwarg = 'board__project__project_id'
    # lookup_field = 'board__project__project_id'
    # def get_queryset(self):
    #     project_id = self.kwargs['board__project__project_id']
    #     return Issue.objects.filter(board__project__project_id=project_id)

class AssigneeList(generics.ListCreateAPIView):
    name = 'assignee-list'
    queryset = Assignee.objects.all()
    serializer_class = MensionAssigneeSerializer

class IssueDetailList(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Issue.objects.all()
    # print(queryset)
    serializer_class = IssueDetailSerializer
    # lookup_url_kwarg = 'issue_id'
    # lookup_field = 'issue_id'
    name = 'issue-detail-list'

    # def get_queryset(self):
    #     issue_id = self.kwargs['issue_id']
    #     # board_id = self.kwargs['board_id']
    #     return Issue.objects.filter(issue_id=issue_id)

class ProjectList(generics.ListCreateAPIView):
    # authentication_classes = []
    permission_classes = (IsAuthenticated,)
    queryset=Project.objects.all()
    # serializer_class = ProjectSerializer
    name='project-list'
    serializer_class = ShortProjectSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProjectDetailList(generics.RetrieveUpdateDestroyAPIView):
    queryset=Project.objects.all()
    serializer_class = ProjectSerializer
    name = 'projectDetail-list'

class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    name='board-list'




class BoardDetailList(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    name = 'boardDetail-list'





class SubscribeList(generics.ListCreateAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    name = 'subscribe-list'
    def post(self,request):
        subscriber=request.data.get('subscriber')
        issue=request.data.get('issue')
        print(request.data)
        user,created=Subscribe.objects.get_or_create(
            subscriber=subscriber, issue=issue
        )
        print(user)
        if not created:
            flag=Subscribe.objects.filter(
                    subscriber=subscriber, issue=issue,flag=True
                ).update(flag=False)

            if not flag:
                Subscribe.objects.filter(
                    subscriber=subscriber, issue=issue
                ).update(flag=True)
                
            return Response(status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

