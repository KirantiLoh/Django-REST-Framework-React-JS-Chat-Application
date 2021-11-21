from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.get_routes, name='Routes'),
    path('token', views.MyTokenObtainPairView.as_view(), name='Token'),
    path('token/refresh', TokenRefreshView.as_view(), name='Refresh Token'),
    path('rooms', views.rooms_view, name='Rooms'),
    path('rooms/<uuid:uid>', views.room_view, name='Room'),
    path('register', views.register_view, name='Register'),
]
