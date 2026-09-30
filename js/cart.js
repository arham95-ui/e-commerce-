class CartManager {
    constructor() {
        this.cartCount = document.querySelector('.cart-count');
        this.init();
    }
    
    init() {
        document.querySelectorAll('.add-to-cart-form').forEach(form => {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData(form);
                
                try {
                    const response = await fetch(form.action, {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    if (data.success) {
                        this.updateCartCount(data.cart_total);
                        this.showToast(data.message, 'success');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    this.showToast('Error adding to cart', 'error');
                }
            });
        });
    }
    
    updateCartCount(count) {
        if (this.cartCount) {
            this.cartCount.textContent = count;
            if (count > 0) {
                this.cartCount.classList.remove('d-none');
                this.cartCount.classList.add('bounce');
                setTimeout(() => this.cartCount.classList.remove('bounce'), 500);
            }
        }
    }
    
    showToast(message, type = 'success') {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        
        const toast = document.createElement('div');
        toast.className = `toast show align-items-center text-white bg-${type === 'success' ? 'success' : 'danger'} border-0`;
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        container.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new CartManager();
});