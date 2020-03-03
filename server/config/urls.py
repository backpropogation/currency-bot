from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.currency.router import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
