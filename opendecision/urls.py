"""opendecision URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.urls import path, re_path, include
from django.views.i18n import JavaScriptCatalog
from django.views.decorators.csrf import csrf_exempt

from allauth.account.views import LoginView
from graphene_django.views import GraphQLView

from builder.views import node_create_view, node_edit_view, load_input_form, load_logic_module, load_nodes, load_token
from pages.views import home_view, contact_view, test_view,show_published_tree, get_published_tree, lang_view, logout_redirect
from dashboard.views import (dashboard_view, published_tree_view, add_tree, tree_view, export_tree,
                            set_as_endnode, delete_node, delete_tree, export_file,
                            load_tree, unpublish_tree)
from visualbuilder.views import visualbuilder_view, load_node_form


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('logout-redirect', logout_redirect, name='logout-redirect'),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),

    path('',  LoginView.as_view()),
    path('contact/', contact_view),
    path('trees/', dashboard_view),
    path('test/', test_view),
    path('lang/', lang_view),
    path('publish/<str:slug>/', show_published_tree , name='publish'),

    path('ajax/load_input_form/', load_input_form, name='ajax_load_input_form'),
    path('ajax/load_logic_module/', load_logic_module, name='ajax_load_logic_module'),
    path('ajax/load_node_form/', load_node_form, name='ajax_load_node_form'),
    path('ajax/add_tree/', add_tree, name='add_tree'),
    path('ajax/load_nodes/', load_nodes, name='ajax_load_nodes'),
    path('ajax/set_as_endnode/', set_as_endnode, name='ajax_set_as_endnode'),
    path('ajax/delete_node/', delete_node, name='ajax_delete_node'),
    path('ajax/delete_tree/', delete_tree, name='ajax_delete_tree'),
    path('ajax/load_token/', load_token, name='ajax_load_token'),
    path('ajax/load_tree/', load_tree, name='ajax_load_tree'),
    path('ajax/unpublish_tree/', unpublish_tree, name='ajax_unpublish_tree'),
    path('ajax/get_published_tree/', get_published_tree, name='ajax_get_published_tree'),


    path('dashboard/', dashboard_view),
    path('published-trees/', published_tree_view, name='published_trees'),
    path('trees/<str:slug>/', tree_view, name='tree_view'),
    path('trees/<str:slug>/create', node_create_view, name='node_create_view'),
    path('trees/<str:slug>/<str:node_slug>/edit', node_edit_view, name='node_edit_view'),
    path('trees/<str:slug>/export', export_tree, name='export_tree_view'),
    path('trees/<str:slug>/export/output', export_file, name='export_file'),

    path('visualbuilder/', visualbuilder_view, name='visualbuilder'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('',  home_view, name='home_view')
    ] + urlpatterns

# Error pages
handler403 = 'pages.views.handler403'
handler404 = 'pages.views.handler404'
handler500 = 'pages.views.handler500'
