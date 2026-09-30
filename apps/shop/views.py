from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.db import models
from .models import Product, Category, ProductReview
from .forms import ReviewForm


class HomeView(ListView):
    model = Product
    template_name = 'shop/home.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all categories
        context['categories'] = Category.objects.filter(parent=None, is_active=True)
        
        # Clothing category products
        clothing_category = Category.objects.filter(category_type='clothing').first()
        if clothing_category:
            context['clothing_products'] = Product.objects.filter(
                category=clothing_category, 
                is_active=True
            )[:6]
        else:
            context['clothing_products'] = []
        
        # Hardware category products
        hardware_category = Category.objects.filter(category_type='hardware').first()
        if hardware_category:
            context['hardware_products'] = Product.objects.filter(
                category=hardware_category, 
                is_active=True
            )[:6]
        else:
            context['hardware_products'] = []
        
        # Featured products
        context['featured_products'] = Product.objects.filter(
            is_featured=True, 
            is_active=True
        )[:8]
        
        # Bestseller products
        context['bestseller_products'] = Product.objects.filter(
            is_bestseller=True, 
            is_active=True
        )[:8]
        
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Get approved reviews
        reviews = product.reviews.filter(is_approved=True)
        context['reviews'] = reviews
        context['review_form'] = ReviewForm()
        
        # Related products
        context['related_products'] = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:4]
        
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'shop/products.html'
    context_object_name = 'products'
    paginate_by = 12
    ordering = ['-created_at']  # Fix pagination warning
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | 
                Q(description__icontains=q) |
                Q(brand__icontains=q)
            )
        
        # Sort
        sort = self.request.GET.get('sort')
        if sort == 'price_low':
            queryset = queryset.order_by('price')
        elif sort == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort == 'rating':
            queryset = queryset.order_by('-rating')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['category'] = get_object_or_404(Category, slug=category_slug)
        context['all_categories'] = Category.objects.filter(parent=None, is_active=True)
        return context


@login_required
def add_review(request, product_id):
    """Add a review for a product"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            # Check if user already reviewed this product
            existing_review = ProductReview.objects.filter(
                product=product, 
                user=request.user
            ).first()
            
            if existing_review:
                messages.warning(request, 'You have already reviewed this product.')
                return redirect('shop:product_detail', slug=product.slug)
            
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            
            # Update product rating
            reviews = product.reviews.filter(is_approved=True)
            if reviews.exists():
                avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
                product.rating = avg_rating or 0
                product.total_reviews = reviews.count()
                product.save()
            
            messages.success(request, 'Your review has been submitted!')
            return redirect('shop:product_detail', slug=product.slug)
        else:
            messages.error(request, 'Please fix the errors in the form.')
            return redirect('shop:product_detail', slug=product.slug)
    
    return redirect('shop:home')