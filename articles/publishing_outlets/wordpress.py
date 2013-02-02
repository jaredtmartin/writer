class WordPressOutlet(object):
    def do_action(self, parent_model):
        import datetime, xmlrpclib

        wp_url = "http://%s/xmlrpc.php" % parent_model.server_domain
        wp_username = parent_model.username
        wp_password = parent_model.password
        wp_blogid = ""

        status_draft = 0
        status_published = 1

        server = xmlrpclib.ServerProxy(wp_url)

        title = "Posting via Python"
        content = "I really hope this works!"
        date_created = xmlrpclib.DateTime(datetime.datetime.strptime("2009-10-20 21:08", "%Y-%m-%d %H:%M"))
        categories = ["Test Category"]
        tags = ["Test", "More Testing"]
        data = {'title': title, 'description': content, 'dateCreated': date_created, 'categories': categories, 'mt_keywords': tags}

        post_id = server.metaWeblog.newPost(wp_blogid, wp_username, wp_password, data, status_published)


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
