from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # Include URLs from our 'users' app for authentication
    path("accounts/", include("users.urls")),
    # Include default auth URLs (for login, logout)
    path("accounts/", include("django.contrib.auth.urls")),
    # Include URLs from our 'portal' app for the main site
    path("", include("portal.urls")),
]

# This is required to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)