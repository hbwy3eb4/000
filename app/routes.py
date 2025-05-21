from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Product, Category, CartItem
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    featured_products = Product.query.filter_by(featured=True).limit(8).all()
    categories = Category.query.all()
    return render_template('index.html', 
                         products=featured_products,
                         categories=categories)

@bp.route('/catalog')
def catalog():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search_query = request.args.get('search', '')
    
    query = Product.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))
        
    products = query.paginate(page=page, per_page=12)
    categories = Category.query.all()
    
    return render_template('catalog.html',
                         products=products,
                         categories=categories,
                         search_query=search_query)

@bp.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter_by(
        category_id=product.category_id).limit(4).all()
    return render_template('product.html',
                         product=product,
                         related_products=related_products)

@bp.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html',
                         cart_items=cart_items,
                         total=total)

@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    product = Product.query.get_or_404(product_id)
    
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Товар добавлен в корзину!', 'success')
    return redirect(url_for('main.cart'))

@bp.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    quantity = int(request.form.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        db.session.commit()
        return jsonify({'success': True})
    else:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'success': True, 'removed': True})

@bp.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Товар удален из корзины!', 'success')
    return redirect(url_for('main.cart'))

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')

# API endpoints для асинхронных запросов
@bp.route('/api/products')
def api_products():
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    
    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    
    products = query.limit(20).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'image_url': p.image_url,
        'category': p.category.name
    } for p in products])

@bp.route('/api/cart/count')
@login_required
def cart_count():
    count = CartItem.query.filter_by(user_id=current_user.id).count()
    return jsonify({'count': count})