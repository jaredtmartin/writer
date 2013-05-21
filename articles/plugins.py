"""
To use these classes, follow the following steps:

class A(PluginModel):
    package_name = "app.plugin_folder"
class B(PluginBaseMixin, models.Model):
    plugin_foreign_key_name='plugin'
    plugin = models.ForeignKey(PluginType)
    def __init__(self, *args, **kwargs):
        super(B, self).__init__(*args, **kwargs)
        self.load_plugin()
"""
from django.db import models

class PluginModel(models.Model):
    package_name="plugins"
    class Meta:
        abstract = True
    class_name = models.CharField(max_length=128)
    module_name = models.CharField(max_length=128)
    module=None
    plugin_class=None
    _plugin=None
    def __init__(self, *args, **kwargs):
        super(PluginModel, self).__init__(*args, **kwargs)
        try:
            # First load the module the plugin is stored in
            self.module = __import__("%s.%s" % (self.package_name, self.module_name), fromlist=['a'])
            # Now get the plugins class
            self.plugin_class = self.get_plugin_class()
            # Now create an instance of the plugin
#            self.plugin = self.get_plugin()
        except ImportError as e: print "There was an ImportError loading the plugin: %s" % e
          
    def get_plugin_class(self):
        # fetches the plugins class from the module
        # print "eval: " + str("self.module.%s" % self.class_name) 
        if self.class_name: return eval("self.module.%s" % self.class_name)
        else: return None

    @property
    def plugin(self):
        if not self._plugin: self._plugin = self.plugin_class()
        return self._plugin


class PluginBaseMixin(object):
    plugin_foreign_key_name='plugin'
    _plugin = None
    def add_mixins(self, *mixins):
        class BareClass(object):pass
        class ModelWithPlugin(BareClass):pass
        ModelWithPlugin.__bases__ = mixins + (self.__class__,)
        self.__class__ = ModelWithPlugin
    def load_plugin(self):
        try:
            self._plugin = getattr(self, self.plugin_foreign_key_name)
        except: pass
        if self._plugin:
            # Create an instance of the plugin
            self.plugin_class=self._plugin.plugin_class
            self.add_mixins(self.plugin_class)
    #                self.__dict__.update(self.cache_vars.items())

        
