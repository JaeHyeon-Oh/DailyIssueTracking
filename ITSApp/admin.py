from django.contrib import admin
from .models import Issue, Attachment, Project, Board, Assignee, Subscribe, ResponsibleIssue, Department, Responsibility


class ImageInline(admin.TabularInline):
    model = Attachment
    extra = 0

class AssigneeInline(admin.TabularInline):
    model = Assignee
    extra = 0

class SubscribeInline(admin.TabularInline):
    model = Subscribe
    extra = 0

class BoardInline(admin.TabularInline):
    model = Board
    extra = 0

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title','get_state','get_reporter','get_assignee','priority','deadline')
    list_filter = ('board__project__project_name','created_at',)
    search_fields = ('reporter__name','title',)
    inlines = [AssigneeInline,ImageInline,SubscribeInline ]
    ordering=('-created_at',)
    fields = ['reporter',('board','responsibleIssue'),'title','content',('deadline','priority'),]
    def get_reporter(self,obj):
        return obj.reporter.name

    def get_assignee(self,obj):
        return [i.user.name for i in Assignee.objects.filter(issue=obj) if i.mension !=True]

    def get_state(self,obj):
        return obj.board.state



class IssueInline(admin.TabularInline):
    model=Issue
    extra = 0

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('board_id', 'state', 'order',)
    list_filter = ('project__project_name',)
    search_fields = ('state',)
    ordering = ['order']
    inlines = (IssueInline,)



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id','project_name','get_owner',)
    search_fields = ('owner__name', 'project_name',)
    inlines = [BoardInline]

    def get_owner(self,obj):
        return obj.owner.name

class ResponsibleIssueInline(admin.TabularInline):
    model = ResponsibleIssue
    extra = 0

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_id','dept_name',)
    search_fields = ('dept_name',)
    list_filter = ('dept_name',)
    inlines = [ResponsibleIssueInline]

@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    list_display = ('id','get_user','get_responsible_issue','order',)
    search_fields = ('get_user','get_responsible_issue',)
    ordering = ['order']

    def get_user(self,obj):
        return obj.user.name

    def get_responsible_issue(self,obj):
        return obj.responsible_issue.responsible_issue_name