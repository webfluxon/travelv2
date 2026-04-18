# app/auth_views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json
import re

from .models import User


def login_page(request):
    """Render the login page"""
    if request.user.is_authenticated:
        return redirect('app:index')  # Redirect to homepage instead of admin_panel
    return render(request, 'app/auth/login.html')


def register_page(request):
    """Render the registration page"""
    if request.user.is_authenticated:
        return redirect('app:index')  # Redirect to homepage
    return render(request, 'app/auth/register.html')


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """API endpoint for login"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        remember = data.get('remember', False)
        
        if not email or not password:
            return JsonResponse({
                'success': False,
                'error': 'Email and password are required'
            }, status=400)
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)  # Browser session
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful',
                    'redirect': '/admin-panel/'  # Redirect to admin panel
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Account is inactive. Please contact support.'
                }, status=401)
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid email or password'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request data'
        }, status=400)
    except Exception as e:
        print(f"Login error: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Server error. Please try again.'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_register(request):
    try:
        data = json.loads(request.body)
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        phone = data.get('phone', '').strip()
        full_name = data.get('full_name', '').strip()
        
        print(f"Registration attempt for: {email}")
        
        # Validation
        if not email or not password:
            return JsonResponse({
                'success': False,
                'error': 'Email and password are required'
            }, status=400)
        
        if not full_name:
            return JsonResponse({
                'success': False,
                'error': 'Full name is required'
            }, status=400)
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                'success': False,
                'error': 'Please enter a valid email address'
            }, status=400)
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'error': 'Email already registered'
            }, status=400)
        
        # Validate password length
        if len(password) < 8:
            return JsonResponse({
                'success': False,
                'error': 'Password must be at least 8 characters'
            }, status=400)
        
        # Check if passwords match
        if password != confirm_password:
            return JsonResponse({
                'success': False,
                'error': 'Passwords do not match'
            }, status=400)
        
        # Clean phone number (remove spaces, dashes, etc.)
        if phone:
            clean_phone = re.sub(r'[\s\-\(\)\+]', '', phone)
            # Basic validation: 10-15 digits
            if not re.match(r'^[0-9]{10,15}$', clean_phone):
                # Don't fail registration, just clear the phone
                clean_phone = ''
        else:
            clean_phone = ''
        
        # Split full name into first and last name
        name_parts = full_name.strip().split()
        first_name = name_parts[0] if name_parts else ''
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
        
        # Create user - NO VERIFICATION NEEDED
        user = User.objects.create_user(
            email=email,
            password=password,
            phone=clean_phone,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            phone_verified=True  # Mark as verified since we're not doing verification
        )
        
        print(f"User created successfully: ID={user.id}, Email={email}")
        
        return JsonResponse({
            'success': True,
            'message': 'Registration successful! You can now login.',
            'redirect': '/auth/login/'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request format'
        }, status=400)
    except Exception as e:
        print(f"Registration error: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': 'Server error. Please try again.'
        }, status=500)


@require_http_methods(["POST"])
def api_logout(request):
    """API endpoint for logout"""
    try:
        logout(request)
        return JsonResponse({
            'success': True,
            'message': 'Logged out successfully',
            'redirect': '/'
        })
    except Exception as e:
        print(f"Logout error: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Server error'
        }, status=500)
