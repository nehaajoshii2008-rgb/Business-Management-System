"""
Inventory App URL Configuration.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Public Landing Page & Auth
    path('', views.landing_page_view, name='landing'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/delete-account/', views.delete_account_view, name='delete_account'),

    # Super Admin Dashboard & KYC Approval
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('api/admin/verify-kyc/<int:store_id>/', views.api_admin_verify_kyc, name='api_admin_verify_kyc'),

    # POS Billing Terminal
    path('pos/', views.pos_view, name='pos'),

    # Inventory Stock Control & Bulk Excel/CSV Import
    path('inventory/', views.inventory_list_view, name='inventory_list'),
    path('api/inventory/add-manual/', views.api_add_product_manual, name='api_add_product_manual'),
    path('api/inventory/delete-product/<int:product_id>/', views.api_delete_product, name='api_delete_product'),
    path('api/inventory/import-excel/', views.api_import_excel_stock, name='api_import_excel_stock'),
    path('api/inventory/sample-excel/', views.api_download_sample_excel, name='api_download_sample_excel'),

    # API Endpoints for POS
    path('api/products/search/', views.api_product_search, name='api_product_search'),
    path('api/pos/checkout/', views.api_create_invoice, name='api_create_invoice'),
    path('api/pos/upi-qr/', views.api_generate_upi_qr, name='api_generate_upi_qr'),

    # Digital Khata (Udhaari Ledger)
    path('khata/', views.khata_dashboard, name='khata_dashboard'),
    path('api/khata/settle/', views.api_settle_khata, name='api_settle_khata'),

    # Analytics & Capital-Risk Analyzer
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),

    # Invoice Print View
    path('invoice/<int:invoice_id>/print/', views.invoice_print_view, name='invoice_print'),
]
