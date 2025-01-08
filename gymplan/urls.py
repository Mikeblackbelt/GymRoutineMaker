from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'), 
    path("signup/", views.signup_view, name="signup"),
    path('emailVerify/',views.emailVerify_view, name='emailVerify'),
    path('settings/', views.settingView, name='settings'),
    path('dashboard/add_routine/', views.addRView, name='add_routine'),
    path('dashboard/add_routine/routineConfig/<str:goal_key>/', views.rgm_View, name='routine_gen'),
    path('', views.login_view, name='root'), 
]

 
