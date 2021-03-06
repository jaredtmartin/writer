from forms.models import UserProfile
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from django.contrib.auth.models import User
import facebook
class FacebookProfileBackend(ModelBackend):
    """
    Authenticate a facebook user and autopopulate facebook data into the
    user's profile.

    """
    def authenticate(self, fb_uid=None, fb_graphtoken=None):
        """
        If we receive a facebook uid then the cookie has already been
        validated.

        """

        if fb_uid:
            user, created = User.objects.get_or_create(username=fb_uid)
            print "Let me know if you're working'"
            print "user: " + str(user) 
            print "created: " + str(created) 
            print "fb_uid: " + str(fb_uid) 
            print "fb_graphtoken: " + str(fb_graphtoken) 
            if fb_graphtoken:
                try: 
                    profile=user.get_profile()
                    print "profile exists"
                except: 
                    profile=UserProfile.objects.create(user=user)
                    print "created profile"
                profile.access_token = fb_graphtoken
                profile.save()
                if created:

                    # It would be nice to replace this with an asynchronous request
                    graph = facebook.GraphAPI(fb_graphtoken)
                    me = graph.get_object('me')
                    if me:
                        if me.get('first_name'):
                            user.first_name = me['first_name']
                        if me.get('last_name'):
                            user.last_name = me['last_name']
                        if me.get('email'):
                            user.email = me['email']
                        user.save()
                        print "fb_graphtoken: " + str(fb_graphtoken) 
            return user
        return None
