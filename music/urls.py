from django.urls import path
from . import views

urlpatterns = [
    # --- Authentication ---
    path('', views.login_view, name='login'),          # Root = login
    path('login/', views.login_view, name='login'),    # Explicit login page
    path('logout/', views.logout_view, name='logout'), # Logout

    # --- Account Management ---
    path('register/', views.register_view, name='register'),
    path('delete-account/', views.delete_account_confirm, name='delete_account_confirm'),
    path('delete-account/confirm/', views.delete_account, name='delete_account'),

    # --- Public Pages ---
    path('contact/', views.contact_view, name='contact'),
    path('useful-links/', views.useful_links, name='useful_links'),  # Added Useful Links page

    # --- Protected Pages ---
    path('home/', views.home, name='home'),                            # Optional home page
    path('landing/', views.landing_page, name='landing_page'),         # Music list (main page)
    path('piece/<int:piece_id>/', views.piece_detail, name='piece_detail'),
]
