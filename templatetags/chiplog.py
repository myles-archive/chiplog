from django.template import Library, Node

from chiplog.settings import CHIPLOG_MEDIA_URL

register = Library()

@register.simple_tag
def chiplog_media_url():
	"""
	Basicly does the same thing as {{ MEDIA_URL }} but
	add the Chiplog media url.
	
	TODO This isn't a good idea.
	"""
	return CHIPLOG_MEDIA_URL
