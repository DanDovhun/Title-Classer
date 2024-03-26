from django.contrib import admin
from django.urls import path
from users_panel import views as userViews
from admin_panel import views as adminViews

urlpatterns = [
    path("", userViews.user_dashboard, name="user"),
    path("prediction/", userViews.user_prediction, name="user_prediction"),
    path("login/", adminViews.admin_login, name="admin_login"),
    path("admin/model/", adminViews.admin_model, name="admin_model"),
    path("admin/reports/", adminViews.admin_reports, name="admin_reports"),
    path("admin/admins/", adminViews.admin_admins, name="admin_admins"),
    path("logout/", adminViews.admin_logout, name="admin_logout"),
    path("retrain/", adminViews.retrain),
    path("test/", admin.site.urls),
]
