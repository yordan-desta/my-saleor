from django.conf.urls import include, url
from django.views.generic.base import TemplateView

from . import views as core_views
from .collection.urls import urlpatterns as collection_urls
from .discount.urls import urlpatterns as discount_urls
from .order.urls import urlpatterns as order_urls
from .product.urls import urlpatterns as product_urls
from .search.urls import urlpatterns as search_urls
from .taxes.urls import urlpatterns as taxes_urls

urlpatterns = [
    url(r'^$', core_views.index, name='index'),
    # url(r'^categories/', include(category_urls)),
    url(r'^collections/', include(collection_urls)),
    url(r'^orders/', include(order_urls)),
    url(r'^products/', include(product_urls)),
    # url(r'^customers/', include(customer_urls)),
    # url(r'^staff/', include(staff_urls)),
    url(r'^discounts/', include(discount_urls)),
    # url(r'^menu/', include(menu_urls)),
    # url(r'^shipping/', include(shipping_urls)),
    url(r'^style-guide/', core_views.styleguide, name='styleguide'),
    url(r'^search/', include(search_urls)),
    url(r'^taxes/', include(taxes_urls)),
    url(r'^next/', TemplateView.as_view(template_name='dashboard/next.html')),
]
