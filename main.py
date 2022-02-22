from dataclasses import dataclass
from os import abort
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from producer import publish
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////main.db'
CORS(app)

db = SQLAlchemy(app)

@dataclass
class Product(db.Model):
  id: int
  title: str
  image: str
  id        = db.Column(db.Integer, primary_key=True, autoincrement=False)
  title     = db.Column(db.String(200))
  image     = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
  id             = db.Column(db.Integer, primary_key=True)
  user_id        = db.Column(db.Integer)
  product_id     = db.Column(db.Integer)

  UniqueConstraint('user_id','product_id',name='user_product_unique')

@app.route('/api/products')
def get_products():
  return jsonify(Product.query.all())

@app.route('/api/products/<int:id>/like', methods=['POST',])
def like(id):
  req = requests.get('http://localhost:8000/api/user')
  data = req.json()
  try:
    productuser = ProductUser(user_id=data['id'], product_id=id)
    db.session.add(productuser)
    db.session.commit()

    publish('Product Liked', id)
  except:
    abort('You already liked this product.')

  return jsonify({'success': True})

if __name__ == '__main__':
  app.run(debug=True)#, host='0.0.0.0')