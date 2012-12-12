from articles.models import Article, ArticleAction, ACT_SUBMIT, ACT_REJECT, ACT_APPROVE, ACT_ASSIGN, ACT_CLAIM, ACT_RELEASE, ACT_PUBLISH
from django.http import HttpResponseRedirect
from django.contrib import messages

def do_action(request, queryset, code, user, error_msg, property_name, additional_filter={}, author=None, clear=[]):
    if additional_filter:
        original_qty=queryset.count()
        queryset = queryset.filter(**additional_filter)
        filtered_qty=queryset.count()
        if filtered_qty==0: 
            messages.error(request, 'The articles selected %s.' % error_msg)
            return HttpResponseRedirect('.')
        elif filtered_qty < original_qty: 
            messages.warning(request, 'Some of the articles selected %s.' % error_msg)
    if not author: author=user
    action=ArticleAction.objects.create(user=user, code=code, author=author)
    action.articles.add(*queryset)
    for p in clear: queryset.update(**{p:None})
    queryset.update(**{property_name: action})
    return HttpResponseRedirect('.')


def publish_articles(view, queryset):
    return do_action(view.request, queryset, 
        additional_filter={'approved__isnull':False},
        code=ACT_PUBLISH,
        user=view.request.user,
        error_msg="have not been approved",
        property_name='published',
    )

publish_articles.short_description = 'Publish Articles'

def claim_articles(view, queryset):
    return do_action(view.request, queryset, 
        additional_filter={'assigned__isnull':True},
        code=ACT_PUBLISH,
        user=view.request.user,
        error_msg="are not available to claim",
        property_name='assigned',
    )

claim_articles.short_description = 'Claim Articles'

def submit_articles(view, queryset):
    if view.request.user.is_staff: additional_filter={}
    else: additional_filter={'assigned__author':view.request.user}
    return do_action(view.request, queryset, 
        additional_filter=additional_filter,
        code=ACT_SUBMIT,
        user=view.request.user,
        error_msg="are not yours to submit",
        property_name='submitted',
        clear=['rejected'],
    )

submit_articles.short_description = 'Submit Articles'

def release_articles(view, queryset):
    if view.request.user.is_staff: additional_filter={}
    else: additional_filter={'assigned__author':view.request.user}
    return do_action(view.request, queryset, 
        additional_filter=additional_filter,
        code=ACT_RELEASE,
        user=view.request.user,
        error_msg="are not yours to release",
        property_name='released',
        clear=['assigned']
    )

release_articles.short_description = 'Release Articles'
