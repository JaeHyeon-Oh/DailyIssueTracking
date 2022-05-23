from django.urls import path
from .views import obtain_jwt_token,verify_jwt_token,refresh_jwt_token, BackList
urlpatterns = [
    path('token/', obtain_jwt_token),#첫 회원가입 때 refresh token 발급
    path('token/verify/', verify_jwt_token),#refresh token만료기간 확인
    path('token/refresh/', refresh_jwt_token),#New refresh token
    path('auth/slack',BackList.as_view(),name=BackList.name),
    # path('token/obtain/', obtain_jwt_token),
    # path('token/refresh/', refresh_jwt_token),
]