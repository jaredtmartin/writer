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
    
class Article(models.Model):
    def __unicode__(self): return self.name
    minimum = models.IntegerField(default=100)
    maximum = models.IntegerField(default=0) # Use zero for no maximum
    body = models.TextField(blank=True, default="")
    _published = models.BooleanField(blank=True, default=False)
    _approved = models.BooleanField(blank=True, default=False)
    _submitted = models.BooleanField(blank=True, default=False)
    _assigned = models.ForeignKey(User, null=True, blank=True, related_name='assigned_articles')
    class ArticleWorkflowException(Exception): pass
    def approve(self, user=None, comment=""):
        if self._submitted:
            self._approved = True
            self.save()
            self.articleaction_set.create(code=ACT_APPROVE, user=user, author=self._assigned, comment=comment)
        else: raise self.ArticleWorkflowException("This article cannot be approved until it has been submitted.")

    def reject(self, user=None, comment=""):
        if self._submitted:
            self._approved = False
            self._submitted = False
            self.save()
            self.articleaction_set.create(code=ACT_REJECT, user=user, author=self._assigned, comment=comment)
        else: raise self.ArticleWorkflowException("This article cannot be rejected until it has been submitted.")
        
    def publish(self, user=None, comment=""):
        if self._approved:
            self._published = True
            self.save()
            self.articleaction_set.create(code=ACT_PUBLISH, user=user, author=self._assigned, comment=comment)
        else: raise self.ArticleWorkflowException("This article cannot be published until it has been approved.")

    def submit(self, user=None, comment=""):
        if not self._submitted:
            self._submitted = True
            self.save()
            self.articleaction_set.create(code=ACT_SUBMIT, user=user, author=user, comment=comment)
        else: raise self.ArticleWorkflowException("This article has already been submitted.")

    def release(self, user=None, comment=""):
        if self._assigned:
            self.articleaction_set.create(code=ACT_RELEASE, user=user, author=self._assigned, comment=comment)
            self._assigned = None # We need to create the action first so we don't lose the guy's name
            self.save()
        else: raise self.ArticleWorkflowException("This article has not been assigned or claimed.")
        
    def assign(self, author, user=None):
        if not self._assigned:
            self._assigned = author
            self.save()
            self.articleaction_set.create(code=ACT_ASSIGN, user=user, author=author, comment=comment)
        else: raise self.ArticleWorkflowException("This article has not been assigned or claimed.")
        
    def claim(self, user=None):
        if not self._assigned:
            self._assigned = user
            self.save()
            self.articleaction_set.create(code=ACT_CLAIM, user=user, author=user, comment=comment)
        else: raise self.ArticleWorkflowException("This article has not been assigned or claimed.")
        
    def reject_and_release(self, user=None, comment=""):
        self.reject(user=user, comment=comment)
        self.release(user=user, comment=comment)
    
    @property
    def submitted(self):
        return self._submitted
    @property
    def published(self):
        return self._published
    @property
    def assigned(self):
        return self._assigned
    @property
    def approved(self):
        return self._approved
    @property
    def keywords(self):
        return str([str(word.keyword) for word in self.keyword_set.all()])
    @property
    def name(self):
        if self.maximum > 0: length=u" (" + str(self.minimum) + u" - " + str(self.maximum) + u") words"
        else: length = u" (" + str(self.minimum) + u") words"
        return self.keywords + length
        
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
    
ACTIONS = (
    (ACT_SUBMIT, 'Submited'),
    (ACT_REJECT, 'Rejected'),
    (ACT_APPROVE, 'Approved'),
    (ACT_ASSIGN, 'Assigned'),
    (ACT_CLAIM, 'Claimed'),
    (ACT_RELEASE, 'Released'),
    (ACT_PUBLISH, 'Published'),
)

class ArticleAction(models.Model):
    article = models.ForeignKey(Article)
    author = user = models.ForeignKey(User, related_name = 'authors')
    code = models.CharField(choices=ACTIONS, max_length=1)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(choices=ACTIONS, max_length=64, default="", blank=True)
    

