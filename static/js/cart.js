// Global Cart Functions
document.addEventListener('DOMContentLoaded', function() {
    
    // Handle all add to cart forms
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const action = this.action;
            
            // Get CSRF token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                             getCookie('csrftoken');
            
            formData.append('csrfmiddlewaretoken', csrfToken);
            
            fetch(action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update cart count
                    updateCartCount(data.cart_total);
                    showToast('✅ ' + data.message, 'success');
                } else {
                    showToast('❌ ' + data.error, 'error');
                }
            })
            .catch(error => {
                showToast('❌ Error adding to cart', 'error');
                console.error('Error:', error);
            });
        });
    });
});

// Update cart count
function updateCartCount(count) {
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        cartCount.textContent = count;
        if (count > 0) {
            cartCount.classList.remove('d-none');
            cartCount.classList.add('bounce');
            setTimeout(() => {
                cartCount.classList.remove('bounce');
            }, 500);
        } else {
            cartCount.classList.add('d-none');
        }
    }
}

// Toast notification
function showToast(message, type = 'success') {
    const existingToasts = document.querySelectorAll('.custom-toast');
    existingToasts.forEach(toast => toast.remove());
    
    const toast = document.createElement('div');
    toast.className = `custom-toast alert alert-${type === 'success' ? 'success' : 'danger'} position-fixed`;
    toast.style.cssText = `
        top: 80px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        animation: slideInRight 0.5s ease;
    `;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close float-end" onclick="this.parentElement.remove()"></button>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.5s ease';
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}

// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    .custom-toast {
        animation: slideInRight 0.5s ease;
    }
    .cart-count.bounce {
        animation: bounceIn 0.5s ease;
    }
    @keyframes bounceIn {
        0% { transform: scale(0); }
        50% { transform: scale(1.5); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(style);