from django.conf.urls import patterns, include, url
from django.contrib import admin
from notes import views


from django.views.generic import ListView, DetailView
from notes.models import Note, Folder, Tag

from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', views.Landing.as_view(), name="landing"),
    url(r'^add/$', views.MyView.as_view(), name="note_add"),
    url(r'^allfolders$', ListView.as_view(model=Folder), name='allfolders'), 
    url(r'^alltags$', ListView.as_view(model=Tag), name='alltags'),
    url(r'^list/(?P<folder>.*)$', views.NoteList.as_view(), name='note_list'),
    url(r'^note/(?P<pk>\d+)/edit/$', views.NoteUpdate.as_view(),  name='note_update'),
    url(r'^note/(?P<pk>\d+)/delete/$', views.NoteDelete.as_view(),  name='note_delete'),
    url(r'^note/(?P<pk>\d+)$', views.NoteDetail.as_view(),  name='detail'),
    url(r'^tag/(?P<tags>.*)$', views.NoteByTag.as_view(), name='note_listtag'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
) 
