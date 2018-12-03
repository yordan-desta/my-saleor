from datetime import date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import pgettext_lazy

from saleor.my_customs.merchant.models import Merchant
from . import forms
from ....core.utils import get_paginator_items
from ....discount import VoucherType
from ....discount.models import Sale, Voucher
from ..views import staff_member_required
from .filters import SaleFilter, VoucherFilter


def get_voucher_type_forms(voucher, data):
    """Return a dict of specific voucher type forms."""
    return {
        VoucherType.SHIPPING: forms.ShippingVoucherForm(
            data or None, instance=voucher, prefix=VoucherType.SHIPPING),
        VoucherType.VALUE: forms.ValueVoucherForm(
            data or None, instance=voucher, prefix=VoucherType.VALUE),
        VoucherType.PRODUCT: forms.ProductVoucherForm(
            data or None, instance=voucher, prefix=VoucherType.PRODUCT),
        VoucherType.COLLECTION: forms.CollectionVoucherForm(
            data or None, instance=voucher, prefix=VoucherType.COLLECTION),
        VoucherType.CATEGORY: forms.CategoryVoucherForm(
            data or None, instance=voucher, prefix=VoucherType.CATEGORY)}


@staff_member_required
@permission_required('discount.manage_discounts')
def sale_list(request):
    user = request.user
    if not user.is_authenticated:
        return  # todo: return unauthorized page
    merchant = Merchant.objects.get_merchant_of_user(user)
    if not merchant:
        return TemplateResponse(request, 'my_customs/merchant_dashboard/not_registered.html')

    sales = Sale.objects.get_by_merchant(merchant).prefetch_related('products').order_by('name')
    sale_filter = SaleFilter(request.GET, queryset=sales)
    sales = get_paginator_items(
        sale_filter.qs, settings.DASHBOARD_PAGINATE_BY,
        request.GET.get('page'))
    ctx = {
        'sales': sales, 'filter_set': sale_filter,
        'is_empty': not sale_filter.queryset.exists()}
    return TemplateResponse(request, 'my_customs/merchant_dashboard/discount/sale/list.html', ctx)


@staff_member_required
@permission_required('discount.manage_discounts')
def sale_add(request):
    user = request.user
    if not user.is_authenticated:
        return  # todo: return unauthorized page
    merchant = Merchant.objects.get_merchant_of_user(user)
    if not merchant:
        return TemplateResponse(request, 'my_customs/merchant_dashboard/not_registered.html')

    sale = Sale()
    form = forms.SaleForm(request.POST or None, instance=sale, merchant = merchant)
    if form.is_valid():
        sale = form.save()
        msg = pgettext_lazy('Sale (discount) message', 'Added sale')
        messages.success(request, msg)
        return redirect('merchant_dashboard:sale-update', pk=sale.pk)
    ctx = {'sale': sale, 'form': form}
    return TemplateResponse(request, 'my_customs/merchant_dashboard/discount/sale/form.html', ctx)


@staff_member_required
@permission_required('discount.manage_discounts')
def sale_edit(request, pk):
    user = request.user
    if not user.is_authenticated:
        return  # todo: return unauthorized page
    merchant = Merchant.objects.get_merchant_of_user(user)
    if not merchant:
        return TemplateResponse(request, 'my_customs/merchant_dashboard/not_registered.html')

    sale = get_object_or_404(Sale.objects.get_by_merchant(merchant), pk=pk)
    form = forms.SaleForm(request.POST or None, instance=sale, merchant=merchant)
    if form.is_valid():
        sale = form.save()
        msg = pgettext_lazy('Sale (discount) message', 'Updated sale')
        messages.success(request, msg)
        return redirect('merchant_dashboard:sale-update', pk=sale.pk)
    ctx = {'sale': sale, 'form': form}
    return TemplateResponse(request, 'my_customs/merchant_dashboard/discount/sale/form.html', ctx)


@staff_member_required
@permission_required('discount.manage_discounts')
def sale_delete(request, pk):
    user = request.user
    if not user.is_authenticated:
        return  # todo: return unauthorized page
    merchant = Merchant.objects.get_merchant_of_user(user)
    if not merchant:
        return TemplateResponse(request, 'my_customs/merchant_dashboard/not_registered.html')

    instance = get_object_or_404(Sale.objects.get_by_merchant(merchant), pk=pk)
    if request.method == 'POST':
        instance.delete()
        msg = pgettext_lazy(
            'Sale (discount) message', 'Removed sale %s') % (instance.name,)
        messages.success(request, msg)
        return redirect('merchant_dashboard:sale-list')
    ctx = {'sale': instance}
    return TemplateResponse(
        request, 'my_customs/merchant_dashboard/discount/sale/modal/confirm_delete.html', ctx)


@staff_member_required
@permission_required('discount.manage_discounts')
def voucher_list(request):
    user = request.user
    if not user.is_authenticated:
        return  # todo: return unauthorized page
    merchant = Merchant.objects.get_merchant_of_user(user)
    if not merchant:
        return TemplateResponse(request, 'my_customs/merchant_dashboard/not_registered.html')

    vouchers = (Voucher.objects.get_by_merchant(merchant).prefetch_related('products', 'collections')
                .order_by('name'))
    voucher_filter = VoucherFilter(request.GET, queryset=vouchers)
    vouchers = get_paginator_items(
        voucher_filter.qs, settings.DASHBOARD_PAGINATE_BY,
        request.GET.get('page'))
    ctx = {
        'vouchers': vouchers, 'filter_set': voucher_filter,
        'is_empty': not voucher_filter.queryset.exists()}
    return TemplateResponse(
        request, 'my_customs/merchant_dashboard/discount/voucher/list.html', ctx)


@staff_member_required
@permission_required('discount.manage_discounts')
def voucher_add(request):
    user = request.user
    if not user.is_authenticated:
        return  # todo: return unauthorized page
    merchant = Merchant.objects.get_merchant_of_user(user)
    if not merchant:
        return TemplateResponse(request, 'my_customs/merchant_dashboard/not_registered.html')

    voucher = Voucher()
    type_base_forms = get_voucher_type_forms(voucher, request.POST)
    voucher_form = forms.VoucherForm(request.POST or None, instance=voucher, merchant = merchant)
    if voucher_form.is_valid():
        voucher_type = voucher_form.cleaned_data.get('type')
        form_type = type_base_forms.get(voucher_type)

        if form_type is None:
            voucher = voucher_form.save()
        elif form_type.is_valid():
            voucher = form_type.save()
            voucher.merchant = merchant
            Voucher.save(voucher)

        if form_type is None or form_type.is_valid():
            msg = pgettext_lazy('Voucher message', 'Added voucher')
            messages.success(request, msg)
            return redirect('merchant_dashboard:voucher-list')
    ctx = {
        'voucher': voucher, 'default_currency': settings.DEFAULT_CURRENCY,
        'form': voucher_form, 'type_base_forms': type_base_forms}
    return TemplateResponse(
        request, 'my_customs/merchant_dashboard/discount/voucher/form.html', ctx)


@staff_member_required
@permission_required('discount.manage_discounts')
def voucher_edit(request, pk):
    user = request.user
    if not user.is_authenticated:
        return  # todo: return unauthorized page
    merchant = Merchant.objects.get_merchant_of_user(user)
    if not merchant:
        return TemplateResponse(request, 'my_customs/merchant_dashboard/not_registered.html')

    voucher = get_object_or_404(Voucher.objects.get_by_merchant(merchant), pk=pk)
    type_base_forms = get_voucher_type_forms(voucher, request.POST)
    voucher_form = forms.VoucherForm(request.POST or None, instance=voucher, merchant = merchant)
    if voucher_form.is_valid():
        voucher_type = voucher_form.cleaned_data.get('type')
        form_type = type_base_forms.get(voucher_type)

        if form_type is None:
            voucher = voucher_form.save()
        elif form_type.is_valid():
            voucher = form_type.save()
            voucher.merchant = merchant
            Voucher.save(voucher)

        if form_type is None or form_type.is_valid():
            msg = pgettext_lazy('Voucher message', 'Updated voucher')
            messages.success(request, msg)
            return redirect('merchant_dashboard:voucher-list')
    ctx = {
        'voucher': voucher, 'default_currency': settings.DEFAULT_CURRENCY,
        'form': voucher_form, 'type_base_forms': type_base_forms}
    return TemplateResponse(
        request, 'my_customs/merchant_dashboard/discount/voucher/form.html', ctx)


@staff_member_required
@permission_required('discount.manage_discounts')
def voucher_delete(request, pk):
    user = request.user
    if not user.is_authenticated:
        return  # todo: return unauthorized page
    merchant = Merchant.objects.get_merchant_of_user(user)
    if not merchant:
        return TemplateResponse(request, 'my_customs/merchant_dashboard/not_registered.html')

    instance = get_object_or_404(Voucher.objects.get_by_merchant(merchant), pk=pk)
    if request.method == 'POST':
        instance.delete()
        msg = pgettext_lazy(
            'Voucher message', 'Removed voucher %s') % (instance,)
        messages.success(request, msg)
        return redirect('merchant_dashboard:voucher-list')
    ctx = {'voucher': instance}
    return TemplateResponse(
        request, 'my_customs/merchant_dashboard/discount/voucher/modal/confirm_delete.html', ctx)


@staff_member_required
@permission_required('discount.manage_discounts')
def ajax_voucher_list(request):
    user = request.user
    if not user.is_authenticated:
        return  # todo: return unauthorized page
    merchant = Merchant.objects.get_merchant_of_user(user)
    if not merchant:
        return TemplateResponse(request, 'my_customs/merchant_dashboard/not_registered.html')

    queryset = Voucher.objects.get_by_merchant(merchant).active(date=date.today())

    search_query = request.GET.get('q', '')
    if search_query:
        queryset = queryset.filter(Q(name__icontains=search_query))

    vouchers = [
        {'id': voucher.pk, 'text': str(voucher)} for voucher in queryset]
    return JsonResponse({'results': vouchers})
