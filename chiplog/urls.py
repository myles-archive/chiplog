from django.conf.urls.defaults import *
from django.views.generic import create_update
from django.views.generic import date_based
from django.views.generic import list_detail
from models import Entry

chiplog_list = {
    'queryset': Entry.objects.all(),
    'template_object_name': 'entry',
    'template_name': 'read.html',
    'paginate_by': 10,
}
chiplog_delete = {
    'model': Entry,
    'template_name': 'delete.html',
    'post_delete_redirect': '/chiplog/',
}
chiplog_save = {
    'model': Entry,
    'template_name': 'create_update.html',
    'extra_context': { 'entry_list': Entry.objects.all },
    'post_save_redirect': '/chiplog/',
}

urlpatterns = patterns('',
    (r'^$', list_detail.object_list, chiplog_list),
    (r'^page/(?P<page>\w)/$', list_detail.object_list, chiplog_list),
    (r'^new/$', create_update.create_object, chiplog_save),
    (r'^edit/(?P<object_id>\d+)/$', create_update.update_object, chiplog_save),
    (r'^delete/(?P<object_id>\d+)/$', create_update.delete_object, chiplog_delete)
)
