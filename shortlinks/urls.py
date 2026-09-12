from django.urls import path
from . import views

app_name = "shortlinks"

urlpatterns = [
    path("create/", views.create_short_link, name="create"),
    path("my/", views.my_links, name="my_links"),
    path("<str:short_code>/", views.link_detail, name="link_detail"),
    path("<str:short_code>/delete/", views.delete_link, name="delete"),
]
