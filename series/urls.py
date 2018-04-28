##
# @file
# Itt találhatóak az alkalmazásból elérhető útvonalak.
#

from django.urls import path, include

from . import views

# Documented var \c urlpatterns .
# Itt találhatóak az alkalmazásból elérhető útvonalak.
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('myprofile/', views.my_profile, name='myprofile'),
    path('subscribe/<int:series_id>/', views.subscribe, name='subscribe'),
    path('unsubscribe/<int:series_id>/', views.unsubscribe, name='unsubscribe'),
    path('my-series/', views.my_series, name='my-series'),
    path('get-hint/<str:title>/', views.get_hint, name='get-hint'),
]
