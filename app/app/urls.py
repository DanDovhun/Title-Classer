
from django.contrib import admin
from django.urls import path
from users_panel import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.user_dashboard, name='user'),
    #path("admin-dashboard/", views.admin_dashboard, name="admin")
]