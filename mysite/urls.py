from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView  # Import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='gymplan/', permanent=False)),  # Redirect root to gymplan/
    path('gymplan/', include('gymplan.urls')),
    path('admin/', admin.site.urls),
]

