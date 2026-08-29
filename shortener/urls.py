from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # UPDATED CODE: SnapURL Dashboard Logic
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # UPDATED CODE: SnapURL Dashboard Logic
    path('history/', views.history_view, name='history'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('shorten/', views.shorten_url, name='shorten_url'),
    path('<str:short_code>/', views.redirect_url, name='redirect_url'),
    path('delete/<int:url_id>/', views.delete_url, name='delete_url'),   
]