from django.contrib.messages import WARNING, ERROR, SUCCESS
import sys
import socket
class WordPressOutlet(object):
  settings = ['Username','Password','Server']
  label = "Wordpress"
  def do_action(self, config, qs, oauth_token="", oauth_secret=""):
    PUBLISHED_STATUS = 1
    import datetime, xmlrpclib
    wp_url = "http://%s/xmlrpc.php" % config['Server']
    server = xmlrpclib.ServerProxy(wp_url)
    wp_blogid = ""
    wp_username = config['Username']
    wp_password = config['Password']
    for article in qs:
      messages=[]
      errors_encountered=False
      data = {'title': article.title, 'description': article.body, 'mt_keywords':["Test"]}
      try: post_id = server.metaWeblog.newPost(wp_blogid, wp_username, wp_password, data, PUBLISHED_STATUS)
      except xmlrpclib.Fault:
        messages.append((ERROR,sys.exc_info()[1].faultString))
        errors_encountered = True
      except socket.gaierror:
        messages.append((ERROR,'Wordpress server URL incorrect.'))
        errors_encountered = True
      except: 
        messages.append((ERROR,"Unexpected error: %s:%s" % (sys.exc_info()[0], sys.exc_info()[1])))
        print "sys.exc_info() = %s" % str(sys.exc_info())
        print "sys.exc_info()[1] = %s" % str(sys.exc_info()[1])
        print "type(sys.exc_info()[1]) = %s" % str(type(sys.exc_info()[1]))
        print "sys.exc_info()[1].__dict__.keys() = %s" % str(sys.exc_info()[1].__dict__.keys())
        errors_encountered = True
    if not errors_encountered: 
      if len(qs)==1: messages.append((SUCCESS,'The article has been posted sucessfully.'))
      elif len(qs)==2: messages.append((SUCCESS,'Both articles have been posted sucessfully.'))
      else: messages.append((SUCCESS,'All of the articles have been posted sucessfully.'))
    return messages
      ###############################################################
      # The following section is a working demo:
      # wp_url = "http://%s/xmlrpc.php" % parent_model.server_domain
      # wp_username = parent_model.username
      # wp_password = parent_model.password
      # wp_blogid = ""

      # status_draft = 0
      # status_published = 1

      # server = xmlrpclib.ServerProxy(wp_url)

      # title = "Posting via Python"
      # content = "I really hope this works!"
      # date_created = xmlrpclib.DateTime(datetime.datetime.strptime("2009-10-20 21:08", "%Y-%m-%d %H:%M"))
      # categories = ["Test Category"]
      # tags = ["Test", "More Testing"]
      # data = {'title': title, 'description': content, 'dateCreated': date_created, 'categories': categories, 'mt_keywords': tags}

      # post_id = server.metaWeblog.newPost(wp_blogid, wp_username, wp_password, data, status_published)


# Just found a js way of doing this:
# See instructions here: https://github.com/developerworks/wordpress-xmlrpc-javascript-api#readme
#var connection = {
#    url : "your xmlprc url such as http://www.exmaple.com/xmlrpc.php",
#    username : "you login name",
#    password : "you password"
#};
#var wp = new WordPress(connection.url, connection.username, connection.password);
#var blogId = 1;
#var postId = 1;
#var object = wp.getPost(blogId, postId);
#// run console.log(object); to output the attributes of the object 
