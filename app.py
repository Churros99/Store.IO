# imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

#  aaplication init
app = Flask(__name__)

#database Init
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

#databases tables
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.float, nullable=False)
    
    def __repr__(self):
        return f'<Product {self.title}>'

# create tables


# routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

# run application
if __name__ == '__main__':
    app.run(debug=True)