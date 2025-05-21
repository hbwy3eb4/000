// Запуск всех функций при загрузке страницы
document.addEventListener('DOMContentLoaded', function () {
  initSearch()
  initCart()
  initFavorites()
  initQuantity()
})

// Поиск товаров
function initSearch() {
  const searchForm = document.querySelector('.search-form')
  const searchInput = document.querySelector('.search-input')

  if (searchForm) {
    searchForm.addEventListener('submit', async (e) => {
      e.preventDefault()
      const query = searchInput.value.trim()
      if (query) {
        try {
          const response = await fetch(`/api/products?search=${query}`)
          const products = await response.json()
          updateProducts(products)
        } catch (error) {
          showMessage('Ошибка поиска')
        }
      }
    })
  }
}

// Корзина
function initCart() {
  const addButtons = document.querySelectorAll('.add-to-cart')

  addButtons.forEach((button) => {
    button.addEventListener('click', async () => {
      const productId = button.dataset.productId
      try {
        const response = await fetch('/api/cart/add', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            productId: productId,
            quantity: 1,
          }),
        })
        const result = await response.json()
        if (result.success) {
          updateCartCount(result.count)
          showMessage('Товар добавлен в корзину')
        }
      } catch (error) {
        showMessage('Ошибка добавления в корзину')
      }
    })
  })
}

// Избранное
function initFavorites() {
  const favButtons = document.querySelectorAll('.favorite-button')

  favButtons.forEach((button) => {
    button.addEventListener('click', async () => {
      const productId = button.dataset.productId
      try {
        const response = await fetch('/api/favorites/toggle', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ productId }),
        })
        const result = await response.json()
        if (result.success) {
          button.classList.toggle('active')
          showMessage('Список избранного обновлен')
        }
      } catch (error) {
        showMessage('Ошибка обновления избранного')
      }
    })
  })
}

// Изменение количества товара
function initQuantity() {
  const quantities = document.querySelectorAll('.quantity-control')

  quantities.forEach((control) => {
    const input = control.querySelector('input')
    const minus = control.querySelector('.decrease')
    const plus = control.querySelector('.increase')

    minus.addEventListener('click', () => {
      let value = parseInt(input.value)
      if (value > 1) {
        input.value = value - 1
        updatePrice(input)
      }
    })

    plus.addEventListener('click', () => {
      let value = parseInt(input.value)
      input.value = value + 1
      updatePrice(input)
    })
  })
}

// Обновление списка товаров
function updateProducts(products) {
  const container = document.querySelector('.products-grid')
  if (!container) return

  container.innerHTML = products
    .map(
      (product) => `
        <div class="product-card">
            <img src="${product.image}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p class="price">${product.price} ₽</p>
            <button class="add-to-cart" data-product-id="${product.id}">
                В корзину
            </button>
        </div>
    `
    )
    .join('')
}
// Обновление счетчика корзины
function updateCartCount(count) {
  const counter = document.querySelector('.cart-counter')
  if (counter) {
    counter.textContent = count
    counter.style.display = count > 0 ? 'block' : 'none'
  }
}

// Обновление цены при изменении количества
function updatePrice(input) {
  const item = input.closest('.cart-item')
  const price = item.querySelector('.price').dataset.price
  const total = item.querySelector('.total')
  total.textContent = price * input.value + ' ₽'
}

// Показ сообщений
function showMessage(text) {
  const message = document.createElement('div')
  message.className = 'message'
  message.textContent = text
  document.body.appendChild(message)

  setTimeout(() => {
    message.remove()
  }, 3000)
}
