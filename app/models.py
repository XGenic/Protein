from app import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    protein_per_serving = db.Column(db.Float, nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    marketplace = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(500))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def protein_price_ratio(self):
        total_protein = self.protein_per_serving * self.servings
        return self.price / total_protein if total_protein > 0 else float('inf') 