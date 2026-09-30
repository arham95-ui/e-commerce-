from django.core.management.base import BaseCommand
from django.core.files import File
from apps.shop.models import Category, Product
from decimal import Decimal
import urllib.request
import os

class Command(BaseCommand):
    help = 'Add sample data with images to database'

    def download_image(self, url, path):
        """Download image from URL and save to path"""
        try:
            urllib.request.urlretrieve(url, path)
            return True
        except Exception as e:
            print(f"Error downloading image: {e}")
            return False

    def handle(self, *args, **kwargs):
        self.stdout.write('🔄 Adding sample data...')
        
        # Categories with images
        categories_data = [
            {
                'name': 'Clothing & Fashion',
                'category_type': 'clothing',
                'icon': '👕',
                'image_url': 'https://images.unsplash.com/photo-1445205170230-053b83016050?w=600&h=400&fit=crop',
                'description': 'Stylish clothing and fashion accessories',
                'featured': True,
                'order': 1
            },
            {
                'name': 'Hardware & Tools',
                'category_type': 'hardware',
                'icon': '🔧',
                'image_url': 'https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=600&h=400&fit=crop',
                'description': 'Professional tools and hardware',
                'featured': True,
                'order': 2
            },
            {
                'name': 'Electronics',
                'category_type': 'electronics',
                'icon': '📱',
                'image_url': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=600&h=400&fit=crop',
                'description': 'Latest electronics and gadgets',
                'featured': True,
                'order': 3
            }
        ]

        # Create Categories
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                category_type=cat_data['category_type'],
                defaults={
                    'name': cat_data['name'],
                    'icon': cat_data['icon'],
                    'image_url': cat_data['image_url'],
                    'description': cat_data['description'],
                    'featured': cat_data['featured'],
                    'order': cat_data['order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'✅ Created category: {category.name}')

        # Get category objects
        clothing = Category.objects.get(category_type='clothing')
        hardware = Category.objects.get(category_type='hardware')
        electronics = Category.objects.get(category_type='electronics')

        # Product data with image URLs
        products_data = [
            # ===== CLOTHING PRODUCTS =====
            {
                'name': 'Premium Leather Jacket',
                'category': clothing,
                'price': 199.99,
                'compare_price': 249.99,
                'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop',
                'description': 'High-quality genuine leather jacket. Perfect for any occasion.',
                'short_description': 'Genuine leather jacket',
                'brand': 'FashionHub',
                'is_featured': True,
                'is_bestseller': True,
                'stock': 50,
                'sku': 'CLTH-001'
            },
            {
                'name': 'Classic Denim Jeans',
                'category': clothing,
                'price': 79.99,
                'image_url': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&h=400&fit=crop',
                'description': 'Classic fit denim jeans. Comfortable and stylish.',
                'short_description': 'Classic denim jeans',
                'brand': 'DenimCo',
                'is_featured': True,
                'stock': 100,
                'sku': 'CLTH-002'
            },
            {
                'name': 'Summer Floral Dress',
                'category': clothing,
                'price': 89.99,
                'compare_price': 129.99,
                'image_url': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400&h=400&fit=crop',
                'description': 'Beautiful floral summer dress.',
                'short_description': 'Floral summer dress',
                'brand': 'SummerVibe',
                'is_bestseller': True,
                'stock': 75,
                'sku': 'CLTH-003'
            },
            {
                'name': 'Sports Running Shoes',
                'category': clothing,
                'price': 129.99,
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop',
                'description': 'Lightweight running shoes with excellent cushioning.',
                'short_description': 'Professional running shoes',
                'brand': 'SportMax',
                'is_bestseller': True,
                'stock': 60,
                'sku': 'CLTH-004'
            },
            # ===== HARDWARE PRODUCTS =====
            {
                'name': 'Professional Drill Set',
                'category': hardware,
                'price': 299.99,
                'compare_price': 399.99,
                'image_url': 'https://images.unsplash.com/photo-1504148455328-c376907d081c?w=400&h=400&fit=crop',
                'description': 'Professional grade drill set with 20-piece accessories.',
                'short_description': 'Professional drill set',
                'brand': 'ToolMaster',
                'is_featured': True,
                'is_bestseller': True,
                'stock': 30,
                'sku': 'HRDW-001'
            },
            {
                'name': 'Complete Toolbox Set',
                'category': hardware,
                'price': 149.99,
                'image_url': 'https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=400&h=400&fit=crop',
                'description': 'Complete toolbox with 100+ essential tools.',
                'short_description': 'Complete toolbox set',
                'brand': 'ProTools',
                'is_featured': True,
                'stock': 45,
                'sku': 'HRDW-002'
            },
            {
                'name': 'Power Circular Saw',
                'category': hardware,
                'price': 249.99,
                'compare_price': 299.99,
                'image_url': 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=400&h=400&fit=crop',
                'description': 'High-power circular saw with laser guide.',
                'short_description': 'Power circular saw',
                'brand': 'PowerTools',
                'is_bestseller': True,
                'stock': 25,
                'sku': 'HRDW-003'
            },
            # ===== ELECTRONICS PRODUCTS =====
            {
                'name': 'Wireless Noise-Canceling Headphones',
                'category': electronics,
                'price': 199.99,
                'compare_price': 249.99,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
                'description': 'Premium wireless headphones with active noise cancellation.',
                'short_description': 'Wireless noise-canceling headphones',
                'brand': 'SoundMax',
                'is_featured': True,
                'stock': 40,
                'sku': 'ELEC-001'
            },
            {
                'name': 'Smart Fitness Watch',
                'category': electronics,
                'price': 249.99,
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
                'description': 'Smart fitness watch with heart rate monitor.',
                'short_description': 'Smart fitness watch',
                'brand': 'TechWear',
                'is_featured': True,
                'stock': 35,
                'sku': 'ELEC-002'
            }
        ]

        # Create Products
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                sku=prod_data['sku'],
                defaults={
                    'name': prod_data['name'],
                    'category': prod_data['category'],
                    'price': Decimal(str(prod_data['price'])),
                    'compare_price': Decimal(str(prod_data['compare_price'])) if prod_data.get('compare_price') else None,
                    'image_url': prod_data['image_url'],
                    'description': prod_data['description'],
                    'short_description': prod_data['short_description'],
                    'brand': prod_data['brand'],
                    'is_featured': prod_data.get('is_featured', False),
                    'is_bestseller': prod_data.get('is_bestseller', False),
                    'stock': prod_data['stock'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'✅ Created product: {product.name}')
            else:
                self.stdout.write(f'↻ Product exists: {product.name}')

        self.stdout.write(self.style.SUCCESS('✅ Sample data added successfully!'))