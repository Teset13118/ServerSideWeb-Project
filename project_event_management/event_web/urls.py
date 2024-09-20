from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("", View_CreateActivity.as_view(), name="create_activity"),
    path("activity/<int:activity_id>", View_Activity.as_view(), name="asdasd"),
    path("index/", index.as_view(), name="asdasd"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)