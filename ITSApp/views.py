
import logging
from .serializers import CommentSerializer, IssueSerializer, ProjectSerializer, BoardSerializer, ShortProjectSerializer, \
    ResponsibilitySerializer, MensionAssigneeSerializer, IssueDetailSerializer, SubscribeSerializer, \
    FilterIssueListSerializer,  MyPageSerializer, MyIssueListSerializer, \
    boardDetailSerializer
from .serializers import DepartmentSerializer,SignUpSerializer
from .models import Comment, Issue, Project, Department, User, Board, Responsibility, Assignee, Subscribe

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.reverse import reverse
from django.db.models import F, Q
import requests
from rest_framework.permissions import IsAuthenticated
from ITSJwt.views import UserList
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import PageNumberPagination


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


#슬랙 유저에게 DM보내기 위한 함수
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

# bot_token


#슬랙 DM보내는 클래스 Slack Bot token필요
class SlackDM(APIView):
    permission_classes = (IsAuthenticated,)
    name='slack-dm'
    def post(self, request):
        user_id=request.data.get('username')
        assignee=User.objects.get(username=user_id).name
        reporter=self.request.user.name
        state=request.data.get('state')
        post_message(bot_token,user_id, f'{reporter}님이  {assignee}님에게 {state}')
        return Response(status=200)

#전반적인 API
class ApiRoot(generics.GenericAPIView):
    name='api-root'
    def get(self,request,*arg,**kwargs):
        return Response({
            'department':reverse(DepartmentList.name,request=request),
            'comment': reverse(CommentList.name, request=request),
            'issue': reverse( IssueList.name, request=request),
            'project': reverse(ProjectList.name, request=request),
            'board':reverse(BoardList.name,request=request),
            'DM':reverse(SlackDM.name,request=request),
            'user': reverse(UserList.name, request=request),
            'responsibility': reverse(ResponsibilityList.name, request=request),
            'assignee': reverse(AssigneeList.name, request=request),
            'subscribe': reverse(SubscribeList.name, request=request),
        })


#마이페이지
class MyPageList(generics.RetrieveUpdateAPIView):
    name = 'MyPage-list'
    queryset = User.objects.all()
    serializer_class = MyPageSerializer
    lookup_url_kwarg = 'username'
    lookup_field = 'username'

    def get_queryset(self):
        user_id = self.kwargs['username']
        return User.objects.filter(username=user_id)


#내 이슈
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
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        return Issue.objects.filter(
         Q(reporter__username=self.request.user) | Q(assignee__user__username=self.request.user)
        ).order_by('board__order','-created_at').distinct()
        # return Issue.objects.order_by('-created_at')

#필터기능이 있는 이슈 리스트
class FilterIssueList(generics.ListCreateAPIView):
    name = 'filter-issueList-list'
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


#필터기능이 있는 보드리스트
class FilterBoardList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    name = 'filter-boardList-list'
    queryset = Board.objects.all()
    serializer_class =BoardSerializer
    lookup_url_kwarg = 'project_id'
    lookup_field = 'project_id'
    search_fields = ['issue__title', 'issue__content']
    filter_backends = [filters.SearchFilter,]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Board.objects.filter(project_id=project_id).order_by('order')

    def post(self, request, *args, **kwargs):
        print(request.data.get('project'))
        project_id=request.data.get('project')
        if Project.objects.filter(project_id=project_id,owner=self.request.user).exists()\
                or User.objects.filter(username=self.request.user).filter(is_staff=1).exists():
           return self.create(request, *args, **kwargs)

        return Response(status=status.HTTP_400_BAD_REQUEST)


#첫 로그인 시 데일리펀딩 이메일을 받는 API
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


#담당이슈->담당자 Read API
class ResponsibilityList(generics.ListCreateAPIView):
    queryset = Responsibility.objects.all().order_by('order')
    serializer_class = ResponsibilitySerializer
    name = 'responsibility-list'


#부서 API(ex:IT실,브랜드 기획,경영지원 등등)
class DepartmentList(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset=Department.objects.all()
    serializer_class = DepartmentSerializer
    name='department-list'


#댓글
class CommentList(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset=Comment.objects.filter(parent=None)
    serializer_class= CommentSerializer
    name='comment-list'


#댓글 디테일(수정,삭제)
class CommentDetailList(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Comment.objects.all()
    serializer_class= CommentSerializer
    name='commentDatail-list'


#이슈리스트
class IssueList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Issue.objects.order_by('-created_at')
    serializer_class = IssueSerializer
    name = 'issue-list'


#담당자 할당- 담당자+멘션(부담당자)
class AssigneeList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    name = 'assignee-list'
    queryset = Assignee.objects.all()
    serializer_class = MensionAssigneeSerializer


#이슈 디테일리스트-보고자,담당자만 수정,삭제 가능
class IssueDetailList(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Issue.objects.annotate(state=F('board__state'), project_id=F('board__project_id'))
    serializer_class = IssueDetailSerializer
    name = 'issue-detail-list'

    def put(self, request, *args, **kwargs):
        if Issue.objects.filter(pk=self.kwargs['pk']).filter(
                board__state='닫힘'
        ).exists():
            return self.update(request, *args, **kwargs)
        if Issue.objects.filter(pk=self.kwargs['pk']).filter(
                Q(reporter__username=self.request.user) | Q(assignee__user__username=self.request.user)
        ).exists():
            return self.update(request, *args, **kwargs)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        # if Issue.objects.filter(pk=self.kwargs['pk']).filter(
        #         board__state='닫힘'
        # ).exists():
        #     return self.partial_update(request, *args, **kwargs)

        if Issue.objects.filter(pk=self.kwargs['pk']).filter(
                Q(reporter__username=self.request.user) | Q(assignee__user__username=self.request.user)
        ).exists():
            return self.partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if Issue.objects.filter(pk=self.kwargs['pk']).filter(
                Q(reporter__username=self.request.user) | Q(assignee__user__username=self.request.user)
        ).exists():
            return self.destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_400_BAD_REQUEST)


#프로젝트리스트-프로젝트 생성한 사람->Owner
class ProjectList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Project.objects.all()
    name='project-list'
    serializer_class = ShortProjectSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


#프로젝트 디테일
class ProjectDetailList(generics.RetrieveUpdateDestroyAPIView):
    queryset=Project.objects.all()
    serializer_class = ProjectSerializer
    name = 'projectDetail-list'


#보드리스트
class BoardList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    name='board-list'


#보드 디테일 리스트
class BoardDetailList(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Board.objects.all()
    serializer_class = boardDetailSerializer
    name = 'boardDetail-list'

    def put(self, request, *args, **kwargs):
        project_id = Board.objects.get(board_id=self.kwargs['pk']).project_id
        print(project_id)
        if Project.objects.filter(project_id=project_id, owner=self.request.user).exists() \
                or User.objects.filter(username=self.request.user).filter(is_staff=1).exists():
            return self.update(request, *args, **kwargs)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        project_id=Board.objects.get(board_id=self.kwargs['pk'] ).project_id
        print(project_id)
        if Project.objects.filter(project_id=project_id,owner=self.request.user).exists()\
                    or User.objects.filter(username=self.request.user).filter(is_staff=1).exists():
            return self.partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        project_id = Board.objects.get(board_id=self.kwargs['pk']).project_id
        print(project_id)
        if Project.objects.filter(project_id=project_id, owner=self.request.user).exists() \
                or User.objects.filter(username=self.request.user).filter(is_staff=1).exists():
            return self.destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_400_BAD_REQUEST)


#구독자리스트
class SubscribeList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    name = 'subscribe-list'
    def post(self,request):
        subscriber_data=self.request.user
        subscriber = User.objects.get(username=subscriber_data).id
        issue=request.data.get('issue')
        user,created=Subscribe.objects.get_or_create(
            subscriber_id=subscriber, issue_id=issue
        )
        if created:
            return Response(status=status.HTTP_200_OK)
        else:
            Subscribe.objects.filter(
                    subscriber_id=subscriber, issue_id=issue
                ).delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

