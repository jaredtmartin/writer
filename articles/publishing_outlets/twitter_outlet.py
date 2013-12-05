from django.template import Context, Template
import urlparse
import oauth2 as oauth
from django.contrib.messages import WARNING, ERROR, SUCCESS
from twitter import *
import sys
CONSUMER_SECRET="DlzUgtRvbMFSTP1wFLY4YuOZtZus59EreDoP8kdSpw"
CONSUMER_KEY = "weGHEJZMZs0h9bnpLouBSw"

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize"
ACCESS_TOKEN_URL  = "https://api.twitter.com/oauth/access_token"
from django.utils.html import strip_tags

class TwitterOutlet(object):
  settings=[]
  uses_oauth = True
  oauth_secret_key = 'oauth_token'
  def get_button_url(self, context=Context()):
    template = Template('<a href="http://twitter.com/home?status={{ article.body|urlencode }}%20{{ article.title|urlencode }}">{{title}}</a>')
    return template.render(context)
  def get_oauth_request_token(self):
    consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    client = oauth.Client(consumer)
    resp, content = client.request(REQUEST_TOKEN_URL, "GET")
    if resp['status'] != '200':
      raise Exception("Invalid response %s." % resp['status'])
    request_token = dict(urlparse.parse_qsl(content))
    return (request_token['oauth_token'], request_token['oauth_token_secret'])
  def verify_token(self, request_token, request):
    consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    temp_token = oauth.Token(request_token.token, request_token.secret)
    temp_token.set_verifier(request.GET['oauth_verifier'])
    client = oauth.Client(consumer, temp_token)

    resp, content = client.request(ACCESS_TOKEN_URL, "POST")
    access = dict(urlparse.parse_qsl(content))
    if '<?xml version' in access.keys(): return (None, None)
    return (access['oauth_token'], access['oauth_token_secret'])
  def get_oauth_request_url(self, token):
    return "%s?oauth_token=%s" % (AUTHORIZE_URL, token)
  def do_action(self, config, qs, oauth_token="", oauth_secret=""):
    messages=[]
    t = Twitter(auth=OAuth(oauth_token, oauth_secret,CONSUMER_KEY, CONSUMER_SECRET))
    errors_encountered=False
    for article in qs: 
      content=article.title+"\n"+strip_tags(article.body)
      if len(content)>140:
        content = content[:137]+"..."
        messages.append((WARNING,'Twitter only allows up to 140 characters.  Your post was shortened'))
      try: t.statuses.update(status=content)
      except TwitterHTTPError: 
        messages.append((ERROR,'"%s" is a duplicate. It has already been posted to this account.' % article.title))
        errors_encountered = True
      except: 
        messages.append((ERROR,"Unexpected error: %s:%s" % (sys.exc_info()[0], sys.exc_info()[1])))
        errors_encountered = True
    if not errors_encountered: 
      if len(qs)==1: messages.append((SUCCESS,'The article has been posted sucessfully.'))
      elif len(qs)==2: messages.append((SUCCESS,'Both articles have been posted sucessfully.'))
      else: messages.append((SUCCESS,'All of the articles have been posted sucessfully.'))
    return messages