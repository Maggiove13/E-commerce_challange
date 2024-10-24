from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pedidos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productos = db.Column(db.String(255), nullable=False)  
    cantidad = db.Column(db.String(255), nullable=False)  
    estado = db.Column(db.String(50), default='pendiente')  
    fecha_compra = db.Column(db.String(50), nullable=False) 

@app.route('/pedidos', methods=['POST'])
def crear_pedido():
    data = request.get_json()
    nuevo_pedido = Pedido(
        productos=data['productos'],
        cantidad=data['cantidad'],
        estado=data.get('estado', 'pendiente'),
        fecha_compra=data['fecha_compra']
    )
    
    
    db.session.add(nuevo_pedido)
    db.session.commit()
    return jsonify({'id': nuevo_pedido.id, 'estado': nuevo_pedido.estado}), 201