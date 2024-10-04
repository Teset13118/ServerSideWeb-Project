from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("", ViewHome.as_view(), name="url_p_homepage"),
    path("Organizer/", ViewOrganizerHome.as_view(), name="url_o_homepage"),
    path("login/", LoginView.as_view(), name="url_login"),
    path("logout/", LogoutView.as_view(), name="url_logout"),
    path("register/", RegisterView.as_view(), name="url_register"),
    path("selectcategory/", SelectCategory.as_view(), name="url_select_category"),

    path("profile/", ViewProfile.as_view(), name="url_profile"),
    path("profile_edit/", ViewProfileEdit.as_view(), name="url_profile_edit"),

    path("activity/<int:activity_id>", ViewActivity.as_view(), name="url_p_activitypage"),
    path("create_activity/", View_CreateActivity.as_view(), name="url_o_createactivity"),
    path("edit_activity/<int:activity_id>", EditActivity.as_view(), name="url_mo_editactivity"),
    path("delete_activity/<int:activity_id>", DeleteActivity.as_view(), name="url_mo_deleteactivity"),
    
    path("manage/users/", ViewManageUser.as_view(), name="url_m_manageusers"),
    path("manage/users/delete/<int:user_id>/", ViewManageUser.as_view(), name="url_m_deleteusers"),
    path("manage/activities/", ViewManageActivity.as_view(), name="url_m_manageactivities"),
    path("manage/activities/delete/<int:activity_id>/", ViewManageActivity.as_view(), name="url_m_deleteactivities"),
    path("manage/activities/approve/<int:activity_id>/", ViewManageActivity.as_view(), name="url_m_approve_activity")
]

# old
    # path("create_activity/", View_CreateActivity.as_view(), name="url_o_activity_form"),
    # path("edit_activity/<int:activity_id>", EditActivity.as_view(), name="url_mo_editactivity"),
    # path("activity/<int:activity_id>", View_Activity.as_view(), name="url_p_activity_detail"),

# setting for showing media on website
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)