from django.contrib import admin
from models import *

class ElementInline(admin.TabularInline):
    model = Element
    extra = 0
    
class ValueInline(admin.TabularInline):
    model = Value
    extra = 0
    
class ResultAdmin(admin.ModelAdmin):
    inlines = [ValueInline,]
    list_display = ('form','created_at')
    list_filter = ('form',)
    
class FormAdmin(admin.ModelAdmin):
    inlines = [ElementInline,]
    list_display = ('name', 'get_absolute_url')
    
admin.site.register(Form, FormAdmin)
admin.site.register(Result, ResultAdmin)
