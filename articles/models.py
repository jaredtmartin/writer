from django.db import models
from django.contrib.auth.models import User

from django.db.models import Q

ACT_SUBMIT = "S"  # When author finishes writing
ACT_REJECT = "X"  # When the user does not accept the article
ACT_APPROVE = "A" # When the user accepts the article
ACT_ASSIGN = "G"  # When the user assigns the article to a writer
ACT_CLAIM = "C"   # When a writer claims an article
ACT_RELEASE = "R" # When a user releases an article that was either claimed or assigned
ACT_PUBLISH = "P" # When the article has been published

ACTIONS = (
    (ACT_SUBMIT, 'Submited'),
    (ACT_REJECT, 'Rejected'),
    (ACT_APPROVE, 'Approved'),
    (ACT_ASSIGN, 'Assigned'),
    (ACT_CLAIM, 'Claimed'),
    (ACT_RELEASE, 'Released'),
    (ACT_PUBLISH, 'Published'),
)

class ArticleType(models.Model):
    name = models.CharField(max_length=16)
    def __unicode__(self): return self.name
    
class Project(models.Model):
    name = models.CharField(max_length=64)
    def __unicode__(self): return self.name

class ArticleAction(models.Model):
    article = models.ForeignKey('Article')
    author = models.ForeignKey(User, related_name = 'authors')  # This is the writer
    code = models.CharField(choices=ACTIONS, max_length=1)
    user = models.ForeignKey(User)                              # This is the reviewer/employer/admin
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(choices=ACTIONS, max_length=64, default="", blank=True)
    def __unicode__(self): return ACTIONS[self.code]

    
class Article(models.Model):
    def __unicode__(self): return self.name
    minimum = models.IntegerField(default=100)
    maximum = models.IntegerField(default=0) # Use zero for no maximum
    body = models.TextField(blank=True, default="")
    article_type = models.ForeignKey(ArticleType, related_name='articles')
    project = models.ForeignKey(Project, related_name='articles', null=True, blank=True)
    tags = models.CharField(max_length=128, blank=True, default="")

    published   = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='published_articles')
    approved    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='approved_articles')
    submitted   = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='submitted_articles')
    assigned    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='assigned_articles')
    rejected    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='rejected_articles')
    released    = models.ForeignKey(ArticleAction, null=True, blank=True, related_name='released_articles')
    class ArticleWorkflowException(Exception): pass
    ATTRIBUTES={'publish':ACT_PUBLISH,'approved':ACT_APPROVE,'submitted':ACT_SUBMIT,'assigned':ACT_ASSIGN,'rejected':ACT_REJECT,'released':ACT_RELEASE}

    def change_status(self, attribute='', code=None, user=None, author=None, comment="", save=True, req=True, clear=[], error="Undefined Workflow Error"):
        if req and attribute in ATTRIBUTES.keys():
            if not author: author=self.assigned.author
            if not code: code=ATTRIBUTES[attribute]
            settattr(self, attribute, self.articleaction_set.create(
                code=code, 
                user=user, 
                author=author, 
                comment=comment
            ))
            for attr in clear: setattr(self, attr, None)
            if save: self.save()
        else: raise self.ArticleWorkflowException(error)

            
    def approve(self, user=None, comment="", save=True):
        self.change_status(
            attribute='approved',
            comment=comment,
            save=save,
            req=self.submitted,
            error="This article cannot be approved until it has been submitted."
        )
    def reject(self, user=None, comment="", save=True):
        self.change_status(
            attribute='rejected',
            comment=comment,
            save=save,
            req=self.submitted,
            clear=['approved','submitted'],
            error="This article cannot be rejected until it has been submitted."
        )
    def publish(self, user=None, comment="", save=True):
        self.change_status(
            attribute='published',
            comment=comment,
            save=save,
            req=self.approved,
            error="This article cannot be published until it has been approved."
        )
    def submit(self, user=None, comment="", save=True):
        self.change_status(
            attribute='submitted',
            comment=comment,
            save=save,
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
            req=(not self.assigned),
            clear = ['assigned'],
            error="This article has already been assigned or claimed."
        )
    def claim(self, user=None, comment="", save=True):
        self.change_status(
            attribute='assigned',
            comment=comment,
            author=user,
            code=ACT_CLAIM,
            save=save,
            req=(not self.assigned),
            clear = ['assigned'],
            error="This article has already been assigned or claimed."
        )
    def reject_and_release(self, user=None, comment="", save=True):
        self.reject(user=user, comment=comment, save=False)
        self.release(user=user, comment=comment, save=save)
    @property
    def klass(self):return self.article_type.name
    @property
    def keywords(self):
        s=''
        if not s=='':s+=','
        for kw in self.keyword_set.all(): s+=kw.keyword  
        return s #str([str(word.keyword) for word in self.keyword_set.all()])
    @property
    def name(self):
        if self.maximum > 0: length=u" (" + str(self.minimum) + u" - " + str(self.maximum) + u") words"
        else: length = u" (" + str(self.minimum) + u") words"
        return self.keywords + length
    @models.permalink
    def get_absolute_url(self):
        return ('article_update', [self.id,])  
#    def last_action(self, group=None):
#        try:
#            if group: return self.articleaction_set.filter(action__in = group)[0]
#            else: return self.articleaction_set.all()[0]
#        except IndexError: return None
#        
#    @property
#    def is_assigned(self):
#        assigned = self.last_action(['G','C'])
#        returned = self.last_action(['U','T'])
#        if assigned:
#            if returned():
#                # the article has been assigned and returned
#                if assigned.timestamp > returned.timestamp: return True
#                else: return False
#            else:
#                # the article has been assigned but never returned
#                return True
#        else:
#            # the article was never assigned
#            return False

        
#    @property
#    def is_submitted(self):
#        submitted = last_action('S')
#        rejected = last_action('R')
#        if submitted:
#            if rejected:
#                if submitted.timestamp > rejected.timestamp: return True
#                else: return False
#            else: return True
#        return False

class Keyword(models.Model):
    article = models.ForeignKey(Article)  
    keyword = models.CharField(max_length=32)
    url = models.CharField(max_length=64)
    times = models.IntegerField(default=1)
    



