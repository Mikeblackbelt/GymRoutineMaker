from django.urls import path
from . import views  # Import views from the same app

urlpatterns = [
    # This will route the base URL for 'gymplan/' to the 'index' view
    path('', views.index, name='index'),
]
