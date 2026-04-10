# app/urls.py
from django.urls import path
from . import views
from . import views_admin

app_name = 'app'

urlpatterns = [
    # Main page
    path('', views.index, name='index'),
    
    # Custom Admin Panel
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    
    # Contact form submission
    path('api/contact/', views.contact_form_submit, name='contact_submit'),
    path('api/enquiry/', views.api_enquiry_create, name='api_enquiry'),
    
    # Public API endpoints
    path('api/visa/<int:visa_id>/', views.get_visa_detail, name='visa_detail'),
    path('api/tour/<int:tour_id>/', views.get_tour_detail, name='tour_detail'),
    path('api/exchange-rate/', views.get_exchange_rate, name='exchange_rate'),
    
    # ========== ADMIN API ENDPOINTS ==========
    # Visas - One URL handles both GET and POST
    path('api/admin/visas/', views_admin.get_visas, name='admin_visas'),
    path('api/admin/visas/<int:visa_id>/', views_admin.visa_detail, name='admin_visa_detail'),
    
    # Tours - One URL handles both GET and POST
    path('api/admin/tours/', views_admin.get_tours, name='admin_tours'),
    path('api/admin/tours/<int:tour_id>/', views_admin.tour_detail, name='admin_tour_detail'),
    
    # Testimonials - One URL handles both GET and POST
    path('api/admin/testimonials/', views_admin.get_testimonials, name='admin_testimonials'),
    path('api/admin/testimonials/<int:testimonial_id>/', views_admin.testimonial_detail, name='admin_testimonial_detail'),
    
    # Why Us - One URL handles both GET and POST
    path('api/admin/whyus/', views_admin.get_whyus, name='admin_whyus'),
    path('api/admin/whyus/<int:whyus_id>/', views_admin.whyus_detail, name='admin_whyus_detail'),
    
    # Enquiries
    path('api/admin/enquiries/', views_admin.get_enquiries, name='admin_enquiries'),
    path('api/admin/enquiries/<int:enquiry_id>/', views_admin.delete_enquiry, name='admin_delete_enquiry'),
    path('api/admin/enquiries/clear-all/', views_admin.clear_all_enquiries, name='admin_clear_enquiries'),
    path('api/admin/enquiries/<int:enquiry_id>/mark-read/', views_admin.mark_enquiry_read, name='admin_mark_enquiry_read'),
    
    # Exchange Rate
    path('api/admin/exchange-rate/', views_admin.get_exchange_rate_api, name='admin_exchange_rate'),
]