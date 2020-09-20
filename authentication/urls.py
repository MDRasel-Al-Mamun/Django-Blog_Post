from .views import *
from django.urls import path
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name="signup"),
    path('sign_in/', SigninView.as_view(), name="signin"),
    path('sign_out/', signoutView, name="signout"),
    path('reset_password/', RequestPasswordResetEmail.as_view(), name="reset_password"),


    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('set_new_password/<uidb64>/<token>', CompletePasswordReset.as_view(), name='reset_user_password'),

    path('validate_username', csrf_exempt(UsernameValidationView.as_view()), name="validate_username"),
    path('validate_email', csrf_exempt(EmailValidationView.as_view()), name='validate_email'),
]
