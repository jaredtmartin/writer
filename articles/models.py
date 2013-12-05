from django.db import models
from django.contrib.auth.models import User, AnonymousUser
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

    def get_button_url(self, context=Context()):
      context.update({'title':self.title})
      return self.plugin.get_button_url(context)
    @property
    def settings(self):
      return self.plugin.settings
    @property
    def connected(self):
      return bool(self.plugin)
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
import json
class UserConfigBaseModel(PluginBaseMixin, models.Model):
  _config = None
  class Meta:
    abstract = True
  json_data = models.CharField(max_length=512, default="", blank=True)
  def __init__(self, *args, **kwargs):
    super(UserConfigBaseModel, self).__init__(*args, **kwargs)
    self.load_plugin()
  def config():
      doc = "The config property."
      def fget(self):
          if self._config: return self._config
          try: self._config = json.loads(self.json_data)
          except ValueError: self._config={x:"" for x in self.outlet.settings}
          return self._config
      def fset(self, value):
          self._config = value
          self.json_data = json.dumps(value)
      return locals()
  config = property(**config())

class PublishingOutletConfiguration(UserConfigBaseModel):
  plugin_foreign_key_name='outlet'
  name = models.CharField(max_length=32, default="")
  user = models.ForeignKey(User, related_name='publishing_outlets')
  outlet = models.ForeignKey(PublishingOutlet, related_name='users')
  active = models.BooleanField(default=False, blank=True)
  # The following are for 
  token = models.CharField(max_length=64, default="")
  secret = models.CharField(max_length=64, default="")
  def __unicode__(self): return "%s for %s" % (self.outlet.title, self.user.username)
  # def fetch_oauth_token(self):
  #   token, secret = self.outlet.plugin.get_oauth_token()
  #   config = self.config
  #   config['oauth_token'] = token
  #   config['oauth_secret'] = secret
  #   self.config = config

  # @property
  # def oauth_token(self):
  #   if 'oauth_token' in self.config and self.config['oauth_token']: return self.config['oauth_token']
  #   self.fetch_oauth_token()
  #   return self.config['oauth_token']
  # @property
  # def oauth_secret(self):
  #   if 'oauth_secret' in self.config and self.config['oauth_secret']: return self.config['oauth_secret']
  #   self.fetch_oauth_token()
  #   self.config['oauth_secret']
  @property
  def oauthrequsttoken(self):
    try: return OAuthRequestToken.objects.get(config_id=self.id)
    except OAuthRequestToken.DoesNotExist: return None
  @property
  def oauth_url(self):
    if not self.oauthrequsttoken:
      token, secret = self.outlet.plugin.get_oauth_request_token()
      url = self.outlet.plugin.get_oauth_request_url(token)
      OAuthRequestToken.objects.create(token=token, config=self, secret=secret, url=url)
    return self.oauthrequsttoken.url
    # def do_action(self, articles):
    #   print "XXXX IMHERE"
    #   print "self = %s" % str(self)
    #   print "self.outlet.plugin = %s" % str(self.outlet.plugin)
    #   print "article_qs = %s" % str(article_qs)
    #   c=self.config
    #   print "self.config = %s" % str(self.config)
    #   return self.outlet.plugin.do_action(self.config, article_qs)
    
class OAuthRequestToken(models.Model):
  token = models.CharField(max_length=64)
  secret = models.CharField(max_length=64)
  url = models.CharField(max_length=300)
  config = models.OneToOneField(PublishingOutletConfiguration)

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

################################################################################
       ###   ###  #   # #####   #    ###  #####  ####
      #   # #   # ##  #   #    # #  #   #   #   #    
      #     #   # # # #   #    ###  #       #    ### 
      #   # #   # #  ##   #   #   # #   #   #       #
       ###   ###  #   #   #   #   #  ###    #   #### 
################################################################################
class Contact(models.Model):
  user_asked = models.ForeignKey(User, related_name='contact_requests', blank=True)
  confirmation = models.NullBooleanField(default=None, blank=True)
  def __unicode__(self): 
    try: 
      r=self.writer.requester
      w=self.writer.writer
      v="write"
    except Writer.DoesNotExist:
      try:
        r=self.reviewer.requester
        w=self.reviewer.reviewer
        v="review"
      except: 
        return "Contact without details"
    if self.confirmation: return "%s %ss for %s" % (w,v,r)
    elif self.user_asked == r: return "%s requested to %s for %s" % (w,v,r)
    return "%s requested that %s %s" % (r,w,v)

class Writer(Contact):
  @property
  def worker(self): return self.writer
  requester = models.ForeignKey(User, related_name='writers')
  writer = models.ForeignKey(User, related_name='contacts_as_writer')
  def __unicode__(self): 
    if self.confirmation: return "%s writes for %s" % (self.writer, self.requester)
    elif self.user_asked == self.requester: return "%s requested to write for %s"% (self.writer, self.requester)
    elif self.user_asked == self.writer: return "%s requested %s to write"% (self.requester, self.writer)


class Reviewer(Contact): 
  @property
  def worker(self): return self.reviewer
  requester = models.ForeignKey(User, related_name='reviewers')
  reviewer = models.ForeignKey(User, related_name='contacts_as_reviewer')
  def __unicode__(self): 
    if self.confirmation: return "%s reviews for %s" % (self.reviewer, self.requester)
    elif self.user_asked == self.requester: return "%s requested to review for %s"% (self.reviewer, self.requester)
    elif self.user_asked == self.reviewer: return "%s requested %s to review"% (self.requester, self.reviewer)

class ContactGroup(models.Model):
  contacts = models.ManyToManyField(Contact)
  name = models.CharField(max_length=32)
  # position = models.IntegerField(choices=WORKING_POSITIONS)
  def __unicode__(self): return self.name
class WriterGroup(ContactGroup):
  owner = models.ForeignKey(User, related_name='writer_groups')
class ReviewerGroup(ContactGroup): 
  owner = models.ForeignKey(User, related_name='reviewer_groups')
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

class Availability(models.Model):
  contact = models.ForeignKey(Contact, null=True, blank=True)
  group = models.ForeignKey(ContactGroup, null=True, blank=True)
  article = models.ForeignKey('Article')
  def __unicode__(self): 
    positions={1:'write',2:'review'}
    if self.contact: return "Available to %s to %s." % (self.contact.worker.full_name, positions[self.contact.position])
    elif self.group: return "Available to %s group to %s." % (self.group.name, positions[self.group.position])

        
################################################################################
      #   #  #### ##### ####        ####  ####   ###  ####   ####
      #   # #     #     #   #       #   # #   # #   # #   # #    
      #   #  ###  ####  ####        ####  ####  #   # ####   ### 
      #   #     # #     #   #       #     #   # #   # #         #
       ###  ####  ##### #   #       #     #   #  ###  #     #### 
################################################################################

def user_full_name(self):
    return "%s %s" % (self.first_name,self.last_name)
User.full_name = property(user_full_name)
# def user_writers(self):
#     return User.objects.filter(contacts_as_worker__position=WRITER_POSITION, contacts_as_worker__requester=self, contacts_as_worker__confirmation=True).distinct()
# User.writers = property(user_writers)
# def user_writer_contacts(self):
#     return self.writers.filter(confirmation=True)
# User.writer_contacts = property(user_writer_contacts)
# def user_reviewers(self):
#     return User.objects.filter(contacts_as_worker__position=REVIEWER_POSITION, contacts_as_worker__requester=self, contacts_as_worker__confirmation=True).distinct()
# User.reviewers = property(user_reviewers)
# def user_requester_contacts(self):
#     return self.contacts_as_worker.filter(confirmation=True)
# User.requester_contacts = property(user_requester_contacts)
# def user_writes_for(self):
#     return self.contacts_as_worker.filter(confirmation=True, position=WRITER_POSITION)
# User.writes_for = property(user_writes_for)
# def user_reviews_for(self):
#     return self.contacts_as_worker.filter(confirmation=True, position=REVIEWER_POSITION)
# User.reviews_for = property(user_reviews_for)
# def user_reviewer_contacts(self):
#     return self.contacts_as_requester.filter(confirmation=True, position=REVIEWER_POSITION)
# User.reviewer_contacts = property(user_reviewer_contacts)
# def get_anon_reviewer_contacts(self): return Reviewer.objects.none()
# AnonymousUser.reviewer_contacts = property(get_anon_reviewer_contacts)
# def get_anon_writer_contacts(self): return Writer.objects.none()
# AnonymousUser.writer_contacts = property(get_anon_writer_contacts)
# def user_writing_contacts(self):
#     return list(set([c.name for c in self.contacts_as_worker.filter(position=WRITER_POSITION)]))
# User.writing_contacts = property(user_writing_contacts)
# def user_reviewing_contacts(self):
#     return list(set([c.name for c in self.contacts_as_worker.filter(position=REVIEWER_POSITION)]))
# User.reviewing_contacts = property(user_reviewing_contacts)
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

class WriterUsersManager(object):
  def all(self): 
    return User.objects.filter(Q(contacts_as_writer__isnull=False)|Q(userprofile__mode=WRITER_MODE)).distinct()
class ReviewerUsersManager(object):
  def all(self): 
    return User.objects.filter(Q(contacts_as_reviewer__isnull=False)|Q(userprofile__mode=REVIEWER_MODE)).distinct()
User.writer_users = WriterUsersManager()
User.reviewer_users=ReviewerUsersManager()
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

################################################################################
        #   ####  ##### #####  ###  #     #####  ####
       # #  #   #   #     #   #   # #     #     #    
       ###  ####    #     #   #     #     ####   ### 
      #   # #   #   #     #   #   # #     #         #
      #   # #   #   #   #####  ###  ##### ##### #### 
################################################################################

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
  _can_write = {}
  _can_review = {}
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
  writer      = models.ForeignKey(Writer, null=True, blank=True, related_name='articles_writing')
  reviewer    = models.ForeignKey(Reviewer, null=True, blank=True, related_name='articles_reviewing')
  # available_to_contacts = models.ManyToManyField(Contact, through='Availability')
  available_to_all_writers = models.BooleanField(default=False, blank=True)
  available_to_all_my_writers = models.BooleanField(default=False, blank=True)
  available_to_all_reviewers = models.BooleanField(default=False, blank=True)
  available_to_all_my_reviewers = models.BooleanField(default=False, blank=True)
  # available_to_groups = models.ManyToManyField(ContactGroup, through='Availability')
  last_action = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='last_action_articles')
  published   = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='published_articles')
  approved    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='approved_articles')
  submitted   = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='submitted_articles')
  # assigned    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='assigned_articles')
  rejected    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='rejected_articles')
  # released    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='released_articles')
  was_claimed = models.BooleanField(default=False)
  writers = models.ManyToManyField(Writer, related_name ='articles_available_to_me_to_write', blank=True, null=True)
  reviewers = models.ManyToManyField(Reviewer, related_name ='articles_available_to_me_to_review', blank=True, null=True)
  writer_groups = models.ManyToManyField(WriterGroup, null=True, blank=True, related_name ='articles_available_to_group_to_write')
  reviewer_groups = models.ManyToManyField(ReviewerGroup, null=True, blank=True, related_name ='articles_available_to_group_to_review')
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
  # writer_availability = models.CharField(max_length=64, blank=True, default="Nobody")
  # reviewer_availability = models.CharField(max_length=64, blank=True, default="Nobody")
  objects = ArticleManager()
  all_objects = models.Manager()
  def get_assignment_status(self, position, assigned, contacts, groups, all_mine, everyone):
    if assigned:
      if self.was_claimed: return "Claimed by %s" % assigned.worker.full_name
      else: return "Assigned to %s" % assigned.worker.full_name
    elif not (contacts or groups or all_mine or everyone):
      return "Unavailable"
    elif contacts:
      if len(contacts)==1: return "Available to %s" % contacts[0].worker.full_name
      else: return "Available to %s writers" % len(contacts)
    elif groups:
      if len(groups)==1: return "Available to %s" % groups[0].name
      else: return "Available to %s groups" % len(groups)
      return msg
    elif all_mine: return "Available to all my %ss" % position
    elif everyone: return "Available to all %ss" % position
    # return "XXX"
  # @property
  # def can_write(self, user):
  #   if user.pk in self._can_write: return self._can_write[user.pk]
  #   self._can_write[user.pk] = self.get_can_write(user)
  # def get_can_write(self, user):
  #   if (user.is_staff or user == self.owner): return True
  #   if self.submitted == None and self.writer:
  #     if user == self.writer: return True
  #     if self.writers.filter(writer=user): return True
  #     if self.writer_groups.filter(writer)

  @property
  def can_edit(self, user):
    if (user.is_staff or user == self.owner) and self.submitted ==False: return True
    if user == self.writer and not self.approved and not self.rejected: return True
    if user == self.reviewer and self.submitted: return True
    return False
  @property
  def writer_status(self): return self.get_assignment_status('writer', self.writer, self.writers.all(), self.writer_groups.all(), self.available_to_all_my_writers, self.available_to_all_writers)
  @property
  def reviewer_status(self): return self.get_assignment_status('reviewer', self.reviewer, self.reviewers.all(), self.reviewer_groups.all(), self.available_to_all_my_reviewers, self.available_to_all_reviewers)
  def can_write(self, user):
    return (not self.submitted and ((self.writer and user == self.writer.writer) or user == self.owner))
  def can_submit(self, user):
    return (not self.submitted and (self.writer and user == self.writer.writer))
  def can_review(self, user):
    if not self.submitted: return False
    if self.rejected: return False
    if self.available_to_all_reviewers: return True
    if user == self.owner: return True
    if self.reviewer and user == self.reviewer.reviewer: return True
    if self.reviewers.filter(reviewer=user): return True
    if self.reviewer_groups.filter(reviewer__reviewer=user): return True
    if self.available_to_all_my_reviewers and self.owner.reviewers.filter(reviewer=user): return True

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
    if self.can_submit(request.user): 
      if self.is_valid(request):
        action = ArticleAction.objects.create(user=request.user, author=request.user, code=ACT_SUBMIT)
        self.last_action=action
        self.submitted = action
        self.status = STATUS_SUBMITTED
        self.save()
      else: messages.error(request, "We were unable to submit the article due to the errors encountered")
  def approve(self, user):
    if self.can_review(user): 
      action = ArticleAction.objects.create(user=user, author=self.writer.writer, code=ACT_APPROVE)
      self.last_action=action
      self.approved = action
      self.status = STATUS_APPROVED
      self.save()
  def reject(self, user):
    if self.can_review(user): 
      action = ArticleAction.objects.create(user=user, author=self.writer.writer, code=ACT_REJECT)
      self.last_action=action
      self.rejected = action
      self.status = STATUS_RELEASED
      self.submitted = None
      self.approved = None
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
  
  class ArticleWorkflowException(Exception): pass
  # ATTRIBUTES={'publish':ACT_PUBLISH,'approved':ACT_APPROVE,'submitted':ACT_SUBMIT,'assigned':ACT_ASSIGN,'rejected':ACT_REJECT,'released':ACT_RELEASE}
  def get_available_actions(self, user):
    status = self.status
    actions=[]
    if not user.is_authenticated(): return []
    if user.mode == WRITER_MODE:
      if self.writer == user and not self.submitted: actions += [ACT_REMOVE_WRITER, ACT_SUBMIT]
      # The following is needed, but is not working:
      # if self.available_to_contacts.filter(position=user.mode, worker=user) or self.available_to_all_writers or (self.available_to_all_my_writers and self.owner.contacts_as_requester__worker=user and self.owner.contacts_as_requester__position=user.mode)
      # contact_names = [c.name for c in self.owner.writer_contacts.filter(worker=user)]
      # elif not self.writer and (self.writer_availability in contact_names or not self.writer_availability):
      #   actions += [ACT_CLAIM_WRITER]
    elif user.mode == REQUESTER_MODE and user==self.owner:
      if   status == STATUS_APPROVED:     actions.append(ACT_PUBLISH)
      elif status == STATUS_SUBMITTED:    actions += [ACT_REJECT, ACT_APPROVE]
    elif user.mode == REVIEWER_MODE:
      # See if user was assigned to review
      if self.reviewer and user == self.reviewer.reviewer: return [ACT_REJECT, ACT_APPROVE]
      # See if user among reviewers made available to or its available to all
      if self.reviewers.filter(reviewer=user) or self.available_to_all_reviewers: 
        return [ACT_REJECT, ACT_APPROVE]
      # If available to all owners reviewers, check if user is among them
      if self.owner.reviewers.filter(reviewer=user) and self.available_to_all_my_reviewers:
        return [ACT_REJECT, ACT_APPROVE]
      # Check if user is member of any group in self.reviewer_groups
      if self.reviewer_groups.filter(contacts__reviewer__reviewer=user):
        return [ACT_REJECT, ACT_APPROVE]
            
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
  # @models.permalink
  # def get_absolute_url(self):
  #     return ('article_update', [self.id,])
  # @models.permalink
  # def get_tag_url(self):
  #     return ('tag_article', [self.id,])
  # @models.permalink
  # def get_claim_url(self):
  #     return ('article_claim', [self.id,])
  # @models.permalink
  # def get_accept_url(self):
  #     return ('accept_article', [self.id,])
  # @models.permalink
  # def get_submit_url(self):
  #     return ('article_submit', [self.id,])
  # @models.permalink
  # def get_release_url(self):
  #     return ('article_release', [self.id,])
  # @models.permalink
  # def get_assign_url(self):
  #     return ('article_assign', [self.id,])
  # @models.permalink
  # def get_reject_url(self):
  #     return ('article_reject', [self.id,])
  # @models.permalink
  # def get_delete_url(self):
  #     return ('article_delete', [self.id,])

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
  # writers = models.ManyToManyField(Contact, related_name = 'requesters_for_writing')
  # reviewers = models.ManyToManyField(Contact, related_name = 'requesters_for_writing')
  @property
  def is_requester(self):return self.mode == REQUESTER_MODE
  @property
  def is_writer(self):return self.mode == WRITER_MODE
  @property
  def is_reviewer(self):return self.mode == REVIEWER_MODE

def create_user_profile(sender, instance, created, **kwargs):
  if created: 
    UserProfile.objects.create(user=instance, mode=WRITER_MODE)
    # for outlet in PublishingOutlet.objects.all():
    #   PublishingOutletConfiguration.objects.create(user=instance, outlet=outlet)
post_save.connect(create_user_profile, sender=User)




