from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("", View_CreateActivity.as_view(), name="create_activity"),
    path("index/", index.as_view(), name="asdasd"),
]