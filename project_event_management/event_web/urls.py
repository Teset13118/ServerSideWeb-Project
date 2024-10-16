from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("", ViewHome.as_view(), name="url_p_homepage"),
    path("Home_activities/", ViewHomeActivity.as_view(), name="url_p_homepage_activity"),
    path("Organizer/", ViewOrganizerHome.as_view(), name="url_o_homepage"),
    
    path("login/", LoginView.as_view(), name="url_login"),
    path("logout/", LogoutView.as_view(), name="url_logout"),
    path("register/", RegisterView.as_view(), name="url_register"),
    path("changepassword/", ChangePasswordView.as_view(), name="url_changepassword"),
    path("selectcategory/<int:user_id>/", SelectCategory.as_view(), name="url_p_select_category"),

    path("profile/", ViewProfile.as_view(), name="url_profile"),
    path("profile_edit/", ViewProfileEdit.as_view(), name="url_profile_edit"),

    path("activity/<int:activity_id>/", ViewActivity.as_view(), name="url_activitypage"),
    path("activity/reviews/delete/<int:review_id>/", ViewActivity.as_view(), name="url_delete_review"),
    path("create_activity/", View_CreateActivity.as_view(), name="url_o_createactivity"),
    path("registration_list/<int:activity_id>/", ViewRegistrationUserList.as_view(), name="url_registration_list"),
    path("edit_activity/<int:activity_id>/", EditActivity.as_view(), name="url_mo_editactivity"),
    path("delete_activity/<int:activity_id>/", DeleteActivity.as_view(), name="url_mo_deleteactivity"),
    
    path("manage/users/", ViewManageUser.as_view(), name="url_m_manageusers"),
    path("manage/users/delete/<int:user_id>/", ViewManageUser.as_view(), name="url_m_deleteusers"),
    path("manage/activities/", ViewManageActivity.as_view(), name="url_m_manageactivities"),
    path("manage/activities/delete/<int:activity_id>/", ViewManageActivity.as_view(), name="url_m_deleteactivities"),
    path("manage/activities/approve/<int:activity_id>/", ViewManageActivity.as_view(), name="url_m_approve_activity"),
    path("manage/reviews/", ViewManageReview.as_view(), name="url_m_managereviews"),
    path("manage/reviews/delete/<int:review_id>/", ViewManageReview.as_view(), name="url_m_deletereview"),
]

# setting for showing media on website
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)