from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("", ViewHome.as_view(), name="url_p_homepage"),
    path("login/", LoginView.as_view(), name="url_login"),
    path("logout/", LogoutView.as_view(), name="url_logout"),
    path("register/", RegisterView.as_view(), name="url_register"),
    path("activity/<int:activity_id>", ViewActivity.as_view(), name="url_p_activitypage"),
    # path("activity/<int:activity_id>", View_Activity.as_view(), name="url_p_activity_detail"),
    path("create_activity/", View_CreateActivity.as_view(), name="url_o_activity_form"),
    path("manage/users/", ViewManageUser.as_view(), name="url_m_manageusers"),
    path("manage/activities/", ViewManageActivity.as_view(), name="url_m_manageactivities"),

    path("test/", ViewTest.as_view(), name="test"),
]

# setting for showing media on website
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)