# from django.conf import settings
# from django.contrib import admin
# from django.urls import path, include
#
# from django.conf.urls.static import static
#
#
# urlpatterns = [
#     path('', include('accounts.urls')),
#     path('admin/', admin.site.urls),
#     path('journal/', include('journal.urls')),
#     path('mailing/', include('mailing.urls')),
#     path('api-auth/', include('rest_framework.urls')),
#     path('api/v1/', include('api.v1.urls'))
# ]
#
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.shortcuts import render

# Представление для обработки ошибки 403
def custom_permission_denied_view(request, exception):
    return render(request, 'people/403.html', status=403)

urlpatterns = [
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('journal/', include('journal.urls')),
    path('mailing/', include('mailing.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('api.v1.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Регистрация кастомного обработчика ошибки 403
handler403 = 'django_journal.urls.custom_permission_denied_view'
