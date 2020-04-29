from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("product.urls")),
    path("account/", include('users.urls')),
    # path("search/", TemplateView.as_view(template_name="search/search.html"))
    path("search/", include('search.urls')),
    path("cart/", include("cart.urls")),
    path("orders/", include('orders.urls')),
    path("billing/", include('billing.urls')),
    path("address/", include('addresses.urls')),
    path("payment/", include('payments.urls')),
    path("contact/", include("contact_us.urls"))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
