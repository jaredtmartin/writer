from django.template import Context, loader
import urllib
import random
from facepy import GraphAPI
from django.utils.html import strip_tags
from django.contrib.messages import WARNING, ERROR, SUCCESS
import sys

FACEBOOK_APP_ID = "1427197910842727"
FACEBOOK_APP_SECRET = "1ef17254fa1ec1e06ea2418c69d3504c"
REDIRECT_URL="http://writeraxis.pythonanywhere.com/user/outlets/verify_oauth/?oauth_token=%s"
CODE_LENGTH = 64
import cgi
class FacebookOutlet(object):
  settings=[]
  uses_oauth = True
  oauth_secret_key = 'code'
  # def do_action(self, parent_model):
  #     raise NotImplemented
  # def get_button_url(self, context=Context()):
  #     template = loader.get_template('articles/facebook_button.html')
  #     for setting in self.data:
  #     	return template.render(context)
  # def get_list_of_settings(self):
  #     return ['Username','Password']
  def get_oauth_request_token(self):
    token = ''.join(random.choice('0123456789ABCDEFGHJKLMNPQRSTUVWXYZ') for i in range(CODE_LENGTH))
    return (token, "not_used")
  def get_oauth_request_url(self, token):
    redirect_uri = REDIRECT_URL % token
    args = dict(client_id=FACEBOOK_APP_ID, redirect_uri=redirect_uri, scope="publish_stream")
    print "args = %s" % str(args)
    return "https://graph.facebook.com/oauth/authorize?" +urllib.urlencode(args)
  def verify_token(self, request_token, request):
    args={}
    args["client_secret"] = FACEBOOK_APP_SECRET
    args['client_id'] = FACEBOOK_APP_ID
    args['redirect_uri'] = redirect_uri = REDIRECT_URL % request_token.token
    args['code'] = request.GET['code']
    response = cgi.parse_qs(urllib.urlopen("https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(args)).read())
    return (response["access_token"][-1], "Not Used")
  def do_action(self, config, qs, oauth_token="", oauth_secret=""):
    messages=[]
    errors_encountered=False
    graph = GraphAPI(oauth_token)
    for article in qs: 
      content=article.title+"\n"+article.body
      # if len(content)>140:
      #   content = content[:137]+"..."
      #   messages.append(('warning','Twitter only allows up to 140 characters.  Your post was shortened'))
      try: graph.post(path = 'me/feed', message = content)
      except: 
        messages.append((ERROR,"Unexpected error:", sys.exc_info()[1]))
        errors_encountered = True
    if not errors_encountered: 
      if len(qs)==1: messages.append((SUCCESS,'The article has been posted sucessfully.'))
      elif len(qs)==2: messages.append((SUCCESS,'Both articles have been posted sucessfully.'))
      else: messages.append((SUCCESS,'All of the articles have been posted sucessfully.'))
    return messages
    
    