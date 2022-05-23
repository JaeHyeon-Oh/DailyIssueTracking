from django.db import models
from ITSJwt.models import User


class Project(models.Model):
    project_id= models.AutoField(primary_key=True,unique=True)
    project_name=models.CharField(max_length=50)


class Board(models.Model):
    board_id= models.AutoField(primary_key=True,unique=True)
    project =models.ForeignKey(Project, related_name='board', on_delete=models.CASCADE)
    title=models.CharField(max_length=10, blank=False, null=False)


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
    user =models.ForeignKey(User,related_name='issue',  on_delete=models.CASCADE)
    board =models.ForeignKey(Board, related_name='issue', on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    content = models.TextField()
    deadline = models.DateTimeField(auto_now=False)
    priority = models.CharField(
        max_length=2,
        choices=PRIORITY_CHOICES,
        default=MEDIUM,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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





class Token(models.Model):
    username=models.CharField(max_length=40,primary_key=True,unique=True)
    key = models.CharField( max_length=40,unique=True)
    # name=models.CharField(max_length=40)


class ResponsibleIssue(models.Model):
    responsible_issue_id=models.AutoField(primary_key=True,unique=True)
    user = models.ForeignKey(User,related_name='responsibleIssue', on_delete=models.CASCADE)
    department=models.ForeignKey(Department,related_name='responsibleIssue', on_delete=models.CASCADE)
    responsible_issue_name=models.CharField(max_length=50)

class Responsibility(models.Model):

    Responsibility_id=models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # issue= models.ForeignKey(Issue,related_name='responsibility', on_delete=models.CASCADE)
    responsible_issue=models.OneToOneField(ResponsibleIssue,related_name='responsibility', on_delete=models.CASCADE)
    responsibility_type=models.CharField(max_length=20)

class Comment(models.Model):
    comment_id=models.AutoField(primary_key=True, unique=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    issue=models.ForeignKey(Issue, on_delete=models.CASCADE)
    parent=models.ForeignKey('self', related_name='reply', on_delete=models.CASCADE, null=True, blank=True)
    comment_content=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Attachment(models.Model):
    attachment_id=models.AutoField(primary_key=True, unique=True)
    issue = models.ForeignKey(Issue,related_name='attachment', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='attachment', blank=True, null=True)

class Subscribe(models.Model):
    subscribe_id=models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

# class User(models.Model):
#     user_id=models.CharField(primary_key=True,max_length=50,unique=True)
#     email=models.EmailField(unique=True)
#     # department=models.ForeignKey(Department, related_name='user',on_delete=models.CASCADE,null=True,blank=True)
#     # responsibleIssue = models.OneToOneField(ResponsibleIssue,related_name='user', on_delete=models.SET_NULL,null=True)
#     name=models.CharField(max_length=50,null=True)
#     picture=models.URLField(max_length=2000,null=True)