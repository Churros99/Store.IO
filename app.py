# imports
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#  aaplication init
app = Flask(__name__)

#database Init
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy()
db.init_app(app)

#databases tables
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<Product {self.title}>'

# create tables
with app.app_context():
    db.create_all()

# routes
@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products = products)

@app.route('/login')
def login():
    return render_template('login.html')

# Products Routes
@app.route('/products', methods=['POST', 'GET'])
def create_product():
    try:
        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            price = request.form.get('price')
            product = Product(title=title, description=description, price=price)
    
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('home'))
        elif request.method == 'GET':
            return render_template('create_product.html')
    except Exception as inst:
        print(inst.args)

# run application
if __name__ == '__main__':
    app.run(debug=True)