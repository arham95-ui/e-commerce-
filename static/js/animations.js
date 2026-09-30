// Smooth Animations and Interactions
document.addEventListener('DOMContentLoaded', function() {
    // Lazy loading images
    const lazyImages = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        lazyImages.forEach(img => imageObserver.observe(img));
    }
    
    // Smooth scroll to top
    const scrollTopBtn = document.querySelector('.scroll-top');
    if (scrollTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                scrollTopBtn.classList.add('visible');
            } else {
                scrollTopBtn.classList.remove('visible');
            }
        });
        
        scrollTopBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
    
    // Price filter range slider
    const priceRange = document.querySelector('.price-range');
    if (priceRange) {
        const minVal = document.getElementById('min-price');
        const maxVal = document.getElementById('max-price');
        const rangeMin = document.getElementById('range-min');
        const rangeMax = document.getElementById('range-max');
        
        // Update price range display
        const updatePriceRange = () => {
            if (minVal && maxVal) {
                const min = parseInt(minVal.value);
                const max = parseInt(maxVal.value);
                if (rangeMin) rangeMin.textContent = `$${min}`;
                if (rangeMax) rangeMax.textContent = `$${max}`;
            }
        };
        
        if (minVal) minVal.addEventListener('input', updatePriceRange);
        if (maxVal) maxVal.addEventListener('input', updatePriceRange);
    }
    
    // Wishlist toggle
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
        btn.addEventListener('click', async function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const icon = this.querySelector('i');
            
            try {
                const response = await fetch('/wishlist/toggle/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ product_id: productId })
                });
                
                const data = await response.json();
                if (data.success) {
                    if (data.added) {
                        icon.className = 'fas fa-heart text-danger fs-4';
                        this.classList.add('animated');
                        setTimeout(() => this.classList.remove('animated'), 500);
                    } else {
                        icon.className = 'far fa-heart fs-4';
                    }
                    
                    // Update wishlist count
                    const wishlistCount = document.querySelector('.wishlist-count');
                    if (wishlistCount) {
                        wishlistCount.textContent = data.total_wishlist;
                    }
                }
            } catch (error) {
                console.error('Error toggling wishlist:', error);
            }
        });
    });
    
    // Product filter with animation
    const filterCheckboxes = document.querySelectorAll('.filter-checkbox');
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const filterForm = this.closest('form');
            if (filterForm) {
                filterForm.submit();
            }
        });
    });
    
    // Quantity input buttons
    document.querySelectorAll('.quantity-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            if (input) {
                let value = parseInt(input.value);
                if (this.dataset.action === 'increase') {
                    value = Math.min(value + 1, parseInt(input.max) || 99);
                } else {
                    value = Math.max(value - 1, parseInt(input.min) || 1);
                }
                input.value = value;
                input.dispatchEvent(new Event('change'));
            }
        });
    });
    
    // Auto-hide alerts
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
    
    // Product gallery
    const mainImage = document.querySelector('.product-main-image');
    const thumbnails = document.querySelectorAll('.product-thumbnail');
    if (mainImage && thumbnails.length) {
        thumbnails.forEach(thumb => {
            thumb.addEventListener('click', function() {
                const imgSrc = this.dataset.src || this.src;
                mainImage.src = imgSrc;
                thumbnails.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }
    
    // Star rating hover effect
    document.querySelectorAll('.star-rating .fa-star').forEach(star => {
        star.addEventListener('mouseenter', function() {
            const rating = parseInt(this.dataset.rating);
            const container = this.closest('.star-rating');
            container.querySelectorAll('.fa-star').forEach(s => {
                const starRating = parseInt(s.dataset.rating);
                if (starRating <= rating) {
                    s.classList.add('hovered');
                } else {
                    s.classList.remove('hovered');
                }
            });
        });
        
        star.addEventListener('mouseleave', function() {
            const container = this.closest('.star-rating');
            container.querySelectorAll('.fa-star').forEach(s => {
                s.classList.remove('hovered');
            });
        });
    });
});

// Utility functions
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
           document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
}