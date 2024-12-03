from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Example dashboard URL
    path("signup/", views.signup_view, name="signup"),
    path('emailVerify/',views.emailVerify_view, name='emailVerify')
    path('', views.login_view, name='root'), 
]
#addin gh ga comment auto reload
