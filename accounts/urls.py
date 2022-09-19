from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('edit_profile/', views.UserEditProfileView.as_view(), name='edit_profile'),
    # favourite video
    path('favourite/<int:myid>/', views.User_Favourite_Add.as_view(), name='favourite_add'),
    path('profile/favourites', views.User_Favourite_List.as_view(), name='favourite_list'),
    # masters
    path('masters/', views.UserMastersView.as_view(), name='master'),
    path('masters/profile/<int:pk>', views.user_master_info, name='master_info'),
    # one time password
    path('verify/', views.VerifyCode.as_view(), name='verify'),
    # password change
    path("password_change/", views.PasswordChange.as_view(), name="password_change"),
    path("password_change_done/", views.PasswordChangeDone.as_view(), name="password_change_done"),
    # password reset
    path("password_reset/", views.UserPasswordReset.as_view(), name="password_reset_form"),
    path("password_reset/done/", views.UserPasswordResetDone.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>", views.UserPasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.UserPasswordResetComplete.as_view(), name="password_reset_complete"),

]