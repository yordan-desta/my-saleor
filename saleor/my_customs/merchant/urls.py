from django.conf.urls import url

from . import views
from ...core import TOKEN_PATTERN

urlpatterns = [
    url(r'^%s/$' % (TOKEN_PATTERN,), views.details, name='details'),
]
