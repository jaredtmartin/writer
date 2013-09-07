from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib import messages
from django.db.models import Q
from django.conf.global_settings import LANGUAGES
# from validation_plugins import *
# from plugin_manager import PluginManager
# from django.conf import settings
from HTMLParser import HTMLParser
# import facebook
import re
from django.template import Context
from plugins import PluginModel, PluginBaseMixin
#from publishing_outlets import *
def CamelToWords(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)
    
ACT_SUBMIT          = "Submitted"  # When author finishes writing
ACT_REJECT          = "Rejected"  # When the user does not accept the article
ACT_APPROVE         = "Approved" # When the user accepts the article

ACT_ASSIGN_WRITER          = "Assigned to Writer"  # When the user assigns the article to a writer
ACT_ASSIGN_REVIEWER        = "Assigned to Reviewer"  # When the user assigns the article to a reviewer
# ACT_CLAIM           = "C"   # When a writer claims an article

ACT_RELEASE         = "Released" # When a user releases an article that was either claimed or assigned
ACT_REMOVE_REVIEWER = "Removed Reviewer"
ACT_REMOVE_WRITER   = "Removed Writer"

ACT_PUBLISH         = "Published" # When the article has been published
ACT_COMMENT         = "Commented on" # When reviewing and a comment should be added

ACT_CLAIM_REVIEWER  = "Claimed by Reviewer"
ACT_CLAIM_WRITER    = "Claimed by Writer"

# These actions do not create action objects, but do appear in the button list
ACT_DELETE          = "Delete"
ACT_TAG             = "Tag"

ACTIONS = (
    (ACT_SUBMIT, 'Submitted'),
    (ACT_REJECT, 'Rejected'),
    (ACT_APPROVE, 'Approved'),
    (ACT_ASSIGN_WRITER, 'Assigned to Writer'),
    # (ACT_CLAIM, 'Claimed'),
    (ACT_RELEASE, 'Made Available'),
    (ACT_PUBLISH, 'Published'),
    (ACT_COMMENT, 'Commented On'),
    (ACT_ASSIGN_REVIEWER, 'Assigned to Reviewer'),
    (ACT_REMOVE_WRITER, 'Removed Writer'),
    (ACT_REMOVE_REVIEWER, 'Removed Reviewer'),
    (ACT_CLAIM_REVIEWER, 'Claimed by Reviewer'),
    (ACT_CLAIM_WRITER, 'Claimed by Writer'),
)
PRIORITY_LOW = 1
PRIORITY_NORMAL = 5
PRIORITY_HIGH = 10
ARTICLE_PRIORITIES = (
    (PRIORITY_LOW, 'Low Priority'),
    (PRIORITY_NORMAL, 'Normal Priority'),
    (PRIORITY_HIGH, 'High Priority'),
)
STATUS_NEW = "Unassigned"
STATUS_RELEASED = 'Released'
STATUS_ASSIGNED = 'Assigned to Writer'
STATUS_SUBMITTED = 'Submitted'
STATUS_APPROVED = 'Approved'
STATUS_PUBLISHED = 'Published'
STATUSES = (
    (STATUS_NEW, "Unassigned"),
    (STATUS_RELEASED, 'Available'),
    (STATUS_ASSIGNED, 'Assigned to Writer'),
    (STATUS_SUBMITTED, 'Submitted'),
    (STATUS_APPROVED, 'Approved'),
    (STATUS_PUBLISHED, 'Published'),
    )

WRITER_MODE = 1
REQUESTER_MODE = 2 
REVIEWER_MODE = 3

USER_MODES = (
    (WRITER_MODE, 'Writer'),
    (REQUESTER_MODE, 'Requester'),
    (REVIEWER_MODE, 'Reviewer'),
)
WRITER_POSITION = 1
REVIEWER_POSITION = 2
WORKING_POSITIONS= (
    (WRITER_POSITION, "Writer"),
    (REVIEWER_POSITION, 'Reviewer'),
)
        
class TestOutlet(PluginModel):
    package_name="articles.pkg"

class PublishingOutlet(PluginModel):
    package_name = "articles.publishing_outlets"
    title = models.CharField(max_length=256)
    
    def do_action(self, *args, **kwargs):
        return self.plugin.do_action(*args, **kwargs)
    def get_button_url(self, context=Context()):
        context.update({'title':self.title})
        return self.plugin.get_button_url(context)
    def __unicode__(self): return self.title

class ValidationPlugin(PluginModel):
    package_name = "articles.validation_plugins"
    title = models.CharField(max_length=256)
    
    def do_action(self):
        return self.plugin.do_action()
    def get_button_url(self, context=Context()):
        context.update({'title':self.title})
        return self.plugin.get_button_url(context)
    def __unicode__(self): return self.title

class UserConfigBaseModel(PluginBaseMixin, models.Model):
    class Meta:
        abstract = True
    pickled_data = models.CharField(max_length=512, default="", blank=True)
    # _data=None
    # def _get_data(self): 
    #     if self._data: return self._data
    #     import pickle
    #     import base64
    #     self._data = pickle.loads(base64.b64decode(self.pickled_data))
    #     return self._data
    # def _set_data(self,value):
    #     self._data = value
    #     import pickle
    #     import base64
    #     self.pickled_data = base64.b64encode(pickle.dumps(value))
    # data = property(_get_data, _set_data)
    # def get_setting(self, setting):
    #     return self.data[setting]
    # def set_setting(self, setting, value):
    #     self.data[setting] = value
    def __init__(self, *args, **kwargs):
        super(UserConfigBaseModel, self).__init__(*args, **kwargs)
        self.load_plugin()
        
import pickle   
class PublishingOutletConfiguration(UserConfigBaseModel):
    plugin_foreign_key_name='outlet'
    user = models.ForeignKey(User, related_name='publishing_outlets')
    outlet = models.ForeignKey(PublishingOutlet, related_name='users')

    def __unicode__(self): return "%s for %s" % (self.outlet.title, self.user.username)
    
class PluginMount(type):
    name="generic"
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = {}
        else:
            cls.plugins[cls.name]=cls

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

class ValidationProvider(object):
    __metaclass__ = PluginMount

    def is_valid(self, article, request):
        raise NotImplemented

    def strip_tags(self, html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

class ArticleType(models.Model):
    name = models.CharField(max_length=16)
    def __unicode__(self): return self.name
    
class Project(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(User, related_name='projects')
    def __unicode__(self): return self.name
    @property
    def keywords(self):
        results=[]
        [results.append(a.keywords) for a in self.articles.all()]
        return ", ".join(results)
    
class ValidationModelMixin(object):
    _validators = models.CharField(max_length=128, blank=True, default="")
#    plugin_loader=PluginManager(settings.DIRNAME+'/articles/validation_plugins/')
#    available_validators=ValidationProvider.plugins

    def validate(self):
        return all(validator.is_valid(self) for validator in self.validators)
    @property
    def validators(self):
        l=[]
        for v in self._validators.split(", "):
            if v in self.available_validators:
                l.append(self.available_validators[v]()) 
        return l           
    def get_validators_as_Str(self):
        return self._validators
    def set_validators_as_Str(self, s):
        self._validators = s
    validators_as_Str = property(get_validators_as_Str, set_validators_as_Str)
    
class ArticleAction(models.Model):
    class Meta:
        ordering = ["timestamp"]
    articles = models.ManyToManyField('Article', related_name='actions')
    # articles = models.ManyToManyField('Article', through='ArticlesActions')
    author = models.ForeignKey(User, related_name = 'authors', null=True, blank=True)  # This is the writer
    code = models.CharField(choices=ACTIONS, max_length=32)
    user = models.ForeignKey(User)                              # This is the reviewer/employer/admin
    timestamp = models.DateTimeField(auto_now_add=True)
    timezone = models.CharField(max_length=32, default="", blank=True)
    comment = models.CharField(max_length=64, default="", blank=True)
    def __unicode__(self): 
        return self.get_code_display() + " by " + self.user.get_full_name()
        
#####################################################################################################
#                                     User Properties                                               #
#####################################################################################################
def user_full_name(self):
    return "%s %s" % (self.first_name,self.last_name)
User.full_name = property(user_full_name)
def user_writers(self):
    return User.objects.filter(contacts_as_worker__position=WRITER_POSITION, contacts_as_worker__requester=self, contacts_as_worker__confirmation=True).distinct()
User.writers = property(user_writers)
def user_writer_contacts(self):
    return self.contacts_as_requester.filter(confirmation=True, position=WRITER_POSITION)
User.writer_contacts = property(user_writer_contacts)
def user_reviewers(self):
    return User.objects.filter(contacts_as_worker__position=REVIEWER_POSITION, contacts_as_worker__requester=self, contacts_as_worker__confirmation=True).distinct()
User.reviewers = property(user_reviewers)
def user_requester_contacts(self):
    return self.contacts_as_worker.filter(confirmation=True)
User.requester_contacts = property(user_requester_contacts)
def user_writes_for(self):
    return self.contacts_as_worker.filter(confirmation=True, position=WRITER_POSITION)
User.writes_for = property(user_writes_for)
def user_reviews_for(self):
    return self.contacts_as_worker.filter(confirmation=True, position=REVIEWER_POSITION)
User.reviews_for = property(user_reviews_for)
def user_reviewer_contacts(self):
    return self.contacts_as_requester.filter(confirmation=True, position=REVIEWER_POSITION)
User.reviewer_contacts = property(user_reviewer_contacts)
def user_writing_contacts(self):
    return list(set([c.name for c in self.contacts_as_worker.filter(position=WRITER_POSITION)]))
User.writing_contacts = property(user_writing_contacts)
def user_reviewing_contacts(self):
    return list(set([c.name for c in self.contacts_as_worker.filter(position=REVIEWER_POSITION)]))
User.reviewing_contacts = property(user_reviewing_contacts)
def user_articles_available_to_write(self):
    return Article.objects.filter(Q(writer_availability__in=self.writing_contacts)|Q(writer_availability=""))
User.articles_available_to_write = property(user_articles_available_to_write)
def user_articles_available_to_review(self):
    return Article.objects.filter(Q(reviewer_availability__in=self.reviewing_contacts)|Q(reviewer_availability=""))
User.articles_available_to_review = property(user_articles_available_to_review)
def user_in_writing_mode(self):
    if self.mode == WRITER_MODE:return True
User.in_writing_mode = property(user_in_writing_mode) 
def user_in_reviewing_mode(self):
    if self.mode == REVIEWER_MODE:return True
User.in_reviewing_mode = property(user_in_reviewing_mode) 
def user_in_requester_mode(self):
    if self.mode == REQUESTER_MODE:return True
User.in_requester_mode = property(user_in_requester_mode) 

# def get_writers(self):
#     return self.objects.filter(contacts_as_worker__position=WRITER_POSITION, contacts_as_worker__confirmation=True).distinct()
# User.writers = property(get_writers) 
# def get_reviewers(self):
#     return self.objects.filter(contacts_as_worker__position=REVIEWER_POSITION, contacts_as_worker__confirmation=True).distinct()
# User.reviewers = property(get_reviewers) 


# def user_outlets(self):
#     return self.relationships_as_requester.filter(confirmed=True, reviewer__isnull=False)
# User.outlets = property(user_outlets)

def get_user_mode(self):
    return self.get_profile().mode
def set_user_mode(self, value):
    p = self.get_profile()
    p.mode = value
    p.save()
User.mode=property(get_user_mode, set_user_mode)

def get_user_mode_display(self):
    return self.get_profile().get_mode_display()
User.mode_display = property(get_user_mode_display)

#####################################################################################################
#                                     Contacts                                                      #
#####################################################################################################
class Contact(models.Model):
    name = models.CharField(max_length=64)
    requester = models.ForeignKey(User, related_name='contacts_as_requester')
    worker = models.ForeignKey(User, related_name='contacts_as_worker')
    user_asked = models.ForeignKey(User, related_name='contact_requests')
    position = models.IntegerField(choices=WORKING_POSITIONS)
    confirmation = models.NullBooleanField(default=None, blank=True)
    @property
    def verb(self):
        if self.position==WRITER_POSITION: return "write"
        elif self.position==REVIEWER_POSITION: return "review"
        else: return "works"
    def __unicode__(self):
        if self.confirmation:
            if self.name == self.worker.full_name:
                return "%s %ss for %s" % (self.worker.full_name, self.verb, self.requester.full_name)
            else:
                return "%s %ss for %s as %s" % (self.worker.full_name, self.verb, self.requester.full_name, self.name)
        else:
            if self.confirmation == None:
                if self.user_asked==self.requester: 
                    return "%s requested to %s for %s" % (self.worker.full_name, self.verb, self.requester.full_name)
                else:
                    return "%s requested %s to %s for him" % (self.requester.full_name, self.worker, self.verb)
            else:
                if self.user_asked==self.requester: 
                    return "%s was not accepted to %s for %s" % (self.worker.full_name, self.verb, self.requester.full_name)
                else:
                    return "%s declined to %s for %s" % (self.worker.full_name, self.verb, self.requester.full_name)

#####################################################################################################
#                                     Articles                                                      #
#####################################################################################################
class NotDeletedManager(models.Manager):
    def get_query_set(self):
        return super(NotDeletedManager, self).get_query_set().filter(deleted=False)

class ArticleManager(NotDeletedManager):
    def filter_valid(self, request):
        qs = super(ArticleManager, self).get_query_set()
        article_pk_list = list(Article.objects.all().values_list('id', flat=True))
        print "article_pk_list = %s" % str(article_pk_list)
        for validation in ValidationPlugin.objects.all():
            for article in qs:
                if not validation.plugin.is_valid(article, request): 
                    try: article_pk_list.remove(article.pk)
                    except ValueError:pass
        return Article.objects.filter(pk__in=article_pk_list)

class Category(models.Model):
    name = models.CharField(max_length=64)
    def __unicode__(self): 
        return self.name

class Article(ValidationModelMixin, models.Model):
    def __unicode__(self): return self.name
    minimum     = models.IntegerField(default=100)
    priority    = models.IntegerField(default=PRIORITY_NORMAL, choices = ARTICLE_PRIORITIES)
    maximum     = models.IntegerField(default=0) # Use zero for no maximum
    body        = models.TextField(blank=True, default="")
    title       = models.CharField(max_length=256, blank=True, default="")
    article_type = models.ForeignKey(ArticleType, related_name='articles')
    project     = models.ForeignKey(Project, related_name='articles', null=True, blank=True)
    category     = models.ForeignKey(Category, related_name='articles', null=True, blank=True)
    tags        = models.CharField(max_length=128, blank=True, default="")
    status      = models.CharField(max_length=32, blank=True, default=STATUS_NEW, choices=STATUSES)
    owner       = models.ForeignKey(User, related_name='articles_owned')
    writer      = models.ForeignKey(User, null=True, blank=True, related_name='articles_writing')
    reviewer    = models.ForeignKey(User, null=True, blank=True, related_name='articles_reviewing')
    
    last_action = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='last_action_articles')
    published   = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='published_articles')
    approved    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='approved_articles')
    submitted   = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='submitted_articles')
    # assigned    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='assigned_articles')
    rejected    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='rejected_articles')
    # released    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='released_articles')
    was_claimed = models.BooleanField(default=False)

    expires = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False, blank=True)
    # released = models.BooleanField(default=False, blank=True)
    description = models.TextField(max_length=256, blank=True, default="")
    article_notes = models.CharField(max_length=128, blank=True, default="")
    review_notes = models.CharField(max_length=128, blank=True, default="")
    referrals = models.CharField(max_length=128, blank=True, default="")
    purpose = models.CharField(max_length=128, blank=True, default="")
    price = models.CharField(max_length=128, blank=True, default="")
    language = models.CharField(max_length=7, choices=LANGUAGES, blank=True, default="en")
    style = models.CharField(max_length=128, blank=True, default="")
    writer_availability = models.CharField(max_length=64, blank=True, default="Nobody")
    reviewer_availability = models.CharField(max_length=64, blank=True, default="Nobody")
    objects = ArticleManager()
    all_objects = models.Manager()
    def get_assignment_status(self, assigned, availability):
        if assigned:
            return "Assigned to %s" % assigned.full_name
        elif availability == "Nobody":
            return "Unavailable"
        elif availability=="":
            return "Available to Everybody"
        else:
            return "Available to %s" % availability
    @property
    def can_edit(self, user):
        if (user.is_staff or user == self.owner) and self.submitted ==False: return True
        if user == self.writer and not self.approved and not self.rejected: return True
        if user == self.reviewer and self.submitted: return True
        return False
    @property
    def writer_status(self): return self.get_assignment_status(self.writer, self.writer_availability)
    @property
    def reviewer_status(self): return self.get_assignment_status(self.reviewer, self.reviewer_availability)

    @classmethod
    def filter_valid(self, qs, request):
        article_pk_list = list(qs.values_list('id', flat=True))
        for article in qs:
            if not article.is_valid(request): article_pk_list.remove(article.pk)
        return Article.objects.filter(pk__in=article_pk_list)

    def is_valid(self, request):
        for validation in ValidationPlugin.objects.all():
            if not validation.plugin.is_valid(self, request): return False
        return True
    def submit(self, request):
        if not self.submitted and request.user == self.writer: 
            if self.is_valid(request):
                action = ArticleAction.objects.create(user=request.user, author=request.user, code=ACT_SUBMIT)
                self.last_action=action
                self.submitted = action
                self.status = STATUS_SUBMITTED
                self.save()
            else: messages.error(request, "We were unable to submit the article due to the errors encountered")
    def approve(self, user):
        if self.submitted and (user==self.owner or user==self.reviewer) and not self.approved: 
            action = ArticleAction.objects.create(user=user, author=self.writer, code=ACT_APPROVE)
            self.last_action=action
            self.approved = action
            self.status = STATUS_APPROVED
            self.save()
    def get_tags(self):
        return self.tags.split(',')
    def set_tags(self, value):
        if type(value)==list:
            self.tags=",".join(set(value))
        else: self.tags=value
    tags_as_list=property(get_tags, set_tags)
    def make_available_to_writer(self, contact):
        self.writer_availability = contact.name
    def make_available_to_reviewer(self, contact):
        self.reviewer_availability = contact.name
    # @property
    # def status(self): 
    #     if self.published: return STATUS_PUBLISHED
    #     if self.approved: return STATUS_APPROVED
    #     if self.submitted: return STATUS_SUBMITTED
    #     if self.writer: return STATUS_ASSIGNED
    #     if self.released: return STATUS_RELEASED
    #     return STATUS_NEW
    
    class ArticleWorkflowException(Exception): pass
    # ATTRIBUTES={'publish':ACT_PUBLISH,'approved':ACT_APPROVE,'submitted':ACT_SUBMIT,'assigned':ACT_ASSIGN,'rejected':ACT_REJECT,'released':ACT_RELEASE}
    def get_available_actions(self, user):
        status = self.status
        actions=[]
        if not user.is_authenticated(): return []
        if user.mode == WRITER_MODE:
            contact_names = [c.name for c in self.owner.writer_contacts.filter(worker=user)]
            if self.writer == user and not self.submitted:
                actions += [ACT_REMOVE_WRITER, ACT_SUBMIT]

            elif not self.writer and (self.writer_availability in contact_names or not self.writer_availability):
                actions += [ACT_CLAIM_WRITER]
        elif user.mode == REQUESTER_MODE and user==self.owner:
            if   status == STATUS_APPROVED:     actions.append(ACT_PUBLISH)
            elif status == STATUS_SUBMITTED:    actions += [ACT_REJECT, ACT_APPROVE]
            # elif status == STATUS_ASSIGNED:     actions.append(ACT_REMOVE_WRITER)
            # elif status == STATUS_RELEASED:     actions.append(ACT_ASSIGN_WRITER)
            # else:                               actions.append(ACT_RELEASE)
            # if not self.approved:
                # actions += [ACT_DELETE]
                # if self.reviewer:
                #     actions += [ACT_REMOVE_REVIEWER]
                # else:
                #     actions += [ACT_ASSIGN_REVIEWER]
            # actions += (ACT_TAG, )
        elif user.mode == REVIEWER_MODE:
            contact_names = [c.name for c in self.owner.reviewers.filter(worker=user)]
            if self.reviewer == user and status == STATUS_SUBMITTED:
                actions += [ACT_REMOVE_REVIEWER, ACT_REJECT, ACT_APPROVE]
            elif not self.reviewer and \
            (self.reviewer_availability in contact_names or not self.reviewer_availability): 
                actions += [ACT_CLAIM_REVIEWER]
        return actions
            
    @property
    def klass(self):return self.article_type.name
    @property
    def keywords(self):
        return ", ".join([k.keyword for k in self.keyword_set.all()])
    @property
    def name(self):
        if self.title: return self.title
        if self.maximum > 0: length=u" (" + str(self.minimum) + u" - " + str(self.maximum) + u" words)"
        else: length = u" (" + str(self.minimum) + u" words)"
        return self.keywords + length
    @models.permalink
    def get_absolute_url(self):
        return ('article_update', [self.id,])
    @models.permalink
    def get_tag_url(self):
        return ('tag_article', [self.id,])
    @models.permalink
    def get_claim_url(self):
        return ('article_claim', [self.id,])
    @models.permalink
    def get_accept_url(self):
        return ('accept_article', [self.id,])
    @models.permalink
    def get_submit_url(self):
        return ('article_submit', [self.id,])
    @models.permalink
    def get_release_url(self):
        return ('article_release', [self.id,])
    @models.permalink
    def get_assign_url(self):
        return ('article_assign', [self.id,])
    @models.permalink
    def get_reject_url(self):
        return ('article_reject', [self.id,])
    @models.permalink
    def get_delete_url(self):
        return ('article_delete', [self.id,])

class ArticleMessage(models.Model):
    msg         = models.CharField(max_length=256)
    article     = models.ForeignKey(Article, related_name='messages')
    # is_sticky   = models.BooleanField(default=False, blank=True)

class Keyword(models.Model):
    article = models.ForeignKey(Article)
    keyword = models.CharField(max_length=32)
    url = models.CharField(max_length=64)
    times = models.IntegerField(default=1)
    def __unicode__(self): return self.keyword
    
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    timezone = models.CharField(max_length=32, default='America/Chicago')
    access_token = models.TextField(blank=True, help_text='Facebook token for offline access', null=True)
    mode = models.IntegerField(choices=USER_MODES)
    article_list_view = models.CharField(max_length=32, blank=True, default='')
    def __unicode__(self): return self.user.username+"'s profile"
    project_filter_value = models.CharField(max_length=64, blank=True, default='')
    writer_filter_value = models.CharField(max_length=64, blank=True, default='')
    @property
    def is_requester(self):
        return self.mode == REQUESTER_MODE
    @property
    def is_writer(self):
        return self.mode == WRITER_MODE
    @property
    def is_reviewer(self):
        return self.mode == REVIEWER_MODE
    # @property
    # def graph(self): return facebook.GraphAPI(self.access_token)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, mode=WRITER_MODE)

post_save.connect(create_user_profile, sender=User)


