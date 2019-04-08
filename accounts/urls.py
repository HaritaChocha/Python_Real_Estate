from django.urls import path, include
from accounts import views

app_name = "accounts"

urlpatterns = [
    # Registration and User Models
    path('register', views.register, name="register"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('changepassword', views.changePassword, name="changePassword"),
    path('firstlogin/', views.firstLoginPassword, name="firstLoginPassword"),

    # Profile
    path('update/profile/<username>', views.updateProfile, name="updateProfile" ),
    path('view/profile/<username>', views.ViewProfile, name="viewProfile" ),

    # User Activation
    path('activate', views.activation, name="activation"),
    path('activate/<username>', views.activateUser, name="activateUser"),

]