from django.conf.urls import patterns, include, url
from django.contrib import admin
from notes import views

from django.views.generic import ListView, DetailView
from notes.models import Note, Folder, Tag

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Note), name="listall"),
    url(r'^add/$', views.MyView.as_view(), name="note_add"),
    url(r'^allfolders$', ListView.as_view(model=Folder), name='allfolders'), 
    url(r'^alltags$', ListView.as_view(model=Tag), name='alltags'),
    url(r'^list/(?P<folder>.*)$', views.NoteList.as_view(), name='note_list'),
    #url(r'^addnc/$', views.NoteCreate.as_view(), name='note_add_old'),
    url(r'^note/(?P<pk>\d+)/edit/$', views.NoteUpdate.as_view(),  name='note_update'),
    url(r'^note/(?P<pk>\d+)/delete/$', views.NoteDelete.as_view(),  name='note_delete'),
    url(r'^note/(?P<pk>\d+)$', views.NoteDetail.as_view(),  name='detail'),
    url(r'^tag/(?P<tags>.*)$', views.NoteByTag.as_view(), name='note_listtag'),
    url(r'^admin/', include(admin.site.urls)),
)
