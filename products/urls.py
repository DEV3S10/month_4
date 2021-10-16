"""products URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLbconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', views.product_list_view),
    path('api/v1/products/<int:pk>/', views.products_item_view),
    path('api/v1/products/reviews/', views.reviews_list_view),
    path('api/v1/products/tags/', views.active_tags_list_view),
    path('api/v1/categories/', views.categories_list_view),
    path('api/v1/login/', views.login),
    path('api/v1/register/', views.register),
]
