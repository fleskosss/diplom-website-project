from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('jewerlies/', views.author_jewelry, name='author_jewelry'),
    path('advices/', views.advices, name='advices'),
    path('advices/<slug:slug>/', views.advice_detail, name='advice_detail'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('public-offer/', views.public_offer, name='public_offer'),
    path('admin-panel/', views.admin_panel_entry, name='admin_panel_entry'),
    path('admin-panel/login/', views.admin_login, name='admin_login'),
    path('admin-panel/profile/', views.admin_profile, name='admin_profile'),
    path('admin-panel/logout/', views.admin_logout, name='admin_logout'),
    re_path(r'^(?P<unknown_path>.*)$', views.custom_404_debug, name='custom_404_debug'),
]