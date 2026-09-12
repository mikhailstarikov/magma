from django.urls import path
from . import views

app_name = "loyalty"

urlpatterns = [
    path("balance/", views.team_balance, name="team_balance"),
    path("transactions/", views.transactions, name="transactions"),
]
