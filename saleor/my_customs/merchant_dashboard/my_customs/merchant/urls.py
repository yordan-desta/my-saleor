from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.merchant_list, name='merchants'),
    url(r'^add/$', views.merchant_create, name='merchant-create'),
    url(r'^(?P<merchant_pk>\d+)/create/$',
        views.create_merchant_from_draft, name='create-merchant-from-draft'),
    url(r'^(?P<merchant_pk>\d+)/$',
        views.merchant_details, name='merchant-details'),
    url(r'^(?P<merchant_pk>\d+)/edit-merchant/$',
        views.merchant_edit, name='merchant-edit')
   ]
