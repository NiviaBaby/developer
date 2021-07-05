from walletservice import views
from django.urls import path


urlpatterns = [
    path('v1/init', views.InitWalletAPIView.as_view(), name='init_wallet'),
    path('v1/wallet', views.WalletAPIView.as_view(), name='wallet'),
    path('v1/wallet/deposits', views.DepositsAPIView.as_view(), name='deposits'),
    path('v1/wallet/withdrawals', views.WithdrawalAPIView.as_view(), name='withdrawals'),
    
]