from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'), 
    path("signup/", views.signup_view, name="signup"),
    path('emailVerify/',views.emailVerify_view, name='emailVerify'),
    path('settings/', views.settingView, name='settings'),
    path('add_routine/', views.addRView, name='add_routine'),
    path('', views.login_view, name='root'), 
]

