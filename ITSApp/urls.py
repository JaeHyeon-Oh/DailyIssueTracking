from django.urls import path
from .views import CommentList, IssueList, ProjectList, DepartmentList, ApiRoot, SignUpList, \
    ResponsibilityList, \
    ProjectDetailList, IssueDetailList, SlackDM, BoardDetailList, BoardList, AssigneeList, \
    CommentDetailList, SubscribeList, FilterIssueList, FilterBoardList, MyPageList, MyIssueList

urlpatterns = [
    path("", ApiRoot.as_view()),
    path('project/<int:pk>/',  ProjectDetailList.as_view(), name= ProjectDetailList.name),
    path('issue/<int:pk>/', IssueDetailList.as_view(), name=IssueDetailList.name),
    path('board/', BoardList.as_view(), name=BoardList.name),
    path('board/<int:pk>/', BoardDetailList.as_view(), name=BoardDetailList.name),
    path('project/', ProjectList.as_view(), name=ProjectList.name),
    path("comment/",CommentList.as_view(),name=CommentList.name),
    path("comment/<int:pk>", CommentDetailList.as_view(), name=CommentDetailList.name),
    path("issue/", IssueList.as_view(), name=IssueList.name),
    path("department",DepartmentList.as_view(),name=DepartmentList.name),
    path('slack/dm',SlackDM.as_view(),name=SlackDM.name),
    path('signUp/<str:username>', SignUpList.as_view(), name=SignUpList.name),
    path('responsibility',ResponsibilityList.as_view(),name=ResponsibilityList.name),
    path('assignee',AssigneeList.as_view(),name=AssigneeList.name),
    path('subscribe',SubscribeList.as_view(),name=SubscribeList.name),
    path('project/<int:board__project__project_id>/issue',FilterIssueList.as_view(),name=FilterIssueList.name),
    path('project/<int:board__project__project_id>/MyIssue',MyIssueList.as_view(),name=MyIssueList.name),
    path('MyIssue',MyIssueList.as_view(),name=MyIssueList.name),
    path('project/<int:project_id>/board',FilterBoardList.as_view(),name=FilterBoardList.name),
    path('myPage/<str:username>',MyPageList.as_view(),name=MyPageList.name),
]
