from forms.models import UserProfile
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
        if fb_uid and fb_graphtoken:
            user, created = User.objects.get_or_create(username=fb_uid)
            if created:
                try: profile=user.get_profile()
                except: profile=UserProfile.objects.create(user=user)
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
                    profile.access_token = fb_graphtoken
                    user.save()
                    profile.save()
            return user
        return None
