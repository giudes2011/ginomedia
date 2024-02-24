from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('profili/', views.profilelist, name='profilelist'),
    path('profilo/<int:pk>', views.userprofile, name='profile'),
    path('accedi/', views.loginuser, name='login'),
    path('disconetti/', views.logoutuser, name='logout'),
    path('registrati/', views.registeruser, name='register'),
    path('aggiorna_profilo/', views.updateuser, name='updateuser'),
    path('postlike/<int:pk>', views.postlike, name='postlike'),
    path('postshare/<int:pk>', views.postshare, name='postshare'),
    path('postdelete/<int:pk>', views.postdelete, name='postdelete'),
    path('postedit/<int:pk>', views.postedit, name='postedit'),
    path('cerca/', views.searchpost, name='search'),
    path('cercaprofilo/', views.searchuser, name='searchuser'),
]
