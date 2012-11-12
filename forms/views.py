from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import FormMixin
from models import Form, Element, Value, Result
from forms import make_form, make_form_class, FormModelForm, ElementInline
from extra_views import CreateWithInlinesView, UpdateWithInlinesView


class FormList(ListView):
    model = Form
    
class ThankYou(DetailView):
    model = Form
    template_name="forms/thankyou.html"
    
class FormView(DetailView, FormMixin):
    model = Form
    success_url = '/forms/'
    context_object_name = 'object'
    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        if not 'form' in context or context['form'].__class__ is Form: 
            context['form'] = make_form(self.object)
        context['object'] = self.object
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
    def get_form_class(self):
        return make_form_class(self.object)
    def get_success_url(self):
        return self.object.success_url
    def form_valid(self, form):
        result=Result.objects.create(form=self.object)
        for e in self.object.elements.all():
            c=form.cleaned_data
            Value.objects.create(element=e, value=form.cleaned_data[e.name], result=result)
        return super(FormView, self).form_valid(form)

class CreateFormView(CreateWithInlinesView):
    model = Form
    form_class = FormModelForm
    inlines = [ElementInline]
    def get_form_kwargs(self):
        kwargs=super(CreateFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

class UpdateFormView(UpdateWithInlinesView):
    model = Form
    form_class = FormModelForm
    context_object_name = 'object'
    inlines = [ElementInline]
    def get_form_kwargs(self):
        kwargs=super(UpdateFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

