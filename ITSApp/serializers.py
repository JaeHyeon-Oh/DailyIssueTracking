from ITSJwt.models import User
from .models import Project,Department,ResponsibleIssue,Board,Issue
from .models import Comment,Attachment
# from .models import User
import jwt

from calendar import timegm
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers


# class DiaryImageSerializer(serializers.ModelSerializer):
#
#     image = serializers.ImageField(use_url=True)
#
#     class Meta:
#         model = Attachment
#         fields = ['image']
#
#
# class IssueSerializer(serializers.ModelSerializer):
#
#     images = serializers.SerializerMethodField()
#
#     def get_images(self, obj):
#         image = obj.diaryimage_set.all()
#         return DiaryImageSerializer(instance=image, many=True, context=self.context).data
#
#     class Meta:
#         model = Issue
#         fields = '__all__'
#
#     def create(self, validated_data):
#         instance = Issue.objects.create(**validated_data)
#         image_set = self.context['request'].FILES
#         for image_data in image_set.getlist('image'):
#             Attachment.objects.create(diary=instance, image=image_data)
#         return instance
#
#
# class IssueListSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Issue
#         fields = '__all__'

class AttachmentSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model=Attachment
        fields=['image']

class IssueSerializer(serializers.ModelSerializer):
    attachment=AttachmentSerializer(many=True, read_only=True)


    class Meta:
        model = Issue
        fields = ['user','board','title','content','deadline','priority','attachment']
        # fields='__all__'
    def create(self, validated_data):
       images_data = self.context['request'].FILES
       post = Issue.objects.create(**validated_data)
       for image_data in images_data.getlist('image'):
           Attachment.objects.create(issue=post, image=image_data)
       return post


#보드
class BoardSerializer(serializers.ModelSerializer):
    # project=ProjectSerializer()
    # state=StateSerializer(read_only=True,many=True)
    issue=IssueSerializer(many=True,allow_null=True)

    class Meta:
        model=Board
        fields='__all__'

# 프로젝트
class ProjectSerializer(serializers.ModelSerializer):
    # board = serializers.SerializerMethodField()
    #
    class Meta:
        model=Project
        fields=['project_id','project_name']

    def create(self,validated_data):
        # data = validated_data.get('board_type')
        project = Project.objects.create(**validated_data)
        print(project.project_id)
        Board.objects.bulk_create([
            Board(project_id=project.project_id,title='할 일'),
            Board(project_id=project.project_id,title='진행'),
            Board(project_id=project.project_id,title='검증'),
            Board(project_id=project.project_id,title='완료'),

        ])
        return project

#부서-담당이슈
class MapDeptSerializer(serializers.ModelSerializer):
    # dept_name = serializers.ChoiceField(choices=Department.DEPT_CHOICES)
    # 'priority_description' 선택값 설명
    # dept_name_description = serializers.CharField(source='get_dept_name_display', read_only=True)
    # responsibleIssue=ResponsibleIssueSerializer()
    class Meta:
        model=Department
        fields = ['dept_name']

#담당이슈-유저
class MapRespIssueSerializer(serializers.ModelSerializer):
    # department = MapDeptSerializer()
    class Meta:
        model = ResponsibleIssue
        fields=['responsible_issue_name']
        # ,'department']
        # fields = '__all__'

class ResponsibleIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsibleIssue
        fields=['responsible_issue_name']
        # fields = '__all__'


#부서
class DepartmentSerializer(serializers.ModelSerializer):
    # dept_name = serializers.ChoiceField(choices=Department.DEPT_CHOICES)
    # 'priority_description' 선택값 설명
    dept_name_description = serializers.CharField(source='get_dept_name_display', read_only=True)
    responsibleIssue=ResponsibleIssueSerializer(many=True,read_only=True)
    class Meta:
        model=Department
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['email']


class AuthLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields = ['user_id','name']



#사용자(디테일)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = '__all__'
# #이슈(디테일)
# class IssueSerializer(serializers.ModelSerializer):
#     priority=serializers.ChoiceField(choices=Issue.PRIORITY_CHOICES)
#     #'priority_description' 선택값 설명
#     priority_description=serializers.CharField(source='get_priority_display',read_only=True)
#     class Meta:
#         model=Issue
#         fields = '__all__'

#대댓글 재귀적으로 구현
class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data

#댓글
class CommentSerializer(serializers.ModelSerializer):
    # reply = serializers.SerializerMethodField()
    reply = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        # fields = ('comment_id', 'parent', 'comment_content', 'reply')
        fields='__all__'
