from django import forms
from django.db.models import Q
from django.utils.translation import npgettext, pgettext_lazy
from django_filters import (
    CharFilter, ChoiceFilter, DateFromToRangeFilter, NumberFilter,
    OrderingFilter)

from saleor.core.filters import SortedFilterSet
from ....my_customs.merchant.models import MERCHANT_ACCOUNT_STATUS, Merchant
from ...widgets import DateRangeWidget

SORT_BY_FIELDS = [
    ('pk', 'pk'),
    ('status', 'status'),
    ('created_on', 'created_on')]

SORT_BY_FIELDS_LABELS = {
    'pk': pgettext_lazy('Order list sorting option', '#'),
    'status': pgettext_lazy(
        'Merchant list sorting option', 'status'),
    'created_on': pgettext_lazy('Merchant list sorting option', 'created_on')}


class MerchantFilter(SortedFilterSet):
    id = NumberFilter(
        label=pgettext_lazy('Merchant list filter label', 'ID'))
    name_or_email = CharFilter(
        label=pgettext_lazy(
            'Merchant list filter label', 'Merchant name or email'),
        method='filter_by_merchant_name_or_email')
    created = DateFromToRangeFilter(
        label=pgettext_lazy('Merchant list filter label', 'Registered on'),
        field_name='created_on', widget=DateRangeWidget)
    status = ChoiceFilter(
        label=pgettext_lazy(
            'Merchant list filter label', 'Merchant status'),
        choices=MERCHANT_ACCOUNT_STATUS,
        empty_label=pgettext_lazy('Filter empty choice label', 'All'),
        widget=forms.Select)

    sort_by = OrderingFilter(
        label=pgettext_lazy('Merchant list filter label', 'Sort by'),
        fields=SORT_BY_FIELDS,
        field_labels=SORT_BY_FIELDS_LABELS)

    class Meta:
        model = Merchant
        fields = []

    def filter_by_merchant_name_or_email(self, queryset, name, value):
        return queryset.filter(
            Q(company_name__icontains=value) |
            Q(company_email__icontains=value))

    def get_summary_message(self):
        counter = self.qs.count()
        return npgettext(
            'Number of matching records in the dashboard merchants list',
            'Found %(counter)d matching merchant',
            'Found %(counter)d matching merchants',
            number=counter) % {'counter': counter}
