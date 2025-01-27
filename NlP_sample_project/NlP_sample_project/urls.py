from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('nlp_app.urls')),  # This will point to the root of nlp_app.urls
    path('admin/', admin.site.urls),
]
