document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
    
    // Wishlist toggle
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
        btn.addEventListener('click', async function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const icon = this.querySelector('i');
            
            try {
                const response = await fetch(`/wishlist/toggle/${productId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    }
                });
                
                const data = await response.json();
                if (data.success) {
                    if (data.added) {
                        icon.className = 'fas fa-heart text-danger fs-4';
                    } else {
                        icon.className = 'far fa-heart fs-4';
                    }
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
});

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
           document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
}