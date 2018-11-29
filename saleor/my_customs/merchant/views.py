from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from saleor.my_customs.merchant.models import Merchant


def details(request, token):
    merchants = Merchant.objects.all()
    merchant = get_object_or_404(merchants, token=token)

    ctx = {
        'merchant': merchant}
    return TemplateResponse(request, 'my_customs/merchant/details.html', ctx)

