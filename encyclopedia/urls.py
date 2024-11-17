from django.urls import path, re_path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r'^wiki/(?P<title>[\w-]+)?/?$', views.get_title, name='get_title'),
    path('random', views.random_encyclopedia, name='random_encyclopedia'),
    path('add/', views.add_encyclopedia, name='add_encyclopedia'),
    path('update/<str:title>/', views.update_encyclopedia, name='update_encyclopedia'),
    path('delete/<str:title>/', views.delete_encyclopedia, name='delete_encyclopedia'),
    path("search/", views.get_query_search, name="get_query_search"),
]
