from django.urls import path
from .views import CommentList, IssueList, ProjectList, DepartmentList, BoardList, ApiRoot, SignUpList, \
    ResponsibilityList, \
    ProjectDetailList, IssueDetailList, DeptIssueList, Attend, BoardDetailList, BoardList, AssigneeList, \
    CommentDetailList, SubscribeList, FilterIssueList, FilterBoardList, MyPageList, MyIssueList

# ,LogoutAndBlacklistRefreshTokenForUserView
    # ,SlackAlarmList
# from ITSApp import views
urlpatterns = [
    path("", ApiRoot.as_view()),
    path('project/<int:pk>/',  ProjectDetailList.as_view(), name= ProjectDetailList.name),
    # path('project/<int:project_id>/',BoardList.as_view(),  name=BoardList.name),
    path('issue/<int:pk>/', IssueDetailList.as_view(), name=IssueDetailList.name),
    path('board/', BoardList.as_view(), name=BoardList.name),
    path('board/<int:pk>/', BoardDetailList.as_view(), name=BoardDetailList.name),
    path('project/', ProjectList.as_view(), name=ProjectList.name),
    path("comment/",CommentList.as_view(),name=CommentList.name),
    path("comment/<int:pk>", CommentDetailList.as_view(), name=CommentDetailList.name),
    path("issue/", IssueList.as_view(), name=IssueList.name),
    path("dept",DeptIssueList.as_view(),name=DeptIssueList.name),
    path('slack/dm',Attend.as_view(),name=Attend.name),
    path('signUp/<str:username>', SignUpList.as_view(), name=SignUpList.name),
    path('responsibility',ResponsibilityList.as_view(),name=ResponsibilityList.name),
    path('assignee',AssigneeList.as_view(),name=AssigneeList.name),
    path('subscribe',SubscribeList.as_view(),name=SubscribeList.name),
    # path('issueList',FilterIssueList.as_view(),name=FilterIssueList.name)
    path('project/<int:board__project__project_id>/issue',FilterIssueList.as_view(),name=FilterIssueList.name),
    # path('project/<int:board__project__project_id>/MyIssue',MyIssueList.as_view(),name=MyIssueList.name),
    path('MyIssue',MyIssueList.as_view(),name=MyIssueList.name),
    path('project/<int:project_id>/board',FilterBoardList.as_view(),name=FilterBoardList.name),
    path('myPage/<str:username>',MyPageList.as_view(),name=MyPageList.name),

]
