from django.urls import path

from .views import add_transaction, get_balance, spend_points

urlpatterns = [
    path('add-transaction/', add_transaction),
    path('get-balance/', get_balance),
    path('spend-points/', spend_points),
]
