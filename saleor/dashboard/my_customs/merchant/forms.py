from django import forms
from django.urls import reverse_lazy
from django.utils.translation import pgettext_lazy

from saleor.account.models import User
from saleor.dashboard.forms import AjaxSelect2ChoiceField, ModelChoiceOrCreationField
from ....my_customs.merchant.models import Merchant, PENDING


class MerchantForm(forms.ModelForm):
    user = ModelChoiceOrCreationField(
        queryset=User.objects.get_queryset(),

        label=pgettext_lazy(
            'Label for merchant form', 'Merchant account admin'))

    class Meta:
        model = Merchant
        fields = ['user', 'company_name', 'company_desc', 'company_phone', 'status']
        labels = {
            'company_name': pgettext_lazy(
                'Company name', 'Company name'
            ),
            'company_phone': pgettext_lazy(
                'Phone', 'Phone'
            ),
            'company_desc': pgettext_lazy(
                'Description', 'Description'
            ),
            'status': pgettext_lazy(
                'Status', 'Status'
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = PENDING
