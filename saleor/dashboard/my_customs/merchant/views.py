from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import pgettext_lazy
from django.views.decorators.http import require_POST

from saleor.account.models import User
from saleor.dashboard.my_customs.merchant.forms import MerchantForm
from ....core.utils import get_paginator_items
from ....my_customs.merchant.models import Merchant
from ...views import staff_member_required
from .filters import MerchantFilter
from django.contrib import messages

from . import forms


@staff_member_required
@permission_required('account.manage_merchants')
def merchant_list(request):
    merchants = Merchant.objects.prefetch_related('users')
    merchant_filter = MerchantFilter(request.GET, queryset=merchants)
    merchants = get_paginator_items(
        merchant_filter.qs, settings.DASHBOARD_PAGINATE_BY,
        request.GET.get('page'))
    ctx = {
        'merchants': merchants, 'filter_set': merchant_filter,
        'is_empty': not merchant_filter.queryset.exists()}
    return TemplateResponse(request, 'dashboard/my_customs/merchant/list.html', ctx)


@staff_member_required
@permission_required('account.manage_merchants')
def merchant_create(request):
    merchant = Merchant()
    form = MerchantForm(
        request.POST or None)
    if form.is_valid():
        merchant = form.save()
        user = form.cleaned_data.get('user')
        user.merchant = merchant
        user.is_merchant = True
        User.save(user)
        messages.success(
            request,
            pgettext_lazy(
                'Dashboard message', 'Added merchant %s') % merchant)
        return redirect('dashboard:merchants')
    ctx = {'merchant': merchant, 'form': form}
    return TemplateResponse(request, 'dashboard/my_customs/merchant/form.html', ctx)



def create_merchant_from_draft(merchant_pk, request):
    return None


def merchant_details(merchant_pk, request):
    return None


def merchant_edit(merchant_pk, request):
    return None
