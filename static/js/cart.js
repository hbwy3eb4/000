// Управление корзиной
class Cart {
    constructor() {
        this.items = [];
        this.total = 0;
        this.init();
    }

    init() {
        this.loadCart();
        this.bindEvents();
        this.updateCartDisplay();
    }

    // Привязка событий
    bindEvents() {
        // Кнопки удаления товара
        document.querySelectorAll('.remove-item').forEach(button => {
            button.addEventListener('click', (e) => {
                const itemId = e.target.dataset.id;
                this.removeItem(itemId);
            });
        });

        // Изменение количества
        document.querySelectorAll('.quantity-input').forEach(input => {
            input.addEventListener('change', (e) => {
                const itemId = e.target.dataset.id;
                const quantity = parseInt(e.target.value);
                this.updateQuantity(itemId, quantity);
            });
        });

        // Кнопка очистки корзины
        const clearButton = document.querySelector('.clear-cart');
        if (clearButton) {
            clearButton.addEventListener('click', () => this.clearCart());
        }

        // Кнопка оформления заказа
        const checkoutButton = document.querySelector('.checkout-button');
        if (checkoutButton) {
            checkoutButton.addEventListener('click', () => this.checkout());
        }
    }

    // Добавление товара в корзину
    async addItem(productId, quantity = 1) {
        try {
            const response = await fetch('/api/cart/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    productId,
                    quantity
                })
            });

            const result = await response.json();
            if (result.success) {
                this.loadCart();
                this.showMessage('Товар добавлен в корзину');
            }
        } catch (error) {
            this.showMessage('Ошибка при добавлении товара', 'error');
        }
    }

    // Удаление товара из корзины
    async removeItem(itemId) {
        try {
            const response = await fetch(`/api/cart/remove/${itemId}`, {
                method: 'POST'
            });

            const result = await response.json();
            if (result.success) {
                this.loadCart();
                this.showMessage('Товар удален из корзины');
            }
        } catch (error) {
            this.showMessage('Ошибка при удалении товара', 'error');
        }
    }

    // Обновление количества товара
    async updateQuantity(itemId, quantity) {
        if (quantity < 1) return;

        try {
            const response = await fetch('/api/cart/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    itemId,
                    quantity
                })
            });

            const result = await response.json();
            if (result.success) {
                this.loadCart();
            }
        } catch (error) {
            this.showMessage('Ошибка при обновлении количества', 'error');
        }
    }

    // Загрузка корзины с сервера
    async loadCart() {
        try {
            const response = await fetch('/api/cart');
            const data = await response.json();
            this.items = data.items;
            this.total = data.total;
            this.updateCartDisplay();
        } catch (error) {
            this.showMessage('Ошибка при загрузке корзины', 'error');
        }
    }

    // Очистка корзины
    async clearCart() {
        try {
            const response = await fetch('/api/cart/clear', {
                method: 'POST'
            });
const result = await response.json();
            if (result.success) {
                this.items = [];
                this.total = 0;
                this.updateCartDisplay();
                this.showMessage('Корзина очищена');
            }
        } catch (error) {
            this.showMessage('Ошибка при очистке корзины', 'error');
        }
    }

    // Оформление заказа
    async checkout() {
        if (this.items.length === 0) {
            this.showMessage('Корзина пуста');
            return;
        }

        try {
            const response = await fetch('/api/orders/create', {
                method: 'POST'
            });

            const result = await response.json();
            if (result.success) {
                window.location.href = '/checkout';
            }
        } catch (error) {
            this.showMessage('Ошибка при оформлении заказа', 'error');
        }
    }

    // Обновление отображения корзины
    updateCartDisplay() {
        // Обновление счетчика товаров
        const counter = document.querySelector('.cart-counter');
        if (counter) {
            const itemCount = this.items.reduce((sum, item) => sum + item.quantity, 0);
            counter.textContent = itemCount;
            counter.style.display = itemCount > 0 ? 'block' : 'none';
        }

        // Обновление общей суммы
        const totalElement = document.querySelector('.cart-total');
        if (totalElement) {
            totalElement.textContent = ${this.total} ₽;
        }

        // Обновление списка товаров
        const cartItems = document.querySelector('.cart-items');
        if (cartItems) {
            cartItems.innerHTML = this.items.map(item => 
                <div class="cart-item" data-id="${item.id}">
                    <img src="${item.image}" alt="${item.name}" class="cart-item-image">
                    <div class="cart-item-details">
                        <h3>${item.name}</h3>
                        <div class="cart-item-price">${item.price} ₽</div>
                    </div>
                    <div class="cart-item-controls">
                        <div class="quantity-control">
                            <button class="decrease">-</button>
                            <input type="number" value="${item.quantity}" 
                                    class="quantity-input" data-id="${item.id}">
                            <button class="increase">+</button>
                        </div>
                        <button class="remove-item" data-id="${item.id}">Удалить</button>
                    </div>
                </div>
            ).join('');

            // Переподключение обработчиков событий
            this.bindEvents();
        }
    }

    // Показ сообщений
    showMessage(text, type = 'success') {
        const message = document.createElement('div');
        message.className = message message-${type};
        message.textContent = text;
        document.body.appendChild(message);

        setTimeout(() => {
            message.remove();
        }, 3000);
    }
}

// Создание экземпляра корзины при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.cart = new Cart();
});