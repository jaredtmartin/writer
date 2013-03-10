from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# from django.db.models import Q
# from validation_plugins import *
# from plugin_manager import PluginManager
# from django.conf import settings
import facebook
import re
from django.template import Context
from plugins import PluginModel, PluginBaseMixin
#from publishing_outlets import *
def CamelToWords(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)
    
ACT_SUBMIT          = "S"  # When author finishes writing
ACT_REJECT          = "X"  # When the user does not accept the article
ACT_APPROVE         = "A" # When the user accepts the article
ACT_WRITER          = "W"  # When the user assigns the article to a writer
ACT_REVIEWER        = "V"  # When the user assigns the article to a reviewer
ACT_CLAIM           = "C"   # When a writer claims an article
ACT_RELEASE         = "R" # When a user releases an article that was either claimed or assigned
ACT_PUBLISH         = "P" # When the article has been published
ACT_COMMENT         = "M" # When reviewing and a comment should be added
ACT_REMOVE_REVIEWER = "A"
ACT_REMOVE_WRITER   = "B"

ACTIONS = (
    (ACT_SUBMIT, 'Submitted'),
    (ACT_REJECT, 'Rejected'),
    (ACT_APPROVE, 'Approved'),
    (ACT_WRITER, 'Assigned'),
    (ACT_CLAIM, 'Claimed'),
    (ACT_RELEASE, 'Made Available'),
    (ACT_PUBLISH, 'Published'),
    (ACT_COMMENT, 'Commented On'),
    (ACT_REVIEWER, 'Assigned'),
    (ACT_REMOVE_WRITER, 'Removed Writer'),
    (ACT_REMOVE_REVIEWER, 'Removed Reviewer'),

)

WRITER_MODE = 1
REQUESTER_MODE = 2 
REVIEWER_MODE = 3

USER_MODES = (
    (WRITER_MODE, 'Writer'),
    (REQUESTER_MODE, 'Requester'),
    (REVIEWER_MODE, 'Reviewer'),
)
        
class TestOutlet(PluginModel):
    package_name="articles.pkg"

class PublishingOutlet(PluginModel):
    package_name = "articles.publishing_outlets"
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
    _data=None
    def _get_data(self): 
        if self._data: return self._data
        import pickle
        self._data = pickle.loads(self.pickled_data)
        return self._data
    def _set_data(self,value):
        self._data = value
        import pickle
        self.pickled_data = pickle.dumps(value)
    data = property(_get_data, _set_data)
    def get_setting(self, setting):
        return self.data[setting]
    def set_setting(self, setting, value):
        self.data[setting] = value
    def __init__(self, *args, **kwargs):
        super(UserConfigBaseModel, self).__init__(*args, **kwargs)
        self.load_plugin()
        
class PublishingOutletConfiguration(UserConfigBaseModel):
    plugin_foreign_key_name='outlet'
    user = models.ForeignKey(User, related_name='publishing_outlets')
    outlet = models.ForeignKey(PublishingOutlet, related_name='users')
    pickled_data = models.CharField(max_length=256, default="", blank=True)
    
    def __unicode__(self): return "%s for %s" % (self.outlet.title, self.user.username)
    

        
#class PublishingOutletConfiguration(models.Model):
#    user = models.ForeignKey(User, related_name='publishing_outlets')
#    outlet = models.ForeignKey(PublishingOutlet, related_name='users')
#    pickled_data = models.CharField(max_length=256, default="", blank=True)
#    def _get_data(self): 
#        if self._data: return self._data
#        import pickle
#        self._data = pickle.loads(self.pickled_data)
#        return self._data
#    def _set_data(self,value):
#        self._data = value
#        self.pickled_data = pickle.dumps(value)
#    data = property(_get_data, _set_data)
#    def get_setting(setting):
#        return self.data[setting]
#    def set_setting(setting, value):
#        self.data[setting] = value
#    def publish(self, article):
#        pass
#    def get_button_url(self, context=Context()):
#        context.update({
#            'username':self.username,
#            'password':self.password,
#            'user':self.user,
#            'server':self.server,
#        })
#        return self.outlet.get_button_url(context=context)
#    
#    def __unicode__(self): return "%s for %s" % (self.outlet.title, self.user.username)

class PluginMount(type):
    name="generic"
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = {}
        else:
            cls.plugins[cls.name]=cls
            
class ValidationProvider(object):
    __metaclass__ = PluginMount
    def is_valid(self, article):
        raise NotImplemented

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
    code = models.CharField(choices=ACTIONS, max_length=1)
    user = models.ForeignKey(User)                              # This is the reviewer/employer/admin
    timestamp = models.DateTimeField(auto_now_add=True)
    timezone = models.CharField(max_length=32, default="", blank=True)
    comment = models.CharField(max_length=64, default="", blank=True)
    def __unicode__(self): 
        return self.get_code_display() + " by " + self.user.get_full_name()
        
class ConfirmedRelationshipManager(models.Manager):
    def get_query_set(self):
        return super(ConfirmedRelationshipManager, self).get_query_set().filter(confirmed=True)
        
class UnconfirmedRelationshipManager(models.Manager):
    def get_query_set(self):
        return super(UnconfirmedRelationshipManager, self).get_query_set().filter(confirmed=False)
def user_full_name(self):
    return "%s %s" % (self.first_name,self.last_name)
User.full_name = property(user_full_name)
def user_writers(self):
    return self.relationships_as_requester.filter(confirmed=True, writer__isnull=False)
User.writers = property(user_writers)
def user_requesters(self):
    return Relationship.objects.filter((Q(writer=self)|Q(reviewer=self)) & Q(confirmed=True))
User.requesters = property(user_requesters)
def user_reviewers(self):
    return self.relationships_as_requester.filter(confirmed=True, reviewer__isnull=False)
User.reviewers = property(user_reviewers)

def is_requester(self): return self.get_profile().is_requester
def is_writer(self): return self.get_profile().is_writer
def is_reviewer(self): return self.get_profile().is_reviewer
User.is_requester=property(is_requester)
User.is_writer=property(is_writer)
User.is_reviewer=property(is_reviewer)

def get_user_mode(self):
    return self.get_profile().preferred_mode
def set_user_mode(self, value):
    p = self.get_profile()
    p.preferred_mode = value
    print "p = %s" % str(p)
    print "value = %s" % str(value)
    print "p.preferred_mode = %s" % str(p.preferred_mode)
    p.save()
    print "p.preferred_mode = %s" % str(p.preferred_mode)
User.mode=property(get_user_mode, set_user_mode)

def get_user_mode_display(self):
    return self.get_profile().get_preferred_mode_display()
User.mode_display = property(get_user_mode_display)

class Relationship(ValidationModelMixin, models.Model):
    requester = models.ForeignKey(User, related_name='relationships_as_requester')
    writer = models.ForeignKey(User, related_name='relationships_as_writer', null=True, blank=True)
    reviewer = models.ForeignKey(User, related_name='relationships_as_reviewer', null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='friend_requests')
    confirmed = models.BooleanField(default=False, blank=True)
    objects = models.Manager()
    pending_objects = UnconfirmedRelationshipManager()
    confirmed_objects = ConfirmedRelationshipManager()
    @property
    def worker(self):
        if self.writer: return self.writer
        else: return self.reviewer
    @property
    def verb(self):
        if self.writer: return "writes"
        else: return "reviews"
    def __unicode__(self): 
        if self.confirmed:
            return "%s %s for %s" % (self.worker.full_name, self.verb, self.requester.full_name)
        else:
            if self.created_by==self.requester: 
                return "%s requested %s to %s for him" % (self.created_by.full_name, self.verb, self.worker.full_name)
            else:
                return "%s requested to %s for %s" % (self.created_by.full_name, self.verb, self.requester.full_name)
    @models.permalink
    def get_delete_url(self):
        return ('relationship_delete', [self.id,])
class NotDeletedManager(models.Manager):
    def get_query_set(self):
        return super(NotDeletedManager, self).get_query_set().filter(deleted=False)

class Article(ValidationModelMixin, models.Model):
    def __unicode__(self): return self.name
    minimum = models.IntegerField(default=100)
    maximum = models.IntegerField(default=0) # Use zero for no maximum
    body = models.TextField(blank=True, default="")
    title = models.CharField(max_length=256, blank=True, default="")
    article_type = models.ForeignKey(ArticleType, related_name='articles')
    project = models.ForeignKey(Project, related_name='articles', null=True, blank=True)
    tags = models.CharField(max_length=128, blank=True, default="")
    
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
    
    expires = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False, blank=True)
    released = models.BooleanField(default=False, blank=True)
    description = models.TextField(max_length=256, blank=True, default="")
    article_notes = models.CharField(max_length=128, blank=True, default="")
    review_notes = models.CharField(max_length=128, blank=True, default="")
    objects = NotDeletedManager()
    all_objects = models.Manager()
    # actions = models.ManyToManyField(ArticleAction, through='ArticlesActions')
#    _actions = (
#        # This is a tuple of actions that can be done on the articles
#        # The first element of each action is its name
#        # The mode it is used for
#        # The permissions required to do the action
#        ['claim', WRITER_MODE, None]
#        ['assign', REQUESTER_MODE, None]
#        ['submit', REQUESTER_MODE, None]
#        ['accept', REQUESTER_MODE, None]
#        ['reject', ]
#        'publish'
#        'release'
#    
#    )

    def get_tags(self):
        return self.tags.split(',')
    def set_tags(self, value):
        if type(value)==list:
            self.tags=",".join(set(value))
        else: self.tags=value
    # @property
    # def tags_as_list(self):
    #     return self._tags
    tags_as_list=property(get_tags, set_tags)
    @property
    def status(self): 
        if self.last_action: return self.last_action.get_code_display()
        return u"New"
    
    class ArticleWorkflowException(Exception): pass
    # ATTRIBUTES={'publish':ACT_PUBLISH,'approved':ACT_APPROVE,'submitted':ACT_SUBMIT,'assigned':ACT_ASSIGN,'rejected':ACT_REJECT,'released':ACT_RELEASE}

    def get_available_actions(self, user):
        try: status= self.last_action.code
        except: status = None
        if user == self.writer and (status == ACT_WRITER or status == ACT_CLAIM): return ['submit','release']
        elif user == self.reviewer and (status == ACT_SUBMIT): return ['accept','reject']
        elif user == self.owner:
            if status == None or status == ACT_RELEASE or status == ACT_REJECT: return ['assign','tag','delete']
            elif status == ACT_SUBMIT: return ['approve','reject','tag','delete']
            elif status == ACT_APPROVE: return ['publish','tag','delete']
            else: return ['release','tag','delete']
        elif status == None or status == ACT_RELEASE or status == ACT_REJECT: return ['claim',]
        return []
            
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
    preferred_mode = models.IntegerField(choices=USER_MODES)
    def __unicode__(self): return self.user.username+"'s profile"

    @property
    def is_requester(self):
        return self.preferred_mode == REQUESTER_MODE
    @property
    def is_writer(self):
        return self.preferred_mode == WRITER_MODE
    @property
    def is_reviewer(self):
        return self.preferred_mode == REVIEWER_MODE
    @property
    def graph(self): return facebook.GraphAPI(self.access_token)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, preferred_mode=WRITER_MODE)

post_save.connect(create_user_profile, sender=User)


