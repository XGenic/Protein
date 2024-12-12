from app import db, app
from app.models import Product

def init_db():
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Add some sample data
        sample_products = [
            Product(
                name='Optimum Nutrition Gold Standard Whey',
                brand='Optimum Nutrition',
                price=29.99,
                protein_per_serving=24,
                servings=30,
                marketplace='Amazon',
                url='https://amazon.com/sample',
                product_type='powder'
            ),
            Product(
                name='MyProtein Impact Whey',
                brand='MyProtein',
                price=24.99,
                protein_per_serving=21,
                servings=40,
                marketplace='MyProtein',
                url='https://myprotein.com/sample',
                product_type='powder'
            ),
            Product(
                name='Quest Protein Bar',
                brand='Quest',
                price=24.99,
                protein_per_serving=20,
                servings=12,
                marketplace='Amazon',
                url='https://amazon.com/sample-bar',
                product_type='bar'
            )
        ]
        
        # Add sample products if they don't exist
        for product in sample_products:
            existing_product = Product.query.filter_by(name=product.name).first()
            if not existing_product:
                db.session.add(product)
        
        db.session.commit()

if __name__ == '__main__':
    init_db() 