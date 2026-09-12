from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from shortlinks import views as shortlinks_views  # ← Импортируем

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('boost/', include('boost.urls')),
    path('loyalty/', include('loyalty_program.urls')),
    path('links/', include('shortlinks.urls')),
    path('s/<str:short_code>', shortlinks_views.redirect_to_original, name='redirect'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)