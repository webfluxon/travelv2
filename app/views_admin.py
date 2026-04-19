# app/views_admin.py - Complete working version

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .models import (
    VisaPackage, TourPackage, Testimonial, WhyUsItem, 
    Enquiry, ExchangeRate
)


def api_response(success=True, data=None, error=None, status=200):
    """Helper function to create consistent API responses"""
    response = {'success': success}
    if data is not None:
        response['data'] = data
    if error is not None:
        response['error'] = error
    return JsonResponse(response, status=status)


def serialize_visa(visa):
    return {
        'id': visa.id,
        'name': visa.name,
        'price': visa.price,
        'description': visa.description,
        'image_url': visa.image_url,
        'is_active': visa.is_active,
        'order': visa.order,
        'created_at': visa.created_at.isoformat(),
        'updated_at': visa.updated_at.isoformat()
    }


def serialize_tour(tour):
    return {
        'id': tour.id,
        'name': tour.name,
        'price': tour.price,
        'description': tour.description,
        'image_url': tour.image_url,
        'is_active': tour.is_active,
        'order': tour.order,
        'created_at': tour.created_at.isoformat(),
        'updated_at': tour.updated_at.isoformat()
    }


def serialize_testimonial(testimonial):
    return {
        'id': testimonial.id,
        'name': testimonial.name,
        'location': testimonial.location,
        'text': testimonial.text,
        'rating': testimonial.rating,
        'avatar_url': testimonial.avatar_url,
        'is_active': testimonial.is_active,
        'order': testimonial.order,
        'created_at': testimonial.created_at.isoformat()
    }


def serialize_whyus(item):
    return {
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'image_url': item.image_url,
        'icon_emoji': item.icon_emoji,
        'is_active': item.is_active,
        'order': item.order,
        'created_at': item.created_at.isoformat()
    }


def serialize_enquiry(enquiry):
    return {
        'id': enquiry.id,
        'name': enquiry.name,
        'phone': enquiry.phone,
        'email': enquiry.email,
        'message': enquiry.message,
        'is_read': enquiry.is_read,
        'created_at': enquiry.created_at.isoformat()
    }


# ========== VISA PACKAGES - Handles GET & POST ==========
@csrf_exempt
def get_visas(request):
    """Handle GET (list) and POST (create) for visas"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            visa = VisaPackage.objects.create(
                name=data.get('name'),
                price=data.get('price'),
                description=data.get('description', ''),
                image_url=data.get('image_url', ''),
                order=data.get('order', 0),
                is_active=data.get('is_active', True)
            )
            return api_response(data=serialize_visa(visa))
        except Exception as e:
            return api_response(success=False, error=str(e), status=400)
    else:  # GET
        visas = VisaPackage.objects.all().order_by('order', '-created_at')
        return api_response(data=[serialize_visa(v) for v in visas])


@csrf_exempt
def visa_detail(request, visa_id):
    """Handle PUT (update) and DELETE for single visa"""
    visa = get_object_or_404(VisaPackage, id=visa_id)
    
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            visa.name = data.get('name', visa.name)
            visa.price = data.get('price', visa.price)
            visa.description = data.get('description', visa.description)
            visa.image_url = data.get('image_url', visa.image_url)
            visa.order = data.get('order', visa.order)
            visa.is_active = data.get('is_active', visa.is_active)
            visa.save()
            return api_response(data=serialize_visa(visa))
        except Exception as e:
            return api_response(success=False, error=str(e), status=400)
    
    elif request.method == 'DELETE':
        visa.delete()
        return api_response()
    
    return api_response(success=False, error='Method not allowed', status=405)


# ========== TOUR PACKAGES - Handles GET & POST ==========
@csrf_exempt
def get_tours(request):
    """Handle GET (list) and POST (create) for tours"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tour = TourPackage.objects.create(
                name=data.get('name'),
                price=data.get('price'),
                description=data.get('description', ''),
                image_url=data.get('image_url', ''),
                order=data.get('order', 0),
                is_active=data.get('is_active', True)
            )
            return api_response(data=serialize_tour(tour))
        except Exception as e:
            return api_response(success=False, error=str(e), status=400)
    else:  # GET
        tours = TourPackage.objects.all().order_by('order', '-created_at')
        return api_response(data=[serialize_tour(t) for t in tours])


@csrf_exempt
def tour_detail(request, tour_id):
    """Handle PUT (update) and DELETE for single tour"""
    tour = get_object_or_404(TourPackage, id=tour_id)
    
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            tour.name = data.get('name', tour.name)
            tour.price = data.get('price', tour.price)
            tour.description = data.get('description', tour.description)
            tour.image_url = data.get('image_url', tour.image_url)
            tour.order = data.get('order', tour.order)
            tour.is_active = data.get('is_active', tour.is_active)
            tour.save()
            return api_response(data=serialize_tour(tour))
        except Exception as e:
            return api_response(success=False, error=str(e), status=400)
    
    elif request.method == 'DELETE':
        tour.delete()
        return api_response()
    
    return api_response(success=False, error='Method not allowed', status=405)


# ========== TESTIMONIALS - Handles GET & POST ==========
@csrf_exempt
def get_testimonials(request):
    """Handle GET (list) and POST (create) for testimonials"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            testimonial = Testimonial.objects.create(
                name=data.get('name'),
                location=data.get('location', ''),
                text=data.get('text', ''),
                rating=data.get('rating', 5),
                avatar_url=data.get('avatar_url', ''),
                order=data.get('order', 0),
                is_active=data.get('is_active', True)
            )
            return api_response(data=serialize_testimonial(testimonial))
        except Exception as e:
            return api_response(success=False, error=str(e), status=400)
    else:  # GET
        testimonials = Testimonial.objects.all().order_by('order', '-created_at')
        return api_response(data=[serialize_testimonial(t) for t in testimonials])


@csrf_exempt
def testimonial_detail(request, testimonial_id):
    """Handle PUT (update) and DELETE for single testimonial"""
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            testimonial.name = data.get('name', testimonial.name)
            testimonial.location = data.get('location', testimonial.location)
            testimonial.text = data.get('text', testimonial.text)
            testimonial.rating = data.get('rating', testimonial.rating)
            testimonial.avatar_url = data.get('avatar_url', testimonial.avatar_url)
            testimonial.order = data.get('order', testimonial.order)
            testimonial.is_active = data.get('is_active', testimonial.is_active)
            testimonial.save()
            return api_response(data=serialize_testimonial(testimonial))
        except Exception as e:
            return api_response(success=False, error=str(e), status=400)
    
    elif request.method == 'DELETE':
        testimonial.delete()
        return api_response()
    
    return api_response(success=False, error='Method not allowed', status=405)


# ========== WHY US - Handles GET & POST ==========
@csrf_exempt
def get_whyus(request):
    """Handle GET (list) and POST (create) for why us items"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item = WhyUsItem.objects.create(
                title=data.get('title'),
                description=data.get('description', ''),
                image_url=data.get('image_url', ''),
                icon_emoji=data.get('icon_emoji', ''),
                order=data.get('order', 0),
                is_active=data.get('is_active', True)
            )
            return api_response(data=serialize_whyus(item))
        except Exception as e:
            return api_response(success=False, error=str(e), status=400)
    else:  # GET
        items = WhyUsItem.objects.all().order_by('order', '-created_at')
        return api_response(data=[serialize_whyus(i) for i in items])


@csrf_exempt
def whyus_detail(request, whyus_id):
    """Handle PUT (update) and DELETE for single why us item"""
    item = get_object_or_404(WhyUsItem, id=whyus_id)
    
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            item.title = data.get('title', item.title)
            item.description = data.get('description', item.description)
            item.image_url = data.get('image_url', item.image_url)
            item.icon_emoji = data.get('icon_emoji', item.icon_emoji)
            item.order = data.get('order', item.order)
            item.is_active = data.get('is_active', item.is_active)
            item.save()
            return api_response(data=serialize_whyus(item))
        except Exception as e:
            return api_response(success=False, error=str(e), status=400)
    
    elif request.method == 'DELETE':
        item.delete()
        return api_response()
    
    return api_response(success=False, error='Method not allowed', status=405)


# ========== ENQUIRIES ==========
@csrf_exempt
def get_enquiries(request):
    """Get all enquiries"""
    enquiries = Enquiry.objects.all().order_by('-created_at')
    return api_response(data=[serialize_enquiry(e) for e in enquiries])


@csrf_exempt
def delete_enquiry(request, enquiry_id):
    """Delete an enquiry"""
    try:
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)
        enquiry.delete()
        return api_response()
    except Exception as e:
        return api_response(success=False, error=str(e), status=400)


@csrf_exempt
def clear_all_enquiries(request):
    """Delete all enquiries"""
    try:
        Enquiry.objects.all().delete()
        return api_response()
    except Exception as e:
        return api_response(success=False, error=str(e), status=400)


@csrf_exempt
def mark_enquiry_read(request, enquiry_id):
    """Mark an enquiry as read"""
    try:
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)
        enquiry.is_read = True
        enquiry.save()
        return api_response(data=serialize_enquiry(enquiry))
    except Exception as e:
        return api_response(success=False, error=str(e), status=400)


# ========== EXCHANGE RATE ==========
@csrf_exempt
def get_exchange_rate_api(request):
    """Get or update exchange rate"""
    rate = ExchangeRate.get_current()
    
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            new_rate = float(data.get('ksh_to_aed'))
            
            if new_rate <= 0 or new_rate > 100:
                return api_response(success=False, error='Invalid exchange rate', status=400)
            
            rate.ksh_to_aed = new_rate
            
            # ✅ CLEVER FIX: Use str(request.user) which calls User.__str__()
            if request.user.is_authenticated:
                rate.updated_by = str(request.user)
            else:
                rate.updated_by = 'System'
            
            rate.save()
            
            return api_response(data={
                'ksh_to_aed': float(rate.ksh_to_aed),
                'aed_to_ksh': round(1 / float(rate.ksh_to_aed), 2),
                'last_updated': rate.last_updated.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_by': rate.updated_by
            })
        except ValueError:
            return api_response(success=False, error='Invalid rate value', status=400)
        except Exception as e:
            return api_response(success=False, error=str(e), status=400)
    else:  # GET
        return api_response(data={
            'ksh_to_aed': float(rate.ksh_to_aed),
            'aed_to_ksh': round(1 / float(rate.ksh_to_aed), 2),
            'last_updated': rate.last_updated.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_by': rate.updated_by
        })