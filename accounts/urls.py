from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('edit_profile/', views.UserEditProfileView.as_view(), name='edit_profile'),
    # one time password
    path('verify/', views.VerifyCode.as_view(), name='verify'),
    # Password change
    path("password_change/", views.PasswordChange.as_view(), name="password_change"),
    path("password_change_done/", views.PasswordChangeDone.as_view(), name="password_change_done"),
    path("password_reset/", views.UserPasswordReset.as_view(), name="password_reset_form"),
    path("password_reset/done/", views.USerPasswordResetDone.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>", views.UserPasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.UserPasswordResetComplete.as_view(), name="password_reset_complete"),

]