from ITSJwt.models import User
from .models import Project, Department, ResponsibleIssue, Board, Issue, Assignee, Subscribe
from .models import Comment,Attachment,Responsibility
from rest_framework import serializers



class AttachmentSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model=Attachment
        fields=['image']


class ResponsibilitySerializer(serializers.ModelSerializer):
    name=serializers.CharField(source='user.name')
    user_id=serializers.CharField(source='user.username')
    class Meta:
        model=Responsibility
        fields=['name','user_id','order']


class MyResponsibilitySerializer(serializers.ModelSerializer):
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
    responsibility=MyResponsibilitySerializer(many=True,read_only=True)
    class Meta:
        model=User
        fields=['email','responsibility']


class AssigneeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username',queryset=User.objects.all())
    class Meta:
        model=Assignee
        fields=['user','mension']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.user:
            ret['user'] = instance.user.name

        return ret


class MensionAssigneeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = Assignee
        fields = ['user','issue', 'mension']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.user:
            ret['user'] = instance.user.name
        return ret


class SubscribeSerializer(serializers.ModelSerializer):
    subscriber = serializers.SlugRelatedField(slug_field='username',queryset=User.objects.all())
    flag=serializers.CharField(read_only=True)
    class Meta:
        model = Subscribe
        fields=['flag','subscriber','issue']


class IssueSerializer(serializers.ModelSerializer):
    attachment=AttachmentSerializer(many=True, read_only=True)
    assignee=AssigneeSerializer(many=True)
    subscribe=SubscribeSerializer(many=True,read_only=True)
    reporter = serializers.SlugRelatedField(slug_field='username',queryset=User.objects.all())
    responsibleIssue=serializers.SlugRelatedField(slug_field='responsible_issue_name',queryset=ResponsibleIssue.objects.all())

    class Meta:
        model = Issue
        fields = ['issue_id','reporter','board','responsibleIssue','assignee','title','content','deadline','priority','attachment','subscribe']

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
    reply = RecursiveSerializer(many=True, read_only=True)
    writer = serializers.SlugRelatedField(slug_field='username',queryset=User.objects.all())


    class Meta:
        model = Comment
        fields=['comment_id',"comment_content","writer","issue","parent","reply","created_at","updated_at"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.writer:
            ret['writer'] = instance.writer.name
        return ret


class IssueDetailSerializer(IssueSerializer):
    comment=CommentSerializer(many=True)
    subscribe=SubscribeSerializer(many=True)
    state = serializers.CharField(read_only=True)
    project_id= serializers.IntegerField(read_only=True)
    class Meta:
        model = Issue
        fields = ['issue_id','reporter', 'assignee','project_id', 'board','state', 'title', 'content', 'deadline', 'priority', 'attachment','comment','subscribe']

class ShortIssueSerializer(serializers.ModelSerializer):
    assignee = AssigneeSerializer(many=True)
    comment = CommentSerializer(many=True)
    subscribe=SubscribeSerializer(many=True,read_only=True)
    attachment_count = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['issue_id','attachment_count', 'reporter','assignee', 'title', 'board','priority','deadline','comment','subscribe']

    def get_attachment_count(self, obj):
        return Attachment.objects.filter(issue=obj).count()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.reporter:
            ret['reporter'] = instance.reporter.name
        return ret


class BoardSerializer(serializers.ModelSerializer):
    issue =ShortIssueSerializer(many=True, read_only=True)
    class Meta:
        model = Board
        fields=['board_id','project','state','order','issue']
        read_only_fields = ['order']

    def create(self, validated_data):
        # new_order = Board.objects.filter(project_id=validated_data['project'].project_id).count()-1
        project_id=validated_data['project']
        new_order=Board.objects.get(project=project_id,state__exact="닫힘").order
        Board.objects.filter(state__exact="닫힘").update(order=new_order+1)
        board__ = Board(
            state=validated_data['state'],
            project=project_id,
            order=new_order
        )
        board__.save()
        return board__


class boardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields='__all__'


class ShortProjectSerializer(serializers.ModelSerializer):
    board_count = serializers.SerializerMethodField()
    issue_count = serializers.SerializerMethodField()
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
        project = Project.objects.create(**validated_data)
        Board.objects.bulk_create([
            Board(project_id=project.project_id,state='열림', order=1),
            Board(project_id=project.project_id,state='할 일',order=2),
            Board(project_id=project.project_id,state='진행',order=3),
            Board(project_id=project.project_id,state='검증',order=4),
            Board(project_id=project.project_id,state='완료',order=5),
            Board(project_id=project.project_id,state='닫힘',order=6),

        ])
        return project


class ProjectSerializer(ShortProjectSerializer):
    boards = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['project_name', 'board_count', 'issue_count','boards']

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


class ResponsibleIssueSerializer(serializers.ModelSerializer):
    responsibility = serializers.SerializerMethodField()

    class Meta:
        model = ResponsibleIssue
        fields = ['responsible_issue_name', 'responsibility']

    def get_responsibility(self, instance):
        responsibilitys = instance.responsibility.all().order_by('order')
        return ResponsibilitySerializer(responsibilitys, many=True).data



class RespIssueSerializer(serializers.ModelSerializer):
    responsibility = serializers.SerializerMethodField()
    class Meta:
        model = ResponsibleIssue
        fields=['responsible_issue_name','responsibility']

    def get_responsibility(self, instance):
        responsibilitys = instance.responsibility.all().order_by('order')
        return ResponsibilitySerializer(responsibilitys, many=True).data
#부서
class DepartmentSerializer(serializers.ModelSerializer):
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


