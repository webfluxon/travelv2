from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class VisaPackage(models.Model):
    """Visa package model"""
    name = models.CharField(max_length=100, help_text="e.g., 14 Days Visa")
    price = models.CharField(max_length=50, help_text="e.g., 299 AED")
    description = models.TextField(blank=True, help_text="Brief description")
    image_url = models.URLField(max_length=500, blank=True, help_text="Image URL for the visa")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Visa Package"
        verbose_name_plural = "Visa Packages"
    
    def __str__(self):
        return f"{self.name} - {self.price}"


class TourPackage(models.Model):
    """Tour package model"""
    name = models.CharField(max_length=100, help_text="e.g., Desert Safari")
    price = models.CharField(max_length=50, help_text="e.g., AED 150")
    description = models.TextField(blank=True, help_text="Brief description")
    image_url = models.URLField(max_length=500, blank=True, help_text="Image URL for the tour")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Tour Package"
        verbose_name_plural = "Tour Packages"
    
    def __str__(self):
        return f"{self.name} - {self.price}"


class Testimonial(models.Model):
    """Customer testimonial model"""
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    avatar_url = models.URLField(max_length=500, blank=True, help_text="Avatar image URL")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        return f"{self.name} - {self.rating}★"


class WhyUsItem(models.Model):
    """Why Us section item model"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True, help_text="Image URL")
    icon_emoji = models.CharField(max_length=10, blank=True, help_text="Optional emoji icon")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Why Us Item"
        verbose_name_plural = "Why Us Items"
    
    def __str__(self):
        return self.title


class Enquiry(models.Model):
    """Customer enquiry/contact form model"""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Enquiry"
        verbose_name_plural = "Enquiries"
    
    def __str__(self):
        return f"{self.name} - {self.phone}"


class ExchangeRate(models.Model):
    """Exchange rate model (KSH to AED)"""
    ksh_to_aed = models.DecimalField(max_digits=10, decimal_places=4, default=3.5, help_text="1 KSH = ? AED")
    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100, blank=True, default="System")
    
    class Meta:
        verbose_name = "Exchange Rate"
        verbose_name_plural = "Exchange Rates"
    
    def __str__(self):
        return f"1 KSH = {self.ksh_to_aed} AED (Updated: {self.last_updated.strftime('%Y-%m-%d')})"
    
    def save(self, *args, **kwargs):
        # Ensure only one record exists
        if not self.pk and ExchangeRate.objects.exists():
            raise ValueError("Only one exchange rate record can exist. Edit the existing one instead.")
        super().save(*args, **kwargs)
    
    @classmethod
    def get_current(cls):
        """Get the current exchange rate or create default"""
        rate, created = cls.objects.get_or_create(
            defaults={'ksh_to_aed': 3.5, 'updated_by': 'System'}
        )
        return rate


class SiteSettings(models.Model):
    """General site settings"""
    site_name = models.CharField(max_length=100, default="Liviel Tours")
    site_tagline = models.CharField(max_length=200, default="UAE tours &amp; visas since 2015")
    whatsapp_number = models.CharField(max_length=50, default="+971528892781")
    whatsapp_number_kenya = models.CharField(max_length=50, default="+254705859796")
    email = models.EmailField(default="livieltourstravel@gmail.com")
    address = models.TextField(default="Baniyas Metro — Sheikha Maryiam Building, P114")
    phone_uae = models.CharField(max_length=50, default="+971 52 889 2781")
    hero_title = models.CharField(max_length=200, default="UAE visas &amp; Dubai tours — fast &amp; fairly priced")
    hero_subtitle = models.TextField(default="Visas or tours in a few taps. WhatsApp support and clear pricing.")
    hero_background_url = models.URLField(max_length=500, blank=True, default="https://images.unsplash.com/photo-1512453979798-5ea266f8880c")
    is_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Ensure only one record exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError("Only one site settings record can exist. Edit the existing one instead.")
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get the current site settings or create default"""
        settings, created = cls.objects.get_or_create(
            defaults={
                'site_name': 'Liviel Tours',
                'site_tagline': 'UAE tours &amp; visas since 2015'
            }
        )
        return settings

# Add to models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
import random
import string

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with email as username"""
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    phone_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True)
    verification_code_expires = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email
    
    def generate_verification_code(self):
        """Generate a 6-digit verification code"""
        code = ''.join(random.choices(string.digits, k=6))
        self.verification_code = code
        self.verification_code_expires = timezone.now() + timezone.timedelta(minutes=10)
        self.save()
        return code
    
    def verify_code(self, code):
        """Verify the provided code"""
        if (self.verification_code == code and 
            self.verification_code_expires and 
            timezone.now() < self.verification_code_expires):
            self.phone_verified = True
            self.verification_code = ''
            self.verification_code_expires = None
            self.save()
            return True
        return False