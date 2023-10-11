from . import shop
from flask import render_template, redirect,url_for,flash
from flask_login import login_required,current_user
from models import Product, CartItem
from run import db


## Shop routes
@shop.route('/shop', methods=["GET", "POST"])
def shop_page():
    return render_template('shop.html')


@shop.route('/products')
def list_products():
    products = Product.query.all()
    return render_template('shop/products.html', products=products)


@shop.route('/product/<int:product_id>')
def view_product(product_id):
    product = Product.query.get(product_id)
    return render_template('shop/product_details.html', product=product)


@shop.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    
    existing_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    
    if existing_item:
        flash('Product is already in your cart.', 'warning')
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product.id)
        db.session.add(cart_item)
        db.session.commit()
        flash('Product added to your cart.', 'success')
    
    return redirect(url_for('shop.list_products'))


@shop.route('/cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.product.price for item in cart_items)
    return render_template('shop/cart.html', cart_items=cart_items, total_price=total_price)


@shop.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get(item_id)
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Product removed from your cart.', 'success')
    
    return redirect(url_for('shop.view_cart'))


@shop.route('/clear_cart')
@login_required
def clear_cart():
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('All items removed from your cart.', 'success')
    return redirect(url_for('shop.view_cart'))

