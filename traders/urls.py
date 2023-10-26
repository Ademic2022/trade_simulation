from django.urls import path
from traders import views


urlpatterns = [
    path('', views.index, name='home'),
    path('simulate_trading/<str:trader_name>/', views.simulate_trading, name='simulate_trading'),
    path('lucky_trader/', views.lucky_trader, name='lucky_trader'),
    path('account/<str:trader_name>/', views.account, name='account'),
    path('dashboard', views.dashboard, name='dashboard'),


]