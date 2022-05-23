from django.urls import path
from .views import CommentList,IssueList,ProjectList,DepartmentList,ApiRoot,SignUpList,IssueDetailList,DeptIssueList,Attend,BoardDetailList,BoardList
    # ,LogoutAndBlacklistRefreshTokenForUserView
    # ,SlackAlarmList
# from ITSApp import views
urlpatterns = [
    path("", ApiRoot.as_view()),
    path('project/<int:project_id>/', BoardDetailList.as_view(), name=BoardDetailList.name),
    path('issue/<int:issue_id>/', IssueDetailList.as_view(), name=IssueDetailList.name),
    path('board/', BoardList.as_view(), name=BoardList.name),
    path('project', ProjectList.as_view(), name=ProjectList.name),
    path("comment",CommentList.as_view(),name=CommentList.name),
    path("issue", IssueList.as_view(), name=IssueList.name),
    path("project", ProjectList.as_view(), name=ProjectList.name),
    path("dept",DeptIssueList.as_view(),name=DeptIssueList.name),
    path('slack/dm',Attend.as_view(),name=Attend.name),
    path('signUp/<str:username>', SignUpList.as_view(), name=SignUpList.name),
]
