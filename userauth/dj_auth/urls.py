from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

urlpatterns = [
    #     path("python", views.DumpPython.as_view(), name="python"),
    #     # path("login/", auth_views.LoginView.as_view(), name="login"),
    #     # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("home", views.home, name="home"),
    path('log_in', views.log_in, name='log_in'),
    path('log_out', views.log_out, name='log_out'),
    path('perm/<int:user_id>', views.user_gains_perm, name="user_gains_perm"),
    path("profile/<int:user_id>", views.user_profile, name="user_profile"),
    path("profile2/<int:user_id>", views.user_profile2, name="user_profile2"),
    path("lrm", views.MyView.as_view(), name="lrm"),
    path("test", views.my_view, name="test"),
    path("test2", views.my_view2, name="test2"),
    path("test3", views.MyView2.as_view(), name="test3"),
    path("perm", views.perm, name="perm"),
    path("perm2", views.perm2.as_view(), name="perm2"),
    path("changepw", views.pw_change, name="changepw"),
    path('change-password/', auth_views.PasswordChangeView.as_view()),
]
