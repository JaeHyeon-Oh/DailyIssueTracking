from ITSJwt.models import User
from ITSJwt.serializers import WriterSerializer
from .models import Project, Department, ResponsibleIssue, Board, Issue, Assignee, Subscribe
from .models import Comment,Attachment,Responsibility


# from .models import User
import jwt

from calendar import timegm
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers

from ITSJwt.serializers import UserSerializer


class AttachmentSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model=Attachment
        fields=['image']

class ResponsibilitySerializer(serializers.ModelSerializer):
    name=serializers.CharField(source='user.name')
    user_id=serializers.CharField(source='user.username')
    responsibleIssue_name=serializers.CharField(source='responsible_issue.responsible_issue_name')
    class Meta:
        model=Responsibility
        fields=['name','user_id','responsibleIssue_name','order']

class MyResponsibilitySerializer(serializers.ModelSerializer):
    # responsibleIssue_name = serializers.CharField(source='responsible_issue.responsible_issue_name')
    responsible_issue = serializers.SlugRelatedField(slug_field='responsible_issue_name', queryset=ResponsibleIssue.objects.all())
    class Meta:
        model=Responsibility
        fields=['responsible_issue']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.responsible_issue:
            ret['responsible_issue'] = instance.responsible_issue.responsible_issue_name

        return ret
class MyPageSerializer(serializers.ModelSerializer):
    # email=serializers.CharField(source='user.email')
    # responsibleIssue_name=serializers.CharField(source='responsible_issue.responsible_issue_name')
    responsibility=MyResponsibilitySerializer(many=True,read_only=True)
    class Meta:
        model=User
        fields=['email','responsibility']
        # fields='__all__'
        # depth = 1


    # def update(self, instance, validated_data):
    #     # print(validated_data.get('responsibleIssue_name', instance.responsibleIssue_name))
    #     # print(instance.responsibility.responsibleIssue_name)
    #     print(validated_data)
    #     responsibleIssue_datas = validated_data.pop('responsibility')
    #     # print(responsibleIssue_data.keys().index('rice'))
    #     responsibility = instance.responsibility
    #     print(instance.responsibility.all())
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()
    #     for responsibleIssue_data in responsibleIssue_datas:
    #         # responsibility=Responsibility.objects.get(responsible_issue=responsibleIssue_data.get('responsible_issue'))
    #         # print(responsibleIssue_data.get('responsible_issue').get('responsible_issue_name'))
    #         resposibleIssue=ResponsibleIssue.objects.filter(responsible_issue_name=responsibleIssue_data.get('responsible_issue')).values('responsible_issue_id')
    #
    #
    #
    #     responsibility.save()
    #
    #     return instance
class AssigneeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username',queryset=User.objects.all())

    class Meta:
        model=Assignee
        fields=['user','mension']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.user:
            ret['user'] = instance.user.name
            # ret['assignee']['user']=instance.assignee.user.name

        return ret

class MensionAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Assignee
        fields='__all__'
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.user:
            ret['user'] = instance.user.name
            # ret['assignee']['user']=instance.assignee.user.name

        return ret

class SubscribeSerializer(serializers.ModelSerializer):
    # subscriber=serializers.CharField(source='subscriber.username')
    flag=serializers.CharField(read_only=True)
    class Meta:
        model = Subscribe
        fields=['flag','subscriber','issue']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.subscriber:
            ret['subscriber'] = instance.subscriber.name
        return ret


class IssueSerializer(serializers.ModelSerializer):
    attachment=AttachmentSerializer(many=True, read_only=True)
    assignee=AssigneeSerializer(many=True)
    subscribe=SubscribeSerializer(many=True,read_only=True)
    reporter = serializers.SlugRelatedField(slug_field='username',queryset=User.objects.all())
    responsibleIssue=serializers.SlugRelatedField(slug_field='responsible_issue_name',queryset=ResponsibleIssue.objects.all())
    # board=serializers.CharField(source='board.board_id')
    # responsibility=ResponsibilitySerializer(many=True, read_only=True)
    class Meta:
        model = Issue
        # exclude=['board']
        fields = ['issue_id','reporter','board','responsibleIssue','assignee','title','content','deadline','priority','attachment','subscribe']
        # fields='__all__'
    def create(self, validated_data):
        assignees_data=validated_data.pop('assignee')
        images_data = self.context['request'].FILES
        post = Issue.objects.create(**validated_data)
        for assignee_data in assignees_data:
            # print(assignee_data)
            Assignee.objects.create(issue=post, **assignee_data)
        for image_data in images_data.getlist('image'):
            Attachment.objects.create(issue=post, image=image_data)
        return post

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.reporter and instance.responsibleIssue:
            ret['reporter'] = instance.reporter.name
            ret['responsibleIssue']=instance.responsibleIssue.responsible_issue_name
        return ret



#대댓글 재귀적으로 구현
class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data

#댓글
class CommentSerializer(serializers.ModelSerializer):
    # reply = serializers.SerializerMethodField()
    # writer=serializers.CharField(source='writer.username')
    reply = RecursiveSerializer(many=True, read_only=True)
    writer = serializers.SlugRelatedField(slug_field='username',queryset=User.objects.all())
    # writer = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='username'
    # )

    class Meta:
        model = Comment
        # fields = ('comment_id', 'parent', 'comment_content', 'reply')
        fields=['comment_id',"comment_content","writer","issue","parent","reply","created_at","updated_at"]

    # def create(self, validated_data):
    #     writer_data = validated_data.pop('writer')
    #     print(User.objects.filter(username=writer_data['username']).values('id'))
    #     # writer=User.objects.filter(username=writer_data).get('id')
    #     writer=User.objects.filter(username=writer_data).values('id')
    #     print(writer)
    #     comment=Comment.objects.create(**validated_data)
    #     # comment = Comment.objects.create(**validated_data)
    #     # # for track_data in tracks_data:
    #     User.objects.create(username=writer, **writer_data)
    #     return comment

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.writer:
            ret['writer'] = instance.writer.name
        return ret

class IssueDetailSerializer(IssueSerializer):
    comment=CommentSerializer(many=True)
    subscribe=SubscribeSerializer(many=True)
    class Meta:
        model = Issue
        fields = ['issue_id','reporter', 'assignee', 'board', 'title', 'content', 'deadline', 'priority', 'attachment','comment','subscribe']

class ShortIssueSerializer(serializers.ModelSerializer):
    assignee = AssigneeSerializer(many=True)
    class Meta:
        model = Issue
        fields = ['issue_id', 'reporter','assignee', 'title', 'board','priority','deadline']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.reporter:
            ret['reporter'] = instance.reporter.name
            # ret['assignee']['user']=instance.assignee.user.name
        return ret

class BoardSerializer(serializers.ModelSerializer):
    # issue = serializers.SeriaflizerMethodField()
    issue =ShortIssueSerializer(many=True, read_only=True)
    class Meta:
        model = Board
        fields=['board_id','project','state','order','issue']
        read_only_fields = ['order']

    # def get_issue(self, obj):
    #     queryset = Issue.objects.filter(board=obj)
    #     return IssueSerializer(queryset, many=True).data
    def create(self, validated_data):
        new_order = Board.objects.filter(project_id=validated_data['project'].project_id).count() + 1
        board__ = Board(
            state=validated_data['state'],
            project=validated_data['project'],
            order=new_order
        )
        board__.save()
        return board__


class ShortProjectSerializer(serializers.ModelSerializer):
    board_count = serializers.SerializerMethodField()
    issue_count = serializers.SerializerMethodField()
    # owner = UserSerializer(read_only=True)
    class Meta:
        model = Project
        fields = ['project_id','project_name',
                 'board_count', 'issue_count','owner']
        read_only_fields = ['owner']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.owner:
            ret['owner'] = instance.owner.username
        return ret

    def get_board_count(self, obj):
        return Board.objects.filter(project=obj).count()

    def get_issue_count(self, obj):
        lists = Board.objects.filter(project=obj)
        return Issue.objects.filter(board__in=lists).count()
    def create(self,validated_data):
        # data = validated_data.get('board_type')
        project = Project.objects.create(**validated_data)
        Board.objects.bulk_create([
            Board(project_id=project.project_id,state='할 일',order=1),
            Board(project_id=project.project_id,state='진행',order=2),
            Board(project_id=project.project_id,state='검증',order=3),
            Board(project_id=project.project_id,state='완료',order=4),

        ])
        return project

class ProjectSerializer(ShortProjectSerializer):
    boards = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['project_name', 'board_count', 'issue_count', 'boards']

    def get_boards(self, obj):
        queryset = Board.objects.filter(project=obj).order_by('order')
        return BoardSerializer(queryset, many=True).data

class FilterIssueListSerializer(IssueSerializer):
    state=serializers.CharField(read_only=True)

    class Meta:
        model = Issue
        fields='__all__'
        depth=2

class MyIssueListSerializer(IssueSerializer):
    # state=serializers.CharField(read_only=True)

    class Meta:
        model = Issue
        fields = ['issue_id', 'reporter', 'board', 'responsibleIssue', 'assignee', 'title', 'content', 'deadline',
                  'priority', 'attachment', 'subscribe']

        depth=2

class FilterBoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields='__all__'
        read_only_fields = ['order']

    def create(self, validated_data):
        new_order = Board.objects.filter(project_id=validated_data['project'].project_id).count() + 1
        board__ = Board(
            state=validated_data['state'],
            project=validated_data['project'],
            order=new_order
        )
        board__.save()
        return board__
#부서-담당이슈
# class MapDeptSerializer(serializers.ModelSerializer):
#     # dept_name = serializers.ChoiceField(choices=Department.DEPT_CHOICES)
#     # 'priority_description' 선택값 설명
#     # dept_name_description = serializers.CharField(source='get_dept_name_display', read_only=True)
#     # responsibleIssue=ResponsibleIssueSerializer()
#     class Meta:
#         model=Department
#         fields = ['dept_name']
#
# #담당이슈-유저
# class MapRespIssueSerializer(serializers.ModelSerializer):
#     # department = MapDeptSerializer()
#     class Meta:
#         model = ResponsibleIssue
#         fields=['responsible_issue_name']
#         # ,'department']
#         # fields = '__all__'

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




# #이슈(디테일)
# class IssueSerializer(serializers.ModelSerializer):
#     priority=serializers.ChoiceField(choices=Issue.PRIORITY_CHOICES)
#     #'priority_description' 선택값 설명
#     priority_description=serializers.CharField(source='get_priority_display',read_only=True)
#     class Meta:
#         model=Issue
#         fields = '__all__'


# #보드
# class BoardSerializer(serializers.ModelSerializer):
#     issue = serializers.SerializerMethodField()
#     class Meta:
#         model = Board
#         fields=['board_id','project','title','issue']
#
#     def get_issue(self, obj):
#         queryset = Issue.objects.filter(board=obj)
#         return IssueSerializer(queryset, many=True).data
#
#     def create(self, validated_data):
#         print(validated_data)
#         new_order = Board.objects.filter(project_id=validated_data['project'].project_id).count() + 1
#         board__ = Board(
#             title=validated_data['title'],
#             project=validated_data['project'],
#             # board_id=validated_data['board_id'],
#             order=new_order
#         )
#         board__.save()
#         return board__
# 프로젝트
# class ProjectSerializer(serializers.ModelSerializer):
#     # board = serializers.SerializerMethodField()
#     #
#     class Meta:
#         model=Project
#         fields=['project_id','project_name']
#
#     def create(self,validated_data):
#         # data = validated_data.get('board_type')
#         project = Project.objects.create(**validated_data)
#         print(project.project_id)
#         Board.objects.bulk_create([
#             Board(project_id=project.project_id,title='할 일'),
#             Board(project_id=project.project_id,title='진행'),
#             Board(project_id=project.project_id,title='검증'),
#             Board(project_id=project.project_id,title='완료'),
#
#         ])
#         return project