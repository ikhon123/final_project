import re
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from .forms import NoteForm, FolderForm, TagForm, NoteFormUpdate
from .models import Note, Folder, Tag
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
 
#from django.views.decorators.csrf import ensure_csrf_cookie

class NoteList(ListView): #https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-display/
    model = Note
    queryset = Note.objects.all()

    def get_queryset(self):
        folder = self.kwargs['folder']
        if folder == '':
            self.queryset = Note.objects.all()
            return self.queryset
        else:
            self.queryset = Note.objects.filter(folder__title__iexact=folder)
            return self.queryset
    
    
    def get_context_data(self, **kwargs):
        context = super(NoteList, self).get_context_data(**kwargs)
        context['total'] = self.queryset.count()
        return context

class NoteDetail(DetailView):
    model = Note

# class NoteCreate(CreateView):
#     model = Note
#     form_class = NoteForm


class NoteUpdate(UpdateView):
    model = Note
    form_class = NoteFormUpdate
    
class NoteByTag(ListView):
    model = Note
    
    queryset = Note.objects.all()
    def get_queryset(self):
        tags = self.kwargs['tags']
        pieces = tags.split('/') #extract different tags separated by /
        
        queries = [Q(tag__title__iexact=value) for value in pieces]
        # Take one Q object from the list
        query = queries.pop()
        # Or the Q object with the ones remaining in the list
        for item in queries:
            query |= item
        # Query the model
        allnotes = Note.objects.filter(query).distinct().order_by('tag__title')
        self.queryset = allnotes #Setting the queryset to allow get_context_data to apply count
        return allnotes
    
    def get_context_data(self, **kwargs):
        context = super(NoteByTag, self).get_context_data(**kwargs)
        context['total'] = self.queryset.count()
        return context


class MyView(TemplateView):
    folder_form_class = FolderForm
    tag_form_class = TagForm
    note_form_class = NoteForm
    template_name = "notes/note_hybrid.html"

    def get(self, request, *args, **kwargs):
        kwargs.setdefault("createfolder_form", self.folder_form_class())
        kwargs.setdefault("createtag_form", self.tag_form_class())
        kwargs.setdefault("createnote_form", self.note_form_class())
        return super(MyView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form_args = {
            'data': self.request.POST,
        }
        
        if "btn_createfolder" in request.POST['form']:
            form = self.folder_form_class(**form_args)
            if not form.is_valid():
                return self.get(request,
                                   createfolder_form=form)
            else:
                form.save()
                data = Folder.objects.all()
                result_list = list(data.values('id','title'))
                return HttpResponse(json.dumps(result_list, cls=DjangoJSONEncoder))
        elif "btn_createtag" in request.POST['form']:
            form = self.tag_form_class(**form_args)
            if not form.is_valid():
                return self.get(request,
                                   createtag_form=form)
            else:
                form.save() #save the new object
                data = Tag.objects.all() # retrieve all records
                result_list = list(data.values('id','title'))
                return HttpResponse(json.dumps(result_list, cls=DjangoJSONEncoder)) #return to ajax as success with all the new records.
        elif "btn_createnote" in request.POST['form']:
            form = self.note_form_class(**form_args)
            if not form.is_valid():
                return self.get(request,
                                   createnote_form=form) 
            else:
                try:
                    obj = form.save() #save the new object
                except Exception, e:
                    print("errors" + e)
                response = {'status': 1, 'message':'ok'}
                return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder)) #return to ajax as success with all the new records.
            
        return super(MyView, self).get(request)
    

class NoteDelete(DeleteView):
    model = Note
    success_url = reverse_lazy('listall')