"""ITS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import CommentList,IssueList,ProjectList,DepartmentList,ApiRoot,SignUpList,DeptIssueList,Attend,BoardDetailList,BoardList
from .slackViews import BackList,AutoLoginList
    # ,SlackAlarmList
# from ITSApp import views
urlpatterns = [
    path("", ApiRoot.as_view()),
    path('project/<int:project_id>/', BoardDetailList.as_view(), name=BoardDetailList.name),
    path('board/', BoardList.as_view(), name=BoardList.name),
    path('project', ProjectList.as_view(), name=ProjectList.name),
    path("comment",CommentList.as_view(),name=CommentList.name),
    path("issue", IssueList.as_view(), name=IssueList.name),
    path("project", ProjectList.as_view(), name=ProjectList.name),
    path("dept",DeptIssueList.as_view(),name=DeptIssueList.name),
    path('slack/dm',Attend.as_view(),name=Attend.name),
    # path('slack/oauth_redirect', CallBackList.as_view(), name=CallBackList.name),
    path('auth/slack',BackList.as_view(),name=BackList.name),
    path('signUp/<str:pk>', SignUpList.as_view(), name=SignUpList.name),
    path('auth/ITS',AutoLoginList.as_view(),name=AutoLoginList.name)

]
