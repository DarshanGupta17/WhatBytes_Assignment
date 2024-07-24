from django.urls import path
from account.views import Register , Login , Home,changePassword , Logout,show_profile
from account.views import Password_Reset_View, Password_Reset_Done_View, Password_Reset_Confirm_View, Password_Reset_Complete_View

from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('register/',Register,name="register"),
    path('',Login,name="login"),
    path('logout/',Logout,name="logout"),
    path('home/',Home,name="home"),
    path('changePassword/',changePassword,name="changepassword"),
    path('profile/',show_profile,name="profile"),

    path('passwordReset/', Password_Reset_View.as_view(), name='password_reset'),
    path('passwordReset/Done/', Password_Reset_Done_View.as_view(), name='password_reset_done'),
    path('Reset/<uidb64>/<token>/', Password_Reset_Confirm_View.as_view(), name='password_reset_confirm'),
    path('Reset/done/', Password_Reset_Complete_View.as_view(), name='password_reset_complete'),
]
