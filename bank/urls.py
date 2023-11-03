from django.urls import path
from.import views

urlpatterns=[
    path('', views.home),
    path('index', views.home),
    path('sign_up', views.sign_up),
    path('sign_in', views.sign_in),
    path('register', views.register),
    path('login', views.login),
    path('user_dashboard',views.user_dashboard),
    path('money_transfer',views.money_transfer),
    path('sendmoney',views.sendmoney),
    #path('statement',views.statement),
    path('statement',views.statement),
    path('stmt',views.stmt),
    path('custom',views.custom),
    path('cus_stmt',views.cus_stmt),
    path('admin_panel', views.admin_panel,name='admin_panel'),
    path('validate_user/<int:user_id>/', views.validate_user, name='validate_user'),
    path('add_balance/<int:user_id>/', views.add_balance, name='add_balance'),
    path('ad_login/', views.ad_login),
    path('my_profile',views.my_profile),
    path('user_edit',views.user_edit),
    path('change_details',views.change_details),
    path('recover_password',views.recover_password),
    path('fgtpass',views.fgtpass),
    path('resetpass',views.resetpass),
    path('forgot_mpin',views.forgot_mpin),
    path('fgtmpin',views.fgtmpin),
    path('resetmpin',views.resetmpin),
    path('card',views.card),
]
   