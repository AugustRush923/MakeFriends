from django.shortcuts import render
from django.views.generic import TemplateView
from model.models import Model

from blog.views import CommonViewMixin


# Create your views here.


class ModelView(CommonViewMixin, TemplateView):
    template_name = 'model/model_page.html'

    def get_context_data(self, **kwargs):
        context = super(ModelView, self).get_context_data(**kwargs)
        context.update({'models': Model.get_models()})
        return context
