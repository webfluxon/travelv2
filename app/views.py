from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
import json
from datetime import datetime

from .models import (
    VisaPackage, TourPackage, Testimonial, WhyUsItem, 
    Enquiry, ExchangeRate, SiteSettings
)


def index(request):
    context = {
        'visas': VisaPackage.objects.filter(is_active=True),
        'tours': TourPackage.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True),
        'why_us_items': WhyUsItem.objects.filter(is_active=True),
        'exchange_rate': ExchangeRate.get_current(),
        'site_settings': SiteSettings.get_settings(),
    }
    return render(request, 'app/index.html', context)


@staff_member_required
def admin_panel(request):
    """Render the admin panel dashboard (requires login)"""
    return render(request, 'app/admin_panel.html')


def contact_form_submit(request):
    """Handle contact form submission via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else request.POST
            name = data.get('name', '').strip()
            phone = data.get('phone', '').strip()
            email = data.get('email', '').strip()
            message = data.get('message', '').strip()
            
            if not name or not phone:
                return JsonResponse({
                    'success': False, 
                    'error': 'Name and phone are required'
                }, status=400)
            
            enquiry = Enquiry.objects.create(
                name=name,
                phone=phone,
                email=email,
                message=message
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you! We will contact you shortly.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)


def get_visa_detail(request, visa_id):
    """API endpoint for visa details"""
    try:
        visa = get_object_or_404(VisaPackage, id=visa_id, is_active=True)
        return JsonResponse({
            'success': True,
            'name': visa.name,
            'price': visa.price,
            'description': visa.description,
            'image_url': visa.image_url
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=404)


def get_tour_detail(request, tour_id):
    """API endpoint for tour details"""
    try:
        tour = get_object_or_404(TourPackage, id=tour_id, is_active=True)
        return JsonResponse({
            'success': True,
            'name': tour.name,
            'price': tour.price,
            'description': tour.description,
            'image_url': tour.image_url
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def api_enquiry_create(request):
    """REST API endpoint for creating enquiries (for admin panel)"""
    try:
        data = json.loads(request.body)
        enquiry = Enquiry.objects.create(
            name=data.get('name', ''),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            message=data.get('message', '')
        )
        return JsonResponse({'success': True, 'id': enquiry.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def get_exchange_rate(request):
    """API endpoint to get current exchange rate"""
    rate = ExchangeRate.get_current()
    return JsonResponse({
        'success': True,
        'ksh_to_aed': float(rate.ksh_to_aed),
        'aed_to_ksh': round(1 / float(rate.ksh_to_aed), 4),
        'last_updated': rate.last_updated.strftime('%Y-%m-%d %H:%M:%S')
    })