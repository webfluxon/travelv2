# app/urls.py
from django.urls import path
from . import views
from . import views_admin
from . import auth_views

app_name = 'app'

urlpatterns = [
    # ========== MAIN PAGE ==========
    path('', views.index, name='index'),
    
    # ========== AUTHENTICATION PAGES ==========
    path('auth/login/', auth_views.login_page, name='login'),
    path('auth/register/', auth_views.register_page, name='register'),
    
    # ========== AUTHENTICATION API ENDPOINTS ==========
    path('api/auth/login/', auth_views.api_login, name='api_login'),
    path('api/auth/register/', auth_views.api_register, name='api_register'),
    path('api/auth/logout/', auth_views.api_logout, name='api_logout'),
    
    # ========== ADMIN PANEL ==========
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    
    # ========== CONTACT & ENQUIRY ENDPOINTS ==========
    path('api/contact/', views.contact_form_submit, name='contact_submit'),
    path('api/enquiry/', views.api_enquiry_create, name='api_enquiry'),
    
    # ========== PUBLIC API ENDPOINTS ==========
    path('api/visa/<int:visa_id>/', views.get_visa_detail, name='visa_detail'),
    path('api/tour/<int:tour_id>/', views.get_tour_detail, name='tour_detail'),
    path('api/exchange-rate/', views.get_exchange_rate, name='exchange_rate'),
    
    # ========== ADMIN API ENDPOINTS - VISAS ==========
    path('api/admin/visas/', views_admin.get_visas, name='admin_visas'),
    path('api/admin/visas/<int:visa_id>/', views_admin.visa_detail, name='admin_visa_detail'),
    
    # ========== ADMIN API ENDPOINTS - TOURS ==========
    path('api/admin/tours/', views_admin.get_tours, name='admin_tours'),
    path('api/admin/tours/<int:tour_id>/', views_admin.tour_detail, name='admin_tour_detail'),
    
    # ========== ADMIN API ENDPOINTS - TESTIMONIALS ==========
    path('api/admin/testimonials/', views_admin.get_testimonials, name='admin_testimonials'),
    path('api/admin/testimonials/<int:testimonial_id>/', views_admin.testimonial_detail, name='admin_testimonial_detail'),
    
    # ========== ADMIN API ENDPOINTS - WHY US ==========
    path('api/admin/whyus/', views_admin.get_whyus, name='admin_whyus'),
    path('api/admin/whyus/<int:whyus_id>/', views_admin.whyus_detail, name='admin_whyus_detail'),
    
    # ========== ADMIN API ENDPOINTS - ENQUIRIES ==========
    path('api/admin/enquiries/', views_admin.get_enquiries, name='admin_enquiries'),
    path('api/admin/enquiries/<int:enquiry_id>/', views_admin.delete_enquiry, name='admin_delete_enquiry'),
    path('api/admin/enquiries/clear-all/', views_admin.clear_all_enquiries, name='admin_clear_enquiries'),
    path('api/admin/enquiries/<int:enquiry_id>/mark-read/', views_admin.mark_enquiry_read, name='admin_mark_enquiry_read'),
    
    # ========== ADMIN API ENDPOINTS - EXCHANGE RATE ==========
    path('api/admin/exchange-rate/', views_admin.get_exchange_rate_api, name='admin_exchange_rate'),
]