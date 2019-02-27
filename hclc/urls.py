"""hclc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from decisiontree.views import product_detail_view, product_create_view
from pages.views import home_view, contact_view
from question.views import show_question
from builder.views import build_tree_view, builder_demo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('contact/', contact_view),
    path('product/', product_detail_view),
    path('create/', product_create_view),
    path('question/', show_question),
    path('builder/', build_tree_view),
    path('builder_demo/', builder_demo),

]
