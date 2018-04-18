from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('subscribe/<int:series_id>/', views.subscribe, name='subscribe'),
    path('my-series/', views.my_series, name='my-series'),
    path('get-hint/<str:title>/', views.get_hint, name='get-hint'),
]
