"""opendecision URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from builder.views import node_create_view, node_edit_view, load_answer_field, load_logic_field, load_nodes
from pages.views import home_view, contact_view, test_view
from interpreter.views import show_interpreter
from dashboard.views import dashboard_view, add_tree, tree_view, export_tree, set_as_endnode, delete_node, delete_tree

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', home_view, name='home'),
    path('contact/', contact_view),
    path('interpreter/', show_interpreter),
    path('trees/', dashboard_view),
    path('test/', test_view),

    path('ajax/load_answer_field/', load_answer_field, name='ajax_load_answer_field'),
    path('ajax/load_logic_field/', load_logic_field, name='ajax_load_logic_field'),
    path('ajax/add_tree/', add_tree, name='add_tree'),
    path('ajax/load_nodes/', load_nodes, name='ajax_load_nodes'),
    path('ajax/set_as_endnode/', set_as_endnode, name='ajax_set_as_endnode'),
    path('ajax/delete_node/', delete_node, name='ajax_delete_node'),
    path('ajax/delete_tree/', delete_tree, name='ajax_delete_tree'),

    path('dashboard/', dashboard_view),
    path('trees/<str:slug>/', tree_view, name='tree_view'),
    path('trees/<str:slug>/create', node_create_view, name='node_create_view'),
    path('trees/<str:slug>/<str:node_slug>/edit', node_edit_view, name='node_edit_view'),
    path('trees/<str:slug>/export', export_tree, name='export_tree_view'),


]
