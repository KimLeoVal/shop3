from django.db.models import Q
from django.utils.http import urlencode
from django.views.generic import ListView

from webapp.forms import SearchForm


class SearchView(ListView):
    search_form_class = SearchForm
    search_form_field = "search"
    query_name = "query"
    search_fields = []

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return self.model.objects.filter(self.get_query())
        return self.model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({self.search_form_field: self.search_value})
            context[self.query_name] = query
            context[self.search_form_field] = self.search_value
        return context

    def get_search_form(self):
        return self.search_form_class(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get(self.search_form_field)

    def get_query(self):
        query = Q()
        for field in self.search_fields:
            kwargs = {field: self.search_value}
            query = query | Q(**kwargs)
        return query
