from flask import render_template, jsonify, request
from app import app, db
from app.models import Product
from sqlalchemy import or_

@app.route('/')
def index():
    # Get search parameters
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'price_per_protein')  # default sort
    product_type = request.args.get('type', 'all')
    
    # Start with base query
    query = Product.query
    
    # Apply search if provided
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f'%{search}%'),
                Product.brand.ilike(f'%{search}%')
            )
        )
    
    # Apply product type filter
    if product_type != 'all':
        query = query.filter(Product.product_type == product_type)
    
    # Apply sorting
    if sort_by == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'protein':
        query = query.order_by(Product.protein_per_serving.desc())
    elif sort_by == 'price_per_protein':
        # Note: This is a bit tricky as we can't sort by computed values directly
        # We'll sort by price/protein ratio in Python
        products = query.all()
        products.sort(key=lambda x: x.protein_price_ratio())
    else:
        products = query.all()
    
    return render_template('index.html', 
                         products=products,
                         search=search,
                         sort_by=sort_by,
                         product_type=product_type)

@app.route('/api/products')
def get_products():
    products = Product.query.all()
    return jsonify([{
        'name': p.name,
        'brand': p.brand,
        'price': p.price,
        'protein_per_serving': p.protein_per_serving,
        'servings': p.servings,
        'price_per_protein': p.protein_price_ratio()
    } for p in products]) 

@app.route('/api/search')
def search_products():
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'price_per_protein')
    product_type = request.args.get('type', 'all')
    
    query = Product.query
    
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f'%{search}%'),
                Product.brand.ilike(f'%{search}%')
            )
        )
    
    if product_type != 'all':
        query = query.filter(Product.product_type == product_type)
        
    products = query.all()
    
    if sort_by == 'price_low':
        products.sort(key=lambda x: x.price)
    elif sort_by == 'price_high':
        products.sort(key=lambda x: -x.price)
    elif sort_by == 'protein':
        products.sort(key=lambda x: -x.protein_per_serving)
    elif sort_by == 'price_per_protein':
        products.sort(key=lambda x: x.protein_price_ratio())
    
    return jsonify([{
        'name': p.name,
        'brand': p.brand,
        'price': p.price,
        'protein_per_serving': p.protein_per_serving,
        'servings': p.servings,
        'price_per_protein': p.protein_price_ratio(),
        'product_type': p.product_type
    } for p in products]) 