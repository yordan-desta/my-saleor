from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.template.response import TemplateResponse

from ....core.utils import get_paginator_items
from ....my_customs.merchant.models import Merchant
from ...views import staff_member_required
from .filters import MerchantFilter


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

def merchant_create(request):
    return None


def create_merchant_from_draft(merchant_pk, request):
    return None


def merchant_details(merchant_pk, request):
    return None


def merchant_edit(merchant_pk, request):
    return None
