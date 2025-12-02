// API Configuration
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : window.location.origin.replace('-5500', '-8000');

let currentUser = null;
let currentCart = [];

// Heavy computation bottleneck for LCP
function heavyComputation() {
    let result = 0;
    // CPU-intensive operation that runs before content is interactive
    for (let i = 0; i < 100000000; i++) {
        result += Math.sqrt(i) * Math.sin(i) * Math.cos(i);
    }
    return result;
}

// Initialize app
async function init() {
    try {
        // BOTTLENECK: Run blocking computation on main thread during init
        console.log('Starting heavy computation...');
        heavyComputation(); // This blocks rendering and increases LCP
        console.log('Heavy computation complete');
        
        // Login as demo user
        const loginResponse = await fetch(`${API_BASE_URL}/demo/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: 'demo@example.com' })
        });
        
        const loginData = await loginResponse.json();
        currentUser = loginData.user;
        
        document.getElementById('userEmail').textContent = currentUser.email;
        
        // Load initial data
        await loadProducts();
        await loadCart();
        
    } catch (error) {
        console.error('Initialization error:', error);
        showNotification('Failed to initialize app', 'error');
    }
}

// Load products
async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/products/`);
        const products = await response.json();
        
        const grid = document.getElementById('productsGrid');
        
        if (products.length === 0) {
            grid.innerHTML = '<div class="empty-cart">No products available</div>';
            return;
        }
        
        grid.innerHTML = products.map(product => `
            <div class="product-card">
                <div class="product-category">${product.category || 'General'}</div>
                <div class="product-name">${product.name}</div>
                <div class="product-description">${product.description || 'No description available'}</div>
                <div class="product-price">$${product.price.toFixed(2)}</div>
                <div class="product-stock">${product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}</div>
                <button 
                    class="add-to-cart-btn" 
                    onclick="addToCart(${product.id})"
                    ${product.stock === 0 ? 'disabled' : ''}
                >
                    ${product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
                </button>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error loading products:', error);
        showNotification('Failed to load products', 'error');
    }
}

// Add to cart
async function addToCart(productId) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/${currentUser.id}/cart`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: 1
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to add to cart');
        }
        
        showNotification('Added to cart!');
        await loadCart();
        
    } catch (error) {
        console.error('Error adding to cart:', error);
        showNotification('Failed to add to cart', 'error');
    }
}

// Load cart
async function loadCart() {
    try {
        const response = await fetch(`${API_BASE_URL}/users/${currentUser.id}/cart`);
        currentCart = await response.json();
        
        updateCartCount();
        displayCart();
        
    } catch (error) {
        console.error('Error loading cart:', error);
    }
}

// Update cart count badge
function updateCartCount() {
    const count = currentCart.length;
    document.getElementById('cartCount').textContent = count;
}

// Display cart
function displayCart() {
    const cartItemsDiv = document.getElementById('cartItems');
    
    if (currentCart.length === 0) {
        cartItemsDiv.innerHTML = '<div class="empty-cart">Your cart is empty</div>';
        return;
    }
    
    const total = currentCart.reduce((sum, item) => {
        return sum + (item.product.price * item.quantity);
    }, 0);
    
    cartItemsDiv.innerHTML = `
        ${currentCart.map(item => `
            <div class="cart-item">
                <div class="cart-item-info">
                    <div class="cart-item-name">${item.product.name}</div>
                    <div class="cart-item-price">
                        $${item.product.price.toFixed(2)} x ${item.quantity} = $${(item.product.price * item.quantity).toFixed(2)}
                    </div>
                </div>
                <button class="remove-btn" onclick="removeFromCart(${item.id})">Remove</button>
            </div>
        `).join('')}
        
        <div class="cart-total">Total: $${total.toFixed(2)}</div>
        <button class="checkout-btn" onclick="checkout()">Proceed to Checkout</button>
    `;
}

// Remove from cart
async function removeFromCart(itemId) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/${currentUser.id}/cart/${itemId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to remove item');
        }
        
        showNotification('Item removed from cart');
        await loadCart();
        
    } catch (error) {
        console.error('Error removing from cart:', error);
        showNotification('Failed to remove item', 'error');
    }
}

// Checkout
async function checkout() {
    if (currentCart.length === 0) {
        showNotification('Cart is empty', 'error');
        return;
    }
    
    if (!confirm('Proceed with checkout?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/${currentUser.id}/checkout`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error('Checkout failed');
        }
        
        const result = await response.json();
        
        showNotification(`Order completed! Total: $${result.total.toFixed(2)}`);
        
        await loadCart();
        await loadProducts(); // Refresh to show updated stock
        
        // Switch to orders tab
        setTimeout(() => {
            showTab('orders');
        }, 1500);
        
    } catch (error) {
        console.error('Checkout error:', error);
        showNotification('Checkout failed', 'error');
    }
}

// Load orders
async function loadOrders() {
    try {
        const response = await fetch(`${API_BASE_URL}/users/${currentUser.id}/orders`);
        const orders = await response.json();
        
        const ordersDiv = document.getElementById('ordersList');
        
        if (orders.length === 0) {
            ordersDiv.innerHTML = '<div class="empty-cart">No orders yet</div>';
            return;
        }
        
        ordersDiv.innerHTML = orders.map(order => `
            <div class="order-card">
                <div class="order-header">
                    <div>
                        <div class="order-id">Order #${order.id}</div>
                        <div style="color: #666; font-size: 14px; margin-top: 5px;">
                            ${new Date(order.created_at).toLocaleDateString()} at ${new Date(order.created_at).toLocaleTimeString()}
                        </div>
                    </div>
                    <div class="order-status">${order.status}</div>
                </div>
                <div>
                    ${order.items.map(item => `
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px; padding: 8px; background: #f9f9f9; border-radius: 4px;">
                            <span>${item.product.name} x ${item.quantity}</span>
                            <span style="font-weight: 600;">$${(item.unit_price_cents * item.quantity / 100).toFixed(2)}</span>
                        </div>
                    `).join('')}
                </div>
                <div style="text-align: right; margin-top: 15px; font-size: 18px; font-weight: bold; color: #667eea;">
                    Total: $${(order.total_cents / 100).toFixed(2)}
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error loading orders:', error);
        showNotification('Failed to load orders', 'error');
    }
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Show cart
function showCart() {
    showTab('cart');
}

// Tab navigation
function showTab(tab) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target?.classList.add('active');
    
    // Update sections
    document.getElementById('productsSection').style.display = tab === 'products' ? 'block' : 'none';
    document.getElementById('cartSection').classList.toggle('active', tab === 'cart');
    document.getElementById('ordersSection').classList.toggle('active', tab === 'orders');
    
    // Load data if needed
    if (tab === 'orders') {
        loadOrders();
    } else if (tab === 'cart') {
        displayCart();
    }
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', init);
