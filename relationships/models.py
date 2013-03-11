from django.db import models
class ConfirmedRelationshipManager(models.Manager):
    def get_query_set(self):
        return super(ConfirmedRelationshipManager, self).get_query_set().filter(confirmed=True)
        
class UnconfirmedRelationshipManager(models.Manager):
    def get_query_set(self):
        return super(UnconfirmedRelationshipManager, self).get_query_set().filter(confirmed=False)

class Relationship(ValidationModelMixin, models.Model):
    child 		= models.ForeignKey(User, related_name='child_relationships')
    parent 		= models.ForeignKey(User, related_name='parent_relationships')
    initiator 	= models.ForeignKey(User, related_name='initiator')
    confirmed 	= models.BooleanField(default=False, blank=True)
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