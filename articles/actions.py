from articles.models import Article, ArticleAction, ACT_SUBMIT, ACT_REJECT, ACT_APPROVE, ACT_ASSIGN, ACT_CLAIM, ACT_RELEASE, ACT_PUBLISH
from django.http import HttpResponseRedirect
from django.contrib import messages
from forms import ActionUserID, TagForm, NoteForm
from django.contrib.auth.models import User
from django.db.models import F

def is_owner_or_staff_filter(user):
    if user.is_staff: return {}
    else: return {'owner':user}
    
def is_author_or_staff_filter(user):
    if user.is_staff: return {}
    else: return {'assigned__author':user}
    
def filter_action(request, queryset, error_msg, additional_filter={}):
    original_qty=queryset.count()
    queryset = queryset.filter(**additional_filter)
    filtered_qty=queryset.count()
    if filtered_qty==0: 
        messages.error(request, 'The articles selected %s.' % error_msg)
        return HttpResponseRedirect('.')
    elif filtered_qty < original_qty: 
        messages.warning(request, 'Some of the articles selected %s.' % error_msg)
    else: messages.info(request,'The articles have been updated successfully')
    return queryset
    
def do_action(request, queryset, code, user, error_msg, property_name=None, additional_filter={}, author=None, clear=[]):
    if additional_filter: queryset = filter_action(request, queryset,error_msg,additional_filter)

    if queryset.count() > 0:
        if not author: author=user
        action=ArticleAction.objects.create(user=user, code=code, author=author)
        action.articles.add(*queryset)
        for p in clear: queryset.update(**{p:None})
        queryset.update(last_action=action)
        if property_name: queryset.update(**{property_name: action})
    return HttpResponseRedirect('.')

#claim_articles
#assign_articles    User
#release_articles
#submit_articles
#tag_articles       Tag
#approve_articles
#reject_articles    Note
#publish_articles

def publish_articles(view, queryset):
    additional_filter = is_owner_or_staff_filter(view.request.user).update({'approved__isnull':False})
    return do_action(view.request, queryset, 
        additional_filter=additional_filter,
        code=ACT_PUBLISH,
        user=view.request.user,
        error_msg="have not been approved",
        property_name='published',
    )

publish_articles.short_description = 'Publish Articles'

def claim_articles(view, queryset):
    return do_action(view.request, queryset, 
        additional_filter={'assigned__isnull':True},
        code=ACT_CLAIM,
        user=view.request.user,
        error_msg="are not available to claim",
        property_name='assigned',
    )

claim_articles.short_description = 'Claim Articles'

def submit_articles(view, queryset):
    additional_filter = is_author_or_staff_filter(view.request.user)
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
    return do_action(view.request, queryset, 
        additional_filter={'assigned__isnull':False},
        code=ACT_RELEASE,
        user=view.request.user,
        error_msg="are not yours to release",
        property_name='released',
        clear=['assigned']
    )

release_articles.short_description = 'Release Articles'

def assign_articles(view, queryset):
    additional_filter = is_owner_or_staff_filter(view.request.user)
    additional_filter.update({'assigned__isnull':True})
    
    u=view.request.user
    print "u.username: " + str(u.username) 
    print "u: " + str(u) 
    print "is_owner_or_staff_filter(u): " + str(is_owner_or_staff_filter(u)) 
    print "is_owner_or_staff_filter(view.request.user): " + str(is_owner_or_staff_filter(view.request.user)) 
    user_select_form=ActionUserID(view.request.POST)
    if user_select_form.is_valid():
        return do_action(view.request, queryset,
            additional_filter=additional_filter,
            code=ACT_ASSIGN,
            user=view.request.user,
            author=user_select_form.cleaned_data['user'],
            error_msg="are not yours to assign or are already assigned",
            property_name='assigned',
        )
    else: 
        print "user_select_form.errors['user']: " + str(user_select_form.errors['user']) 
        messages.error(view.request, 'You did not select a valid user.')
        return HttpResponseRedirect('.')

assign_articles.short_description = 'Assign Articles'

def tag_articles(view, queryset):
    additional_filter = is_owner_or_staff_filter(view.request.user)
    tag_form=TagForm(view.request.POST)
    if tag_form.is_valid():
        queryset=filter_action(
            request=view.request,
            queryset=queryset,
            additional_filter = is_owner_or_staff_filter(view.request.user), 
            error_msg="are not yours to tag",
        )
        # This doesn't work!!! IT tries to do arithmatic, strings arent supported
        queryset.update(tags=F('tags')+tag_form.cleaned_data['tag']) 
        return HttpResponseRedirect('.')
    else: 
        messages.error(view.request, 'You did not enter a valid tag.')
        return HttpResponseRedirect('.')

tag_articles.short_description = 'Tag Articles'

def approve_articles(view, queryset):
    additional_filter = is_owner_or_staff_filter(view.request.user).update({'submitted__isnull':False})
    return do_action(view.request, queryset, 
        additional_filter=additional_filter,
        code=ACT_APPROVE,
        user=view.request.user,
        error_msg="have not been submitted or are not yours.",
        property_name='approved',
    )
approve_articles.short_description = 'Approve Articles'

def reject_articles(view, queryset):
    additional_filter = is_owner_or_staff_filter(view.request.user).update({'submitted__isnull':False})
    return do_action(view.request, queryset, 
        additional_filter=additional_filter,
        code=ACT_REJECT,
        user=view.request.user,
        error_msg="have not been submitted or are not yours.",
        property_name='approved',
        clear=['submitted','approved'],
    )
reject_articles.short_description = 'Reject Articles'

def reject_and_release_articles(view, queryset):
    additional_filter = is_owner_or_staff_filter(view.request.user).update({'submitted__isnull':False})
    return do_action(view.request, queryset, 
        additional_filter=additional_filter,
        code=ACT_REJECT,
        user=view.request.user,
        error_msg="have not been submitted or are not yours.",
        property_name='approved',
        clear=['submitted','approved','assigned'],
    )
reject_and_release_articles.short_description = 'Reject & Release Articles'
    
