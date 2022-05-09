from rest_framework import serializers
from .models import Project,Department,User,ResponsibleIssue,Board,Issue
from .models import Responsibility,Comment,Attachment,Subscribe

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'

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
        fields='__all__'


    def create(self,validated_data):
        data = validated_data.get('board_type')
        project = Project.objects.create(**validated_data)
        print(project.project_id)
        if  data=='개발':
            Board.objects.bulk_create([
                Board(project_id=project.project_id,title='할 일'),
                Board(project_id=project.project_id,title='진행'),
                Board(project_id=project.project_id,title='검증'),
                Board(project_id=project.project_id,title='완료'),

            ])
        else:
            Board.objects.bulk_create([
                Board(project_id=project.project_id, title='할 일'),
                Board(project_id=project.project_id, title='진행'),
                Board(project_id=project.project_id, title='완료'),

            ])

        return project
# #보드
# class BoardSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model=Board
#         fields='__all__'
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
    # dept = serializers.IntegerField(read_only=True)
    # responsibleIssue=MapRespIssueSerializer()
    # def update(self, instance, validated_data):
    #     # profile_data = validated_data.pop('responsibleIssue')
    #     # profile = instance.responsibleIssue
    #
    #     # print(instance.responsibleIssue.department_id)
    #     # instance.user_id = validated_data.get('user_id', instance.user_id)
    #     instance.email = validated_data.get('email', instance.email)
    #     # profile=ResponsibleIssue.objects.get(responsible_issue_name=profile_data.get('responsible_issue_name'))
    #
    #     # instance.responsibleIssue_id = ResponsibleIssue.objects.filter(
    #     #     responsible_issue_name=profile.responsible_issue_name
    #     # )[0].responsible_issue_id
    #     # print(instance.responsibleIssue_id)
    #     instance.save()
    #     # profile.responsible_issue_id = instance.responsibleIssue_id
    #     # print(profile.responsible_issue_id)
    #
    #
    #     # profile.save()
    #     return instance

    class Meta:
        model=User
        fields = ['email']
        # ,'responsibleIssue']


class AuthLoginSerializer(serializers.ModelSerializer):
    # dept=serializers.CharField(source='responsibleIssue.department.dept_name')
    # print(dept)
    class Meta:
        model=User
        fields = ['user_id','name']
        # ,'dept']



# #프로젝트
# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Project
#         fields = '__all__'


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
        fields = ('comment_id', 'parent', 'comment_content', 'reply')

    # def get_reply(self, instance):
    #     # recursive
    #     serializer = self.__class__(instance.reply, many=True)
    #     serializer.bind('', self)
    #     return serializer.data