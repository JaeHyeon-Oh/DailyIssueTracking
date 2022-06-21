from django.db import models
from ITSJwt.models import User


class Project(models.Model):
    project_id= models.AutoField(primary_key=True,unique=True)
    project_name=models.CharField(max_length=50)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owned_projects')


class Board(models.Model):
    board_id= models.AutoField(primary_key=True,unique=True)
    project =models.ForeignKey(Project, related_name='board', on_delete=models.CASCADE)
    state=models.CharField(max_length=10, blank=False, null=False)
    order=models.IntegerField()


#부서(IT실,경영지원,브랜드 전략,여신 관리)
class Department(models.Model):
    IT = 'IT'
    BUSINESS='BN'
    BRAND = 'BR'
    CREDIT = 'CD'
    # (a,b) a->DB, b->API
    DEPT_CHOICES = (
        (IT, 'IT실'),
        (BUSINESS, '경영지원'),
        (BRAND, '브랜드전략'),
        (CREDIT, '여신관리'),
    )
    dept_id= models.AutoField(primary_key=True,unique=True)
    dept_name = models.CharField(
        max_length=2,
        choices=DEPT_CHOICES,
        default=IT,
    )


class ResponsibleIssue(models.Model):
    responsible_issue_id=models.AutoField(primary_key=True,unique=True)
    department=models.ForeignKey(Department,related_name='responsibleIssue', on_delete=models.CASCADE)
    responsible_issue_name=models.CharField(max_length=50)
    def __str__(self):
        return self.responsible_issue_name


class Responsibility(models.Model):
    user = models.ForeignKey(User,related_name='responsibility', on_delete=models.CASCADE)
    responsible_issue=models.ForeignKey(ResponsibleIssue,related_name='responsibility',on_delete=models.CASCADE)
    order=models.IntegerField(default=3)


class Issue(models.Model):
    FAST = 'F'
    MEDIUM='M'
    SLOW = 'S'
    #(a,b) a->DB, b->API
    PRIORITY_CHOICES = (
        (FAST, '긴급'),
        (MEDIUM, '보통'),
        (SLOW, '여유'),
    )

    issue_id= models.AutoField(primary_key=True, unique=True)
    reporter =models.ForeignKey(User,related_name='issue',  on_delete=models.CASCADE)
    board =models.ForeignKey(Board, related_name='issue', on_delete=models.CASCADE)
    responsibleIssue =models.ForeignKey(ResponsibleIssue, related_name='issue', on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    content = models.TextField()
    # deadline = models.DateTimeField(auto_now=False)
    deadline=models.CharField(max_length=20)
    priority = models.CharField(
        max_length=2,
        choices=PRIORITY_CHOICES,
        default=MEDIUM,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Assignee(models.Model):
    user = models.ForeignKey(User,related_name='assignee', on_delete=models.CASCADE)
    issue=models.ForeignKey(Issue,related_name='assignee', on_delete=models.CASCADE)
    mension=models.BooleanField(default=False)


class Comment(models.Model):
    comment_id=models.AutoField(primary_key=True, unique=True)
    writer= models.ForeignKey(User,related_name='comment', on_delete=models.CASCADE)
    issue=models.ForeignKey(Issue,related_name='comment', on_delete=models.CASCADE)
    parent=models.ForeignKey('self', related_name='reply', on_delete=models.CASCADE, null=True, blank=True)
    comment_content=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Attachment(models.Model):
    attachment_id=models.AutoField(primary_key=True, unique=True)
    issue = models.ForeignKey(Issue,related_name='attachment', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='attachment', blank=True, null=True)


class Subscribe(models.Model):
    id=models.AutoField(primary_key=True, unique=True)
    subscriber = models.ForeignKey(User,related_name='subscribed_user', on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue,related_name='subscribe', on_delete=models.CASCADE)
    flag =models.BooleanField(default=True)


