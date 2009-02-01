from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import date_based, list_detail, create_update
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings
from chiplog.models import Entry
from chiplog.forms import EntryForm

@permission_required('entries.can_add')
def entry_list(request, page=0):
	if request.POST:
		form = EntryForm(data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('chiplog_index'))
		else:
			return render_to_response('chiplog/entry_form.html', {'form': form}, context_instance=RequestContext(request))
	else:
		return list_detail.object_list(
			request,
			queryset = Entry.objects.all(),
			template_object_name = 'entry',
			template_name = 'chiplog/entry_list.html',
			paginate_by = 10,
			page = page,
			extra_context = { 'form': EntryForm, 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }
		)

@permission_required('entries.can_add')
def entry_detail(request, object_id):
	return list_detail.object_detail(
		request,
		object_id = object_id,
		queryset = Entry.objects.all(),
		template_name = 'chiplog/entry_detail.html',
		extra_context = { 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }
	)

@permission_required('entries.can_delete')
def entry_delete(request, object_id):
	return create_update.delete_object(
		request,
		object_id = object_id,
		model = Entry,
		template_name = 'chiplog/entry_confirm_delete.html',
		post_delete_redirect = reverse('chiplog_index'),
		extra_context = { 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }
	)

@permission_required('entries.can_add')
def entry_create(request):
	return create_update.create_object(
		request,
		model = Entry,
		template_name = 'chiplog/entry_form.html',
		post_save_redirect = reverse('chiplog_index'),
		extra_context = { 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }
	)

@permission_required('entries.can_update')
def entry_update(request, object_id):
	return create_update.update_object(
		request,
		object_id = object_id,
		model = Entry,
		template_name = 'chiplog/entry_form.html',
		post_save_redirect = reverse('chiplog_index'),
		extra_context = { 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }
	)

@permission_required('entries.can_add')
def search(request):
	if request.GET:
		search_term = '%s' % request.GET['s']
		if len(search_term) != 0:
			entry_list = Entry.objects.filter(body__icontains=search_term)
			context = { 'entry_list': entry_list, 'search_term':search_term, 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }
			return render_to_response('chiplog/entry_search.html', context, context_instance=RequestContext(request))
		else:
			message = 'Search term was too vague. Please try again.'
			context = { 'message':message, 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }
			return render_to_response('chiplog/entry_search.html', context, context_instance=RequestContext(request))
	else:
		return render_to_response('chiplog/entry_search.html', { 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }, context_instance=RequestContext(request))
=======
@login_required
def entry_list(request, page=0):
    """
    Dual-purpose view: add new Entries / view paginated list of Entires.
    """
    if request.POST:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            form.save()
            # request.user.message_set.create(message="Entry created.")
            return HttpResponseRedirect(reverse('chiplog_index'))
        else:
            return render_to_response('chiplog/entry_form.html', {'form': form, 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL})
    else:
        return list_detail.object_list(
            request,
            queryset = Entry.objects.all(),
            template_object_name = 'entry',
            paginate_by = 10,
            page = page,
            extra_context = { 'form': EntryForm, 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }
        )

@login_required
def tagged_list(request, tag):
    """
    All entries for a particular tag.
    """
    return list_detail.object_list(
        request,
        queryset = Entry.objects.filter(tags__icontains=tag),
        template_name = 'chiplog/entry_tagged.html',
        template_object_name = 'entry',
        extra_context = { 'tag': tag, 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }
    )

@login_required
def entry_detail(request, object_id):
    return list_detail.object_detail(
        request,
        object_id = object_id,
        queryset = Entry.objects.all(),
        template_object_name = 'entry',
        extra_context = { 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }
    )

@login_required
def entry_delete(request, object_id):
    return create_update.delete_object(
        request,
        object_id = object_id,
        model = Entry,
        post_delete_redirect = reverse('chiplog_index'),
        template_object_name = 'entry',
        extra_context = { 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }
    )

@login_required
def entry_create(request):
    return create_update.create_object(
        request,
        model = Entry,
        post_save_redirect = reverse('chiplog_index'),
        extra_context = { 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }
    )

@login_required
def entry_update(request, object_id):
    return create_update.update_object(
        request,
        object_id = object_id,
        model = Entry,
        # post_save_redirect = request.POST['referrer'],
        template_object_name = 'entry',
        extra_context = { 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL },
    )

@login_required
def search(request):
    if request.GET:
        try:
            query = request.GET['q']
        except KeyError:
            # If they use the wrong query string (?s instead of ?q).
            message = 'Something has gone wrong, champ. Try again.'
            context = { 'message':message, 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }
            return render_to_response('chiplog/entry_search.html', context, context_instance=RequestContext(request))
        if len(query) != 0:
            entry_list = Entry.objects.filter(body__icontains=query)
            context = { 'entry_list': entry_list, 'query':query, 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }
            return render_to_response('chiplog/entry_search.html', context, context_instance=RequestContext(request))
        else:
            message = 'Search term was too vague. Please try again.'
            context = { 'message':message, 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }
            return render_to_response('chiplog/entry_search.html', context, context_instance=RequestContext(request))
    else:
        return render_to_response('chiplog/entry_search.html', { 'chiplog_media_url': settings.CHIPLOG_MEDIA_URL }, context_instance=RequestContext(request))
