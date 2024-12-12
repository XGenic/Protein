from flask import render_template
from app import app
from app.models import Product

@app.route('/')
def index():
    return render_template('index.html') 