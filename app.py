# imports
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

#  aaplication init
app = Flask(__name__)

#database Init
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'paswd'

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#databases tables
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<Product {self.title}>'
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, promary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))

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

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if product:
        product.title = request.form.get('title')
        product.description = request.form.get('description')
        product.price = request.form.get('price')
        db.session.commit()
        
    return redirect(url_for('home'))

@app.route('/products/delete/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()

    return redirect(url_for('home'))
    
# run application
if __name__ == '__main__':
    app.run(debug=True)