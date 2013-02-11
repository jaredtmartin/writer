from django.db import models

class PluginModel(models.Model):
    package_name="plugins"
    class Meta:
        abstract = True
    class_name = models.CharField(max_length=128)
    module_name = models.CharField(max_length=128)
    module=None
    plugin_class=None
    plugin=None
    def __init__(self, *args, **kwargs):
        super(PluginModel, self).__init__(*args, **kwargs)
        try:
            # First load the module the plugin is stored in
            self.module = __import__("%s.%s" % (self.package_name, self.module_name), fromlist=[True])
            # Now get the plugins class
            self.plugin_class = self.get_plugin_class()
            # Now create an instance of the plugin
            self.plugin = self.get_plugin()
        except ImportError as e: print "There was an ImportError loading the plugin: %s" % e
        
    def get_plugin(self):
        # Creates an instance of the plugin
        return self.plugin_class()
          
    def get_plugin_class(self):
        # fetches the plugins class from the module
        return eval("self.module.%s" % self.class_name)
