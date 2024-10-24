from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carrito.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Carritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable= False)
    producto_id = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    fecha_agregado = db.Column(db.DateTime, default=func.now())


@app.route('/carrito', methods=['POST'])
def agregar_al_carrito():
    data = request.get_json()
    nuevo_item = Carritos(
        user_id = data['user_id'],
        producto_id = data['producto_id'],
        cantidad = data.get('cantidad', 1)
    )
    
    print(nuevo_item)
    
    db.session.add(nuevo_item)
    db.session.commit()
    return jsonify({'user_id': nuevo_item.user_id, 
                    'id': nuevo_item.id, 
                    'producto_id': nuevo_item.producto_id,
                    'cantidad': nuevo_item.cantidad}), 201



@app.route('/carrito/<int:user_id>', methods=['GET'])
def listar_carrito(user_id):
    items = Carritos.query.filter_by(user_id = user_id).all()
    
    return jsonify([{'id': item.id, 
                    'producto_id': item.producto_id, 
                    'cantidad': item.cantidad} for item in items]), 200