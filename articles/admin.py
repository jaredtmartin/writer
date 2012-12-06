from django.contrib import admin
from articles.models import *
from django.contrib import messages

class KeywordInline(admin.TabularInline):
    list_display = ('keyword','url', 'times')
    model = Keyword
    extra=1


def approve(modeladmin, request, queryset):
    for obj in queryset:
        try: obj.approve(user=request.user)
        except Article.ArticleWorkflowException, err: messages.add_message(request, messages.ERROR, err)

approve.short_description = "Approve selected articles"

def reject(modeladmin, request, queryset):
    for obj in queryset:
        try: obj.reject(user=request.user)
        except Article.ArticleWorkflowException, err: messages.add_message(request, messages.ERROR, err)
reject.short_description = "Reject selected articles"

def publish(modeladmin, request, queryset):
    for obj in queryset:
        try: obj.publish(user=request.user)
        except Article.ArticleWorkflowException, err: messages.add_message(request, messages.ERROR, err)
publish.short_description = "Publish selected articles"

def submit(modeladmin, request, queryset):
    for obj in queryset:
        try: obj.submit(user=request.user)
        except Article.ArticleWorkflowException, err: messages.add_message(request, messages.ERROR, err)
submit.short_description = "Submit selected articles"

def release(modeladmin, request, queryset):
    for obj in queryset:
        try: obj.release(user=request.user)
        except Article.ArticleWorkflowException, err: messages.add_message(request, messages.ERROR, err)
release.short_description = "Release selected articles"

def claim(modeladmin, request, queryset):
    for obj in queryset:
        try: obj.claim(user=request.user)
        except Article.ArticleWorkflowException, err: messages.add_message(request, messages.ERROR, err)
claim.short_description = "Claim selected articles"

def reject_and_release(modeladmin, request, queryset):
    for obj in queryset:
        try: 
            obj.reject(user=request.user)
            obj.release(user=request.user)
        except Article.ArticleWorkflowException, err: messages.add_message(request, messages.ERROR, err)
reject_and_release.short_description = "Reject and release selected articles"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name','assigned','submitted','approved','published')
#    list_filter = ('assigned','submitted','approved','published')
    list_filter=('project','minimum')
    search_fields = ['project']
    inlines = [KeywordInline]
    actions = [approve, reject, publish, submit, release, claim, reject_and_release]
    
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleType)
admin.site.register(ArticleAction)
admin.site.register(Project)
