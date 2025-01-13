from django.urls import path
from .views import loginViews, mainViews, routineViews

urlpatterns = [
    path('login/', loginViews.login_view, name='login'),
    path('dashboard/', mainViews.dashboard_view, name='dashboard'), 
    path("signup/", loginViews.signup_view, name="signup"),
    path('emailVerify/',loginViews.emailVerify_view, name='emailVerify'),
    path('settings/', mainViews.settingView, name='settings'),
    path('dashboard/add_routine/', routineViews.addRView, name='add_routine'),
    path('dashboard/add_routine/routineConfig/<str:goal_key>/', routineViews.rgm_View, name='routine_gen'), #http://127.0.0.1:8000/dashboard/add_routine/routineConfig/Fitness-General-Health/
    path('dashboard/add_routine/generating', routineViews.genRoutine, name='generating'),
    path('dashboard/viewRoutine/<str:routineID>/', routineViews.viewRoutine, name='routine_view'),
    path('', loginViews.login_view, name='root'), 
]

 
 