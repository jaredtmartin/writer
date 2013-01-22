from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Q
from validation_plugins import *
from plugin_manager import PluginManager
from django.conf import settings
def CamelToWords(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)
    
ACT_SUBMIT = "S"  # When author finishes writing
ACT_REJECT = "X"  # When the user does not accept the article
ACT_APPROVE = "A" # When the user accepts the article
ACT_ASSIGN = "G"  # When the user assigns the article to a writer
ACT_CLAIM = "C"   # When a writer claims an article
ACT_RELEASE = "R" # When a user releases an article that was either claimed or assigned
ACT_PUBLISH = "P" # When the article has been published
ACT_COMMENT = "M" # When reviewing and a comment should be added

ACTIONS = (
    (ACT_SUBMIT, 'Submitted'),
    (ACT_REJECT, 'Rejected'),
    (ACT_APPROVE, 'Approved'),
    (ACT_ASSIGN, 'Assigned'),
    (ACT_CLAIM, 'Claimed'),
    (ACT_RELEASE, 'Released'),
    (ACT_PUBLISH, 'Published'),
    (ACT_COMMENT, 'Commented On'),
)

WRITER_MODE = 1
REQUESTER_MODE = 2 
DUAL_MODE = 3

USER_MODES = (
    (WRITER_MODE, 'Writer'),
    (REQUESTER_MODE, 'Requester'),
    (DUAL_MODE, 'Both'),
)

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
    plugin_loader=PluginManager(settings.DIRNAME+'/articles/validation_plugins/')
    available_validators=ValidationProvider.plugins
    
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
        ordering = ['-timestamp']
    articles = models.ManyToManyField('Article')
    author = models.ForeignKey(User, related_name = 'authors', null=True, blank=True)  # This is the writer
    code = models.CharField(choices=ACTIONS, max_length=1)
    user = models.ForeignKey(User)                              # This is the reviewer/employer/admin
    timestamp = models.DateTimeField(auto_now_add=True)
    timezone = models.CharField(max_length=32)
    comment = models.CharField(max_length=64, default="", blank=True)
    def __unicode__(self): 
        return self.get_code_display() + " by " + self.user.get_full_name()
        
class ConfirmedRelationshipManager(models.Manager):
    def get_query_set(self):
        return super(ConfirmedRelationshipManager, self).get_query_set().filter(confirmed=True)
        
class UnconfirmedRelationshipManager(models.Manager):
    def get_query_set(self):
        return super(UnconfirmedRelationshipManager, self).get_query_set().filter(confirmed=False)
def full_name(self):
    return "%s %s" % (self.first_name,self.last_name)
User.full_name=property(full_name)
def writers(self):
    l=[]
    for r in self.writer_relationships.all():
        writer = r.writer
        writer.is_confirmed = r.confirmed
        writer.is_confirmable = not r.confirmed and not self == r.created_by
        writer.relationship = r
        l.append(writer)
    return l
    return [r.writer for r in self.writer_relationships.all()]
User.writers=property(writers)
def requesters(self):
    l=[]
    for r in self.requester_relationships.all():
        requester = r.requester
        requester.is_confirmed = r.confirmed
        requester.is_confirmable = not r.confirmed and not self == r.created_by
        requester.relationship = r
        l.append(requester)
    return l
    return [r.requester for r in self.requester_relationships.all()]
User.requesters=property(requesters)
def is_requester(self): return self.get_profile().is_requester
def is_writer(self): return self.get_profile().is_writer
User.is_requester=property(is_requester)
User.is_writer=property(is_writer)

class Relationship(ValidationModelMixin, models.Model):
    requester = models.ForeignKey(User, related_name='writer_relationships')
    writer = models.ForeignKey(User, related_name='requester_relationships')
    created_by = models.ForeignKey(User, related_name='friend_requests')
    confirmed = models.BooleanField(default=False, blank=True)
    objects = models.Manager()
    pending_objects = UnconfirmedRelationshipManager()
    confirmed_objects = ConfirmedRelationshipManager()
    def __unicode__(self): 
        if self.confirmed:
            return "%s writes for %s" % (self.writer.full_name, self.requester.full_name)
        else:
            if self.created_by==self.requester: 
                return "%s requested %s to write for him" % (self.created_by.full_name, self.writer.full_name)
            else:
                return "%s requested to write for %s" % (self.created_by.full_name, self.requester.full_name)
    @models.permalink
    def get_delete_url(self):
        return ('relationship_delete', [self.id,])
class PostingOutlet(models.Model):
    name = models.CharField(max_length=256)
    
    

class Article(ValidationModelMixin, models.Model):
    def __unicode__(self): return self.name
    minimum = models.IntegerField(default=100)
    maximum = models.IntegerField(default=0) # Use zero for no maximum
    body = models.TextField(blank=True, default="")
    title = models.CharField(max_length=256, blank=True, default="")
    article_type = models.ForeignKey(ArticleType, related_name='articles')
    project = models.ForeignKey(Project, related_name='articles', null=True, blank=True)
    _tags = models.CharField(max_length=128, blank=True, default="")
    owner = models.ForeignKey(User, related_name='articles')
    expires = models.DateTimeField(blank=True, null=True)
    
    def get_tags(self):
        return self._tags.split(',')
    def set_tags(self, value):
        if type(value)==list:
            self._tags=",".join(value)
        else: self._tags=value
    def tags_as_str(self):
        return self._tags
    tags=property(get_tags, set_tags)
    @property
    def status(self): 
        if self.last_action: return self.last_action.get_code_display()
        return u"New"
    
    last_action = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='articles_last_action')
    published   = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='published_articles')
    approved    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='approved_articles')
    submitted   = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='submitted_articles')
    assigned    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='assigned_articles')
    rejected    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='rejected_articles')
    released    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='released_articles')
    class ArticleWorkflowException(Exception): pass
    ATTRIBUTES={'publish':ACT_PUBLISH,'approved':ACT_APPROVE,'submitted':ACT_SUBMIT,'assigned':ACT_ASSIGN,'rejected':ACT_REJECT,'released':ACT_RELEASE}

    @property
    def available_actions(self):
        status= self.last_action.code
        print "status: " + str(status) 
        print "status==ACT_ASSIGN: " + str(status==ACT_ASSIGN) 
        print "ACT_ASSIGN: " + str(ACT_ASSIGN) 
        if status == None: return []
        elif status == ACT_ASSIGN: return ['submit','release']
        elif status == ACT_SUBMIT: return ['approve','reject']
        elif status == ACT_APPROVE: return ['publish']
        elif status == ACT_REJECT: return ['submit','release']
            
    def change_status(self, attribute='', code=None, user=None, author=None, comment="", save=True, req=True, clear=[], error="Undefined Workflow Error"):
        if req and attribute in Article.ATTRIBUTES.keys():
            if not author: author=self.assigned.author
            if not code: code=Article.ATTRIBUTES[attribute]
            action = self.articleaction_set.create(
                code=code, 
                user=user, 
                author=author, 
                comment=comment,
                timezone=user.get_profile().timezone,
            )
            setattr(self, attribute, action)
            self.last_action=action
            for attr in clear: setattr(self, attr, None)
            if save: self.save()
        else: raise self.ArticleWorkflowException(error)

            
    def approve(self, user=None, comment="", save=True):
        self.change_status(
            attribute='approved',
            comment=comment,
            save=save,
            req=self.submitted,
            user=user, 
            error="This article cannot be approved until it has been submitted."
        )
    def reject(self, user=None, comment="", save=True):
        self.change_status(
            attribute='rejected',
            comment=comment,
            save=save,
            req=self.submitted,
            user=user, 
            clear=['approved','submitted'],
            error="This article cannot be rejected until it has been submitted."
        )
    def publish(self, user=None, comment="", save=True):
        self.change_status(
            attribute='published',
            comment=comment,
            save=save,
            user=user, 
            req=self.approved,
            error="This article cannot be published until it has been approved."
        )
    def submit(self, user=None, comment="", save=True):
        self.change_status(
            attribute='submitted',
            comment=comment,
            save=save,
            user=user, 
            req=(not self.submitted),
            author=user,
            clear=['rejected'],
            error="This article has already been submitted."
        )
    def release(self, user=None, comment="", save=True):
        self.change_status(
            attribute='released',
            comment=comment,
            save=save,
            user=user, 
            req=self.assigned,
            clear = ['assigned'],
            error="This article has not been assigned or claimed."
        )
    def assign(self, author, user=None, comment="", save=True):
        self.change_status(
            attribute='assigned',
            author=author,
            comment=comment,
            save=save,
            user=user, 
            req=(not self.assigned),
#            clear = ['assigned'],
            error="This article has already been assigned or claimed."
        )
    def claim(self, user=None, comment="", save=True):
        self.change_status(
            attribute='assigned',
            comment=comment,
            author=user,
            user=user, 
            code=ACT_CLAIM,
            save=save,
            req=(not self.assigned),
#            clear = ['assigned'],
            error="This article has already been assigned or claimed."
        )
    def reject_and_release(self, user=None, comment="", save=True):
        self.reject(user=user, comment=comment, save=False)
        self.release(user=user, comment=comment, save=save)
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
        return self.preferred_mode >= REQUESTER_MODE
    @property
    def is_writer(self):
        return self.preferred_mode in [WRITER_MODE, DUAL_MODE]
    @property
    def graph(self): return facebook.GraphAPI(self.access_token)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, preferred_mode=WRITER_MODE)

post_save.connect(create_user_profile, sender=User)


